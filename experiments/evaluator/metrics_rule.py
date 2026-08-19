#!/usr/bin/env python3
"""规则指标（Rule-based Metrics）——主判决依据（01-experiment.md 第 6 节）。

全部为纯函数，可独立测试（tests/test_metrics.py 含手算已知值）。
输入约定：results 为输出 JSONL 的 dict 列表，含
  item_id / arm / label / rationale / gold_label / failure_class / parse_ok
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


# ---------------------------------------------------------------------------
# 输入输出
# ---------------------------------------------------------------------------

def load_outputs(path: str | Path) -> list[dict[str, Any]]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def index_by_id(results: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {r["item_id"]: r for r in results}


def label_accuracy(results: Iterable[dict[str, Any]]) -> float:
    n = sum(1 for r in results if r.get("gold_label") is not None)
    if n == 0:
        return 0.0
    ok = sum(1 for r in results if r.get("label") == r.get("gold_label"))
    return ok / n


# ---------------------------------------------------------------------------
# 核心指标
# ---------------------------------------------------------------------------

def macro_f1(labels: list[str], preds: list[str]) -> float:
    """三标签 macro-F1（对缺失类也计入，避免偏置）。"""
    classes = sorted(set(labels) | set(preds))
    f1s = []
    for c in classes:
        tp = sum(1 for l, p in zip(labels, preds) if l == c and p == c)
        fp = sum(1 for l, p in zip(labels, preds) if l != c and p == c)
        fn = sum(1 for l, p in zip(labels, preds) if l == c and p != c)
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        f1s.append(f1)
    return sum(f1s) / len(f1s) if f1s else 0.0


def kappa(labels: list[str], preds: list[str]) -> float:
    """Cohen's kappa（模型输出 vs 金标准）。"""
    n = len(labels)
    if n == 0:
        return 0.0
    po = sum(1 for l, p in zip(labels, preds) if l == p) / n
    classes = sorted(set(labels) | set(preds))
    pe = sum((labels.count(c) / n) * (preds.count(c) / n) for c in classes)
    if pe >= 1.0:
        return 1.0 if po >= 1.0 else 0.0
    return (po - pe) / (1 - pe)


def flip_rate(
    base_results: Iterable[dict[str, Any]],
    delta_results: Iterable[dict[str, Any]],
    target_items: Iterable[str],
    prescribed_label: str,
) -> float:
    """失败类 flip rate：基线在 target_items 上的错误项中，
    加入 Delta 后翻转为 prescribed_label 的比例。"""
    base = index_by_id(base_results)
    delta = index_by_id(delta_results)
    wrong = [
        i for i in target_items
        if i in base and i in delta
        and base[i].get("gold_label") is not None
        and base[i]["label"] != base[i]["gold_label"]
    ]
    if not wrong:
        return 0.0
    flipped = sum(1 for i in wrong if delta[i]["label"] == prescribed_label)
    return flipped / len(wrong)


def collateral_damage(base_acc: float, delta_acc: float) -> float:
    """附带损伤（pp）：非失败类条目 accuracy 变化。负值 = 退化。"""
    return (delta_acc - base_acc) * 100.0


def accuracy_on(results: Iterable[dict[str, Any]], item_ids: set[str]) -> float:
    """限定条目集上的 accuracy。"""
    subset = [r for r in results if r["item_id"] in item_ids]
    return label_accuracy(subset)


def confusion_matrix(results: Iterable[dict[str, Any]]) -> dict[tuple[str, str], int]:
    """{(gold, pred): count}。"""
    m: dict[tuple[str, str], int] = {}
    for r in results:
        key = (r.get("gold_label"), r["label"])
        m[key] = m.get(key, 0) + 1
    return m


def confusion_shift(
    base: dict[tuple[str, str], int], delta: dict[tuple[str, str], int]
) -> dict[tuple[str, str], int]:
    """标签混淆位移：delta 矩阵相对 base 矩阵的每格变化。"""
    return {k: delta.get(k, 0) - base.get(k, 0) for k in set(base) | set(delta)
            if delta.get(k, 0) != base.get(k, 0)}


def summary(results: Iterable[dict[str, Any]]) -> dict[str, float]:
    """单组结果摘要。"""
    rows = list(results)
    labels = [r.get("gold_label") for r in rows]
    preds = [r["label"] for r in rows]
    return {
        "n": len(rows),
        "accuracy": label_accuracy(rows),
        "macro_f1": macro_f1(labels, preds),
        "kappa": kappa(labels, preds),
    }


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else None
    if not path:
        print("usage: python3 metrics_rule.py <outputs.jsonl>")
        sys.exit(1)
    print(json.dumps(summary(load_outputs(path)), ensure_ascii=False, indent=2))