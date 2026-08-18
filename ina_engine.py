#!/usr/bin/env python3
"""INA execution engine — loads an INA JSON and makes decisions with it.

Implements the executable core described in INA_Project_Definition.pdf:
  1. parse log text -> structured candidates (feature extraction)
  2. check red flags (veto)
  3. score candidates with the weighted priority framework from the INA
  4. pick the highest-scoring flag-free candidate, or REJECT all

Scoring formulas mirror the `check` strings stored in the INA JSON
(see ina/ina_tech_selection_alice_v1.json).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Log parsing (natural-language log -> structured candidate)
# ---------------------------------------------------------------------------

_PATTERNS = {
    "stars": re.compile(r"GitHub stars (\d+)"),
    "last_commit_days": re.compile(r"最近一次提交在 (\d+) 天前"),
    "release_cycle_months": re.compile(r"约 (\d+) 个月发布一个版本"),
    "open_issues": re.compile(r"开放 issue (\d+) 个"),
    "team_familiarity": re.compile(r"团队已有 (\d+) 人"),
    "completeness": re.compile(r"功能覆盖度约 (\d+)%"),
    "bundle_kb": re.compile(r"打包后约 (\d+)kb"),
    "render_ms": re.compile(r"渲染耗时约 (\d+)ms"),
    "maintainers_single": re.compile(r"仅由一位维护者维护"),
    "maintainers_multi": re.compile(r"由 (\d+) 位维护者共同维护"),
    "typescript_yes": re.compile(r"官方提供 TypeScript 类型定义"),
    "typescript_no": re.compile(r"不提供 TypeScript 类型定义"),
}

@dataclass
class Candidate:
    name: str
    stars: int
    last_commit_days: int
    release_cycle_months: int
    open_issues: int
    team_familiarity: int
    completeness: float
    bundle_kb: int
    render_ms: int
    maintainers: int
    typescript: bool

    def to_dict(self) -> dict:
        return asdict(self)

def parse_candidates(log_text: str) -> list[Candidate]:
    """Extract one Candidate per '- <name>：...' line in the log."""
    cands: list[Candidate] = []
    for line in log_text.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        name = line[2:].split("：")[0].strip()
        m = _PATTERNS["maintainers_single"].search(line)
        if m:
            maintainers = 1
        else:
            m = _PATTERNS["maintainers_multi"].search(line)
            maintainers = int(m.group(1)) if m else 1
        cands.append(Candidate(
            name=name,
            stars=int(_PATTERNS["stars"].search(line).group(1)),
            last_commit_days=int(_PATTERNS["last_commit_days"].search(line).group(1)),
            release_cycle_months=int(_PATTERNS["release_cycle_months"].search(line).group(1)),
            open_issues=int(_PATTERNS["open_issues"].search(line).group(1)),
            team_familiarity=int(_PATTERNS["team_familiarity"].search(line).group(1)),
            completeness=int(_PATTERNS["completeness"].search(line).group(1)) / 100.0,
            bundle_kb=int(_PATTERNS["bundle_kb"].search(line).group(1)),
            render_ms=int(_PATTERNS["render_ms"].search(line).group(1)),
            maintainers=maintainers,
            typescript=bool(_PATTERNS["typescript_yes"].search(line)),
        ))
    return cands

# ---------------------------------------------------------------------------
# INA engine
# ---------------------------------------------------------------------------

class INA:
    """Loads an INA document and executes its decision patterns."""

    def __init__(self, ina_dict: dict):
        self.ina = ina_dict["ina"]
        self.metadata = self.ina["metadata"]
        self.patterns = self.ina["decision_patterns"]
        self.preferences = self.ina["preference_model"]

    @classmethod
    def load(cls, path: str | Path) -> "INA":
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    # -- red flags ----------------------------------------------------------
    def _check_red_flags(self, cand: Candidate) -> list[str]:
        flags = []
        if cand.maintainers == 1:
            flags.append("single_maintainer")
        if cand.last_commit_days > 180:
            flags.append("stale_commit")
        if not cand.typescript:
            flags.append("no_typescript")
        return flags

    # -- scoring (formulas mirror the INA's check strings) ------------------
    @staticmethod
    def _score_factor(factor: str, c: Candidate) -> float:
        if factor == "community_activity":
            return 0.7 * min(1.0, c.stars / 15000) + 0.3 * max(0.0, 1 - c.last_commit_days / 180)
        if factor == "maintenance":
            return 0.6 * max(0.0, 1 - c.release_cycle_months / 12) + 0.4 * max(0.0, 1 - c.open_issues / 300)
        if factor == "team_familiarity":
            return min(1.0, c.team_familiarity / 5)
        if factor == "completeness":
            return c.completeness
        if factor == "performance":
            return 0.5 * max(0.0, 1 - c.bundle_kb / 150) + 0.5 * max(0.0, 1 - c.render_ms / 60)
        raise ValueError(f"unknown factor: {factor}")

    def _score(self, cand: Candidate) -> tuple[float, dict[str, float]]:
        pattern = self.patterns[0]
        weights = {f["factor"]: f["weight"] for f in pattern["priority_framework"]}
        factor_scores = {f: self._score_factor(f, cand) for f in weights}
        total = sum(weights[f] * factor_scores[f] for f in weights)
        return total, factor_scores

    # -- decision ------------------------------------------------------------
    def decide(self, cands: list[Candidate]) -> dict[str, Any]:
        """Return SELECT (best flag-free candidate) or REJECT (all flagged)."""
        scored = []
        for c in cands:
            flags = self._check_red_flags(c)
            if flags:
                scored.append({"name": c.name, "flags": flags, "total": None,
                               "factors": {}, "eligible": False})
                continue
            total, factors = self._score(c)
            scored.append({"name": c.name, "flags": [], "total": total,
                           "factors": factors, "eligible": True})
        eligible = [s for s in scored if s["eligible"]]
        if not eligible:
            return {
                "decision": "REJECT",
                "picked": None,
                "confidence": 0.0,
                "candidates": scored,
                "pattern_id": self.patterns[0]["id"],
            }
        best = max(eligible, key=lambda s: s["total"])
        return {
            "decision": "SELECT",
            "picked": best["name"],
            "confidence": best["total"],
            "candidates": scored,
            "pattern_id": self.patterns[0]["id"],
        }

    def decide_from_log(self, log_text: str) -> dict[str, Any]:
        return self.decide(parse_candidates(log_text))


if __name__ == "__main__":
    # smoke test: run the engine on one train log and one test log
    import sys
    ina = INA.load(Path(__file__).resolve().parent / "ina" / "ina_tech_selection_alice_v1.json")
    for path in ["data/train_logs.json", "data/test_logs.json"]:
        logs = json.loads(Path(path).read_text(encoding="utf-8"))
        for entry in logs[:1]:
            r = ina.decide_from_log(entry["log"])
            print(f"{entry['id']}: {r['decision']} {r['picked'] or ''} "
                  f"(conf={r['confidence']:.3f})")
