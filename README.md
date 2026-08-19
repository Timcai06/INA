# INA — Verified Behavioral Adaptation Control Plane

**Phase 0 — Behavioral Evolution Validation**：为 Behavioral Delta 的存在性、区分性、可验证性、可迁移性、生命周期收集证据（RQ1–RQ5）。

## 目录导航（一眼看懂）

| 目录 | 是什么 | 性质 |
|---|---|---|
| `V0.4.1_docs/` | 冻结研究基线：定义 INA 要证明什么 | immutable，不改 |
| `phase0-research/` | Phase 0 研究导航：路线图、实验规格、阶段计划 | 方向导航，开工前读 |
| `experiments/` | Phase 0 实验现场：数据集、evaluator、Delta、结果与判决 | 实验执行，收尾时写 |
| `architecture/` | 长期工程架构决策（ADR 索引） | 演化中的工程决策 |
| `ina_engine.py` | 早期原型 | 非架构先例（见 architecture/adr/0001） |

## 规则速记

- 实验结论不得直接修改 `V0.4.1_docs/` 与 `phase0-research/` 中的设计；改方向走 ADR；
- 每个实验 run 必须满足 `experiments/README.md` 的运行协议（预注册、fingerprint、固定 seed、隐藏集纪律）；
- no push ≠ no commit（ADR-0006）。
