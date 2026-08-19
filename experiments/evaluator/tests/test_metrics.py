#!/usr/bin/env python3
"""指标函数自测（手算已知值）。运行：python3 tests/test_metrics.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from metrics_rule import (  # noqa: E402
    accuracy_on, collateral_damage, confusion_shift, flip_rate,
    index_by_id, kappa, label_accuracy, macro_f1,
)
from metrics_regression import (  # noqa: E402
    perturbation_invariance, removal_rollback, run_variance,
)


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def test_label_accuracy():
    rows = [
        {"item_id": "a", "label": "SUPPORT", "gold_label": "SUPPORT"},
        {"item_id": "b", "label": "REFUTE", "gold_label": "SUPPORT"},
        {"item_id": "c", "label": "NEUTRAL", "gold_label": "NEUTRAL"},
    ]
    assert approx(label_accuracy(rows), 2 / 3)
    assert approx(accuracy_on(rows, {"a"}), 1.0)


def test_macro_f1():
    # SUPPORT: tp=1 fp=0 fn=1 -> P=1.0 R=0.5 F1=2/3
    # REFUTE:  tp=1 fp=1 fn=0 -> P=0.5 R=1.0 F1=2/3
    labels = ["SUPPORT", "SUPPORT", "REFUTE"]
    preds = ["SUPPORT", "REFUTE", "REFUTE"]
    assert approx(macro_f1(labels, preds), 2 / 3)


def test_kappa():
    # labels=[A,A,A,B,B], preds=[A,A,B,A,B]
    # Po=3/5=0.6; Pe=0.36+0.16=0.52; kappa=0.08/0.48=0.1666667
    labels = ["A", "A", "A", "B", "B"]
    preds = ["A", "A", "B", "A", "B"]
    assert approx(kappa(labels, preds), 0.1666666667)
    assert approx(kappa(labels, labels), 1.0)


def test_flip_rate():
    base = [
        {"item_id": "1", "label": "SUPPORT", "gold_label": "NEUTRAL"},
        {"item_id": "2", "label": "SUPPORT", "gold_label": "NEUTRAL"},
        {"item_id": "3", "label": "REFUTE", "gold_label": "REFUTE"},
    ]
    delta = [
        {"item_id": "1", "label": "NEUTRAL", "gold_label": "NEUTRAL"},
        {"item_id": "2", "label": "SUPPORT", "gold_label": "NEUTRAL"},
        {"item_id": "3", "label": "REFUTE", "gold_label": "REFUTE"},
    ]
    # 目标项中基线错误 2 条（1、2），翻为 NEUTRAL 1 条 -> 0.5
    assert approx(flip_rate(base, delta, ["1", "2", "3"], "NEUTRAL"), 0.5)
    # 基线无错误项 -> 0.0
    assert approx(flip_rate(base, delta, [], "NEUTRAL"), 0.0)


def test_collateral_damage():
    assert approx(collateral_damage(0.8, 0.75), -5.0)


def test_confusion_shift():
    base = {("SUPPORT", "SUPPORT"): 5, ("NEUTRAL", "SUPPORT"): 2}
    delta = {("SUPPORT", "SUPPORT"): 4, ("NEUTRAL", "NEUTRAL"): 2}
    shift = confusion_shift(base, delta)
    assert shift[("SUPPORT", "SUPPORT")] == -1
    assert shift[("NEUTRAL", "SUPPORT")] == -2
    assert shift[("NEUTRAL", "NEUTRAL")] == 2


def test_run_variance():
    assert approx(run_variance([0.8, 0.8, 0.8]), 0.0)
    # 样本标准差 [0.7, 0.9]: mean=0.8, sd=sqrt(0.02)=0.141421
    assert approx(run_variance([0.7, 0.9]), 0.1414213562)


def test_perturbation_invariance():
    assert approx(perturbation_invariance(0.8, 0.75), 5.0)


def test_removal_rollback():
    base = {"a": "SUPPORT", "b": "SUPPORT"}
    delta = {"a": "NEUTRAL", "b": "SUPPORT"}
    removed = {"a": "SUPPORT", "b": "SUPPORT"}
    # 变化 1 条（a），回退 1 条 -> 1.0
    assert approx(removal_rollback(base, delta, removed), 1.0)
    removed_no = {"a": "NEUTRAL", "b": "SUPPORT"}
    assert approx(removal_rollback(base, delta, removed_no), 0.0)


def test_index_by_id():
    rows = [{"item_id": "x", "label": "A"}, {"item_id": "y", "label": "B"}]
    idx = index_by_id(rows)
    assert set(idx) == {"x", "y"}


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)} tests passed")