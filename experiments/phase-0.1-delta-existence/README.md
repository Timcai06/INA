---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
实验ID: EX-0.1-A
规格来源: research/phase0-first-experiment.md
---

# experiments/phase-0.1-delta-existence/ — 实验协议

## 本目录对应

- 规格：[`../../research/phase0-first-experiment.md`](../../research/phase0-first-experiment.md)（唯一权威）
- 阶段设计：[`../../research/phases/phase-0.1-delta-existence.md`](../../research/phases/phase-0.1-delta-existence.md)

## 目录布局

```text
data/
├── annotation-protocol.md   # 标注协议（先于数据冻结）
├── dev.jsonl                # D_dev 40 条（失败识别用）
├── test.jsonl               # D_test 60 条（隐藏集，预注册前不暴露）
└── pert.jsonl               # D_pert 20 条（扰动不变性）
runs/
├── preregistration.md       # 预注册：阈值冻结 + 隐藏集 hash + 统计约定
└── run-<NNN>/               # 每次 run
    ├── baseline_fingerprint.yaml   # Fingerprint 快照
    ├── contract.yaml + contract.sha256  # 所用 Delta + hash
    ├── inputs.jsonl / outputs.jsonl   # 输入输出
    └── notes.md                     # 环境备注 / uncontrolled variables
analysis/
├── metrics.csv              # 全部指标汇总
├── confusion-matrix.png     # 标签位移
├── delta-consistency-review.md  # 人工盲评记录
└── decision-memo.md         # Go / No-Go 判决
```

## 本实验三组配置

| 组 | 配置 | 用途 |
|---|---|---|
| G0 | Baseline prompt 模板 v1 | 主比较基准 |
| G1 | G0 + 结构化 Adaptation Contract 注入 | 主处理组 |
| G2 | G0 + 等量自然语言改写（非结构化） | 健全性对照 |

三组共享同一 Baseline Fingerprint；G1 与 G0 的唯一差异是注入块。

## 开工清单（进入正式实验前逐项打勾）

- [ ] `data/annotation-protocol.md` 冻结（先于数据）
- [ ] D_dev 40 条构造并标注完成
- [ ] 基线运行 N=10，识别实测失败模式（选定 Delta 靶点）
- [ ] Adaptation Contract 定稿（`contract.yaml` + hash）
- [ ] `runs/preregistration.md` 冻结全部阈值 + 隐藏集 hash（git commit）
- [ ] D_test / D_pert 标注完成且未暴露给模型
- [ ] 正式评估 run 执行（N=10 × 3 组）
- [ ] 人工盲评（2 名评员，kappa ≥ 0.7）
- [ ] `analysis/decision-memo.md` 产出判决

## 纪律

- 预注册后不得修改阈值；
- 任何 run 缺失 Fingerprint 即作废；
- 负面结果与正面结果同等记录。