#!/usr/bin/env python3
"""行为指标（Behavior Metrics）——Effect Vector 与文本级信号（01-experiment.md 第 6 节）。

注意：证据引用密度与理由一致性是**启发式近似**，仅作参考信号；
主判决仍以规则指标 + 人工盲评为准。
"""

from __future__ import annotations

import re
from typing import Any, Iterable

from metrics_rule import index_by_id

# Delta 对失败模式的指定标签（01-experiment.md 第 4 节；以契约定稿为准）
PRESCRIBED = {
    "context_mismatch": "NEUTRAL",
    "correlation_as_causation": "NEUTRAL",
    "insufficient_evidence": "NEUTRAL",
    "contradiction_softening": "REFUTE",
}

_LABEL_SYNONYMS = {
    "SUPPORT": ["支持", "一致", "证实", "吻合"],
    "REFUTE": ["反驳", "反对", "否定", "不支持", "矛盾", "相悖"],
    "NEUTRAL": ["中性", "无法判断", "不足以", "不确定", "无法确定"],
}

_NUM_RE = re.compile(r"[0-9]+%?|显著|p\s*[<≤=≥]\s*0?\.?\d*")


def rationale_label_consistency(results: Iterable[dict[str, Any]]) -> float:
    """理由一致性：理由文本中出现与标签同义的关键词的比例（启发式）。"""
    rows = list(results)
    if not rows:
        return 0.0
    ok = 0
    for r in rows:
        syns = _LABEL_SYNONYMS.get(r["label"], [])
        if any(s in r.get("rationale", "") for s in syns):
            ok += 1
    return ok / len(rows)


def evidence_citation_density(results: Iterable[dict[str, Any]]) -> float:
    """证据引用密度：每条理由中数字/统计信号的平均数量（启发式）。"""
    rows = list(results)
    if not rows:
        return 0.0
    total = sum(len(_NUM_RE.findall(r.get("rationale", ""))) for r in rows)
    return total / len(rows)


def support_precision(results: Iterable[dict[str, Any]]) -> float:
    """SUPPORT 精确率：预测 SUPPORT 中金标准为 SUPPORT 的比例。"""
    rows = list(results)
    pred_support = [r for r in rows if r["label"] == "SUPPORT"]
    if not pred_support:
        return 0.0
    tp = sum(1 for r in pred_support if r.get("gold_label") == "SUPPORT")
    return tp / len(pred_support)


def neutral_appropriateness(results: Iterable[dict[str, Any]]) -> float:
    """NEUTRAL 恰当性：金标准为 NEUTRAL 的条目上的准确率。"""
    rows = [r for r in results if r.get("gold_label") == "NEUTRAL"]
    if not rows:
        return 0.0
    ok = sum(1 for r in rows if r["label"] == "NEUTRAL")
    return ok / len(rows)


def disconfirmation_reporting(results: Iterable[dict[str, Any]]) -> float:
    """反驳报告：金标准为 REFUTE 的条目上输出 REFUTE 的比例（REFUTE recall）。"""
    rows = [r for r in results if r.get("gold_label") == "REFUTE"]
    if not rows:
        return 0.0
    ok = sum(1 for r in rows if r["label"] == "REFUTE")
    return ok / len(rows)


def effect_vector(
    base_results: Iterable[dict[str, Any]],
    delta_results: Iterable[dict[str, Any]],
) -> dict[str, float]:
    """Effect Vector：各失败模式的 flip rate + 三个行为维度。

    flip 定义：基线错误 → Delta 改为该模式指定标签。
    """
    base = index_by_id(base_results)
    delta = index_by_id(delta_results)
    vec: dict[str, float] = {}
    for fc, prescribed in PRESCRIBED.items():
        items = [i for i in base if base[i].get("failure_class") == fc]
        wrong = [
            i for i in items
            if base[i].get("gold_label") is not None
            and base[i]["label"] != base[i]["gold_label"]
            and delta[i]["label"] == prescribed
        ]
        vec[f"flip_{fc}"] = len(wrong) / len(items) if items else 0.0
    vec["support_precision"] = support_precision(delta_results)
    vec["neutral_appropriateness"] = neutral_appropriateness(delta_results)
    vec["disconfirmation_reporting"] = disconfirmation_reporting(delta_results)
    return vec


if __name__ == "__main__":
    import json
    import sys

    from metrics_rule import load_outputs

    if len(sys.argv) < 3:
        print("usage: python3 metrics_behavior.py <base.jsonl> <delta.jsonl>")
        sys.exit(1)
    vec = effect_vector(load_outputs(sys.argv[1]), load_outputs(sys.argv[2]))
    print(json.dumps(vec, ensure_ascii=False, indent=2))