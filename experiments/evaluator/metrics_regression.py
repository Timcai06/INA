#!/usr/bin/env python3
"""回归指标（Regression Metrics）——稳定性与不变性（01-experiment.md 第 6 节）。

覆盖：run 方差 / 扰动不变性 / Sham 对照差异 / 移除回退。
"""

from __future__ import annotations

import statistics
from typing import Any, Iterable

from metrics_rule import accuracy_on, index_by_id


def run_variance(accuracies: list[float]) -> float:
    """N 次重复 run 的 accuracy 样本标准差（SD）。0 = 完全稳定。"""
    if len(accuracies) < 2:
        return 0.0
    return statistics.stdev(accuracies)


def perturbation_invariance(base_acc: float, delta_acc: float) -> float:
    """扰动不变性（pp）：扰动集 D_pert 上加入 Delta 前后的 accuracy 变化绝对值。"""
    return abs(delta_acc - base_acc) * 100.0


def sham_difference(delta_metric: float, sham_metric: float) -> float:
    """Sham 对照差异：真 Delta 与 Sham 在主指标上的差距（越大越有利）。"""
    return delta_metric - sham_metric


def removal_rollback(
    base_labels: dict[str, str],
    delta_labels: dict[str, str],
    removed_labels: dict[str, str],
) -> float:
    """移除回退率：Delta 改变的条目中，移除 Delta 后回到基线行为的比例。"""
    changed = [
        i for i in delta_labels
        if i in base_labels and delta_labels[i] != base_labels[i]
    ]
    if not changed:
        return 0.0
    reverted = sum(1 for i in changed if removed_labels.get(i) == base_labels[i])
    return reverted / len(changed)


def regression_summary(
    *,
    base_runs: list[Iterable[dict[str, Any]]],
    delta_runs: list[Iterable[dict[str, Any]]],
    pert_items: set[str],
    base_on_pert: Iterable[dict[str, Any]],
    delta_on_pert: Iterable[dict[str, Any]],
    sham_results: Iterable[dict[str, Any]],
    delta_results: Iterable[dict[str, Any]],
) -> dict[str, float]:
    """汇总回归指标（供分析脚本/决策备忘使用）。"""
    base_accs = [accuracy_on(r, {x["item_id"] for x in r}) for r in base_runs]
    delta_accs = [accuracy_on(r, {x["item_id"] for x in r}) for r in delta_runs]
    return {
        "base_run_variance": run_variance(base_accs),
        "delta_run_variance": run_variance(delta_accs),
        "perturbation_invariance_pp": perturbation_invariance(
            accuracy_on(base_on_pert, pert_items), accuracy_on(delta_on_pert, pert_items)
        ),
        "sham_gap": sham_difference(
            accuracy_on(delta_results, {x["item_id"] for x in delta_results}),
            accuracy_on(sham_results, {x["item_id"] for x in sham_results}),
        ),
    }


if __name__ == "__main__":
    import sys

    print("metrics_regression: import-only module（函数见文档字符串）")
    if len(sys.argv) > 1:
        print("usage: python3 metrics_regression.py   # 无 CLI，作为库使用")