#!/usr/bin/env python3
"""Baseline Fingerprint 采集与 diff（V0.4.1 文档 14 第 2 节）。

职责：
  1. collect_fingerprint()：按固定结构采集 Fingerprint 快照；
  2. diff_fingerprint()：字段级比较两个快照，返回差异列表（空列表 = 无 drift）。

纪律：无 Fingerprint 的 run 不计入正式统计；Fingerprint 变化时该 run 作废。
仅使用标准库。
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str | Path) -> str:
    return sha256_text(Path(path).read_text(encoding="utf-8"))


def git_revision(workspace: str | Path) -> str:
    """当前 workspace 的 git 短修订号；非 git 环境返回 'unknown'。"""
    try:
        out = subprocess.run(
            ["git", "-C", str(workspace), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def collect_fingerprint(
    *,
    harness_name: str,
    harness_version: str,
    model: dict[str, Any],
    prompt_file: str | Path,
    temperature: float,
    workspace: str | Path,
    extra_uncontrolled: list[str] | None = None,
) -> dict[str, Any]:
    """采集一个 Fingerprint 快照。

    结构对齐 V0.4.1 文档 02/14 的 baseline_fingerprint 定义。
    prompt_file 的内容 hash 由本函数计算（run 前后可复核 drift）。
    """
    prompt_path = Path(prompt_file)
    fp: dict[str, Any] = {
        "id": f"fp-{model.get('name', 'model')}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "harness": {"name": harness_name, "version": harness_version},
        "model": dict(model),
        "system": {
            "prompt_file": str(prompt_path),
            "prompt_sha256": sha256_file(prompt_path),
        },
        "tools": {"enabled": []},
        "permissions": {"profile": "none"},
        "skills": {"enabled": []},
        "memory": {"mode": "none"},
        "runtime": {"temperature": float(temperature), "max_steps": 1},
        "environment": {"workspace_revision": git_revision(workspace)},
        "uncontrolled_variables": list(extra_uncontrolled or []),
    }
    return fp


def diff_fingerprint(a: dict[str, Any], b: dict[str, Any]) -> list[str]:
    """字段级 diff；返回形如 'system.prompt_sha256: abc -> def' 的差异列表。"""
    changed: list[str] = []

    def walk(x: dict[str, Any], y: dict[str, Any], prefix: str = "") -> None:
        for k in sorted(set(x) | set(y)):
            p = f"{prefix}.{k}" if prefix else k
            if k not in x:
                changed.append(f"{p}: added {y[k]!r}")
            elif k not in y:
                changed.append(f"{p}: removed {x[k]!r}")
            elif isinstance(x[k], dict) and isinstance(y[k], dict):
                walk(x[k], y[k], p)
            elif x[k] != y[k]:
                changed.append(f"{p}: {x[k]!r} -> {y[k]!r}")

    walk(a, b)
    return changed


def write_snapshot(fp: dict[str, Any], out_dir: str | Path) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "baseline_fingerprint.yaml"
    path.write_text(_to_yaml(fp), encoding="utf-8")
    return path


def _to_yaml(fp: dict[str, Any]) -> str:
    """极简 YAML 序列化（仅本项目的嵌套 dict/list/标量结构）。"""
    lines = ["baseline_fingerprint:"]

    def emit(d: dict[str, Any], indent: int) -> None:
        pad = "  " * indent
        for k, v in d.items():
            if isinstance(v, dict):
                lines.append(f"{pad}{k}:")
                emit(v, indent + 1)
            elif isinstance(v, list):
                if v:
                    lines.append(f"{pad}{k}:")
                    for item in v:
                        lines.append(f"{pad}  - {json.dumps(item, ensure_ascii=False)}")
                else:
                    lines.append(f"{pad}{k}: []")
            else:
                lines.append(f"{pad}{k}: {json.dumps(v, ensure_ascii=False)}")

    emit(fp, 1)
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    # 自检：采集 + 故意 drift + diff
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        prompt = tmp_path / "prompt.txt"
        prompt.write_text("v1", encoding="utf-8")
        model = {"provider": "mock", "name": "mock-judge", "version": "0.1.0"}
        fp1 = collect_fingerprint(
            harness_name="python-runner", harness_version="0.1.0",
            model=model, prompt_file=prompt, temperature=0, workspace=tmp_path,
        )
        prompt.write_text("v2", encoding="utf-8")  # 故意 drift
        fp2 = collect_fingerprint(
            harness_name="python-runner", harness_version="0.1.0",
            model=model, prompt_file=prompt, temperature=0, workspace=tmp_path,
        )
        diffs = diff_fingerprint(fp1, fp2)
        assert any("prompt_sha256" in d for d in diffs), diffs
        print("fingerprint self-check OK; diff sample:")
        for d in diffs:
            print(f"  {d}")