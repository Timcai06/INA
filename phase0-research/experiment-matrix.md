---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
---

# Phase 0 Experiment Matrix

> 实验编号约定：`EX-0.<Phase>.<序号>`。状态：`planned / running / passed / failed / killed`。
> 所有阈值均为 **Phase-0 preregistered provisional thresholds**（文档 12 第 1 节），正式实验前冻结，不得事后修改。

## 实验矩阵

| ID | Phase | 回答 | 设计要点 | 主要指标 | 成功阈值（provisional） | 失败阈值（provisional） | 状态 |
|---|---|---|---|---|---|---|---|
| EX-0.0-1 | 0.0 | 测量管道能否检测已知变化 | 注入已知行为变化（gold 已知），跑全管道 | 检出率 / 假阳性率 | 检出率 ≥ 0.95，假阳性 ≤ 0.05 | 检出率 < 0.8 或假阳性 > 0.2 | planned |
| EX-0.1-A | 0.1 | Delta 是否产生稳定行为变化 | 科研证据判断；G0 baseline vs G1 baseline+delta vs G2 prompt-paraphrase | 失败类 flip rate、类内 accuracy、macro-F1 | flip rate ≥ 0.6 且失败类 accuracy 提升 ≥ 20pp 且附带损伤 ≤ 5pp 且 run 方差 ≤ 3pp | 无显著差异，或附带损伤 > 20pp，或方差 > 5pp | planned |
| EX-0.1-B | 0.1 | 移除 / 变异是否可预测 | Removal Test + Mutation Test（文档 14 14-A） | 移除后行为回退率、变异方向一致性 | 移除回退率 ≥ 0.6；变异导致方向可预测变化 | 移除无回退；变异无规律 | planned |
| EX-0.2-A | 0.2 | Delta ≠ Prompt / Skill / Memory | 四臂对照：同一行为意图，四种载体（等量信息、等长、同 Fingerprint） | 效果幅度、特异性、稳定性、可编辑性、可审计性（多维） | Delta 在 ≥ 1 个治理维度显著优于全部对手，且效果不劣 | H0-Skill 成立：Skill+Eval 完全等价或更优 | planned |
| EX-0.3-A | 0.3 | Conformance Score 能否判定生效 | 为 Delta 定义验证项集；delta-present vs delta-absent vs delta-mutated | conformance 区分度、稳定性 | present/absent 间距 ≥ 2σ，mutated 落在 absent 侧 | 分数无法区分 present/absent | planned |
| EX-0.3-B | 0.3 | Conformance 能否检测回归 | 注入回归（delta 冲突 / 退化），观察 conformance 下降 | 回归检出率 | 检出率 ≥ 0.9 | 检出率 < 0.6 | planned |
| EX-0.4-A | 0.4 | Delta 是否跨模型保持 | 同一 Delta，3 个模型（含不同家族） | 方向一致率、效应保留率 | 方向一致 ≥ 0.8，效应保留 ≥ 0.5 | 任一模型方向相反或效应消失 | planned |
| EX-0.4-B | 0.4 | Delta 是否跨 Harness 保持 | 同一 Delta，2 个 Harness realization（文档 14 14-C / Harness Selection ADR） | cross-harness fidelity | fidelity ≥ 0.5（provisional，正式实验前冻结） | fidelity < 0.5 或方向不一致 | planned |
| EX-0.5-A | 0.5 | 闭环单环是否可行 | trajectory → failure → delta（人工主导）→ conformance → version → 注入回归 → rollback，2 代 | 每代 conformance 单调性、回滚成功率 | ≥ 2 代连续改进；回滚成功率 1.0 | 无法从经验改进；回滚失败 | planned |

## 门禁链

```text
EX-0.0-1 → EX-0.1-A → EX-0.1-B → EX-0.2-A → EX-0.3-A → EX-0.3-B → EX-0.4-A → EX-0.4-B → EX-0.5-A
   │          │          │          │          │          │          │          │          │
   └── 任一失败 → 该 Phase Kill Gate 触发 → 按 roadmap 7.3 的失败点定位 Pivot（走 ADR）
```

## 冻结规则

1. 每个实验开工前，将阈值写入 `experiments/phase-0.X-*/runs/preregistration.md` 并 git commit；
2. 实验过程中不得修改已冻结阈值；
3. 隐藏集在冻结阈值前不得被模型或人看过；
4. 每个 run 必须附带 Baseline Fingerprint 快照；
5. 负面结果与正面结果同权记录。