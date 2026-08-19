---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
目录性质: 阶段计划目录（方向导航，非设计文档）
---

# research/ — INA Phase 0 阶段计划目录

## 这个目录是什么

本目录是 **INA Phase 0 — Behavioral Evolution Validation** 的研究工程运行导航（Research Engineering Operating Document）。

它的职责只有一个：

> 提示未来所有开发工作的方向：当前阶段要证明什么、怎么证明、什么时候杀死它。

## 这个目录不是什么

| 不是 | 原因 |
|---|---|
| 不是 `V0.4.1_docs/` 的一部分 | v0.4.1 文档基线已冻结（2026-08-18），且文档矩阵明确禁止新增 20、21、22… 编号文档。本目录刻意与 docs 分离，不污染冻结基线。 |
| 不是产品 Roadmap | 不含 UI、PRD、商业模式承诺。 |
| 不是开发计划 | 不承诺具体工期与功能排期，只定义证据门槛。 |
| 不是 Schema / 协议规范 | Schema 的权威仍在 `V0.4.1_docs/02-核心理论与规范/`（04、05）。本目录只决定"先验证什么"。 |
| 不是结果记录 | 实验结果一律写入 `../experiments/`，本目录不保存实验数据。 |

## 两个目录的分工

```text
research/      阶段计划：方向、问题、实验设计、门禁、成败去向   ← 先读这里
experiments/   实验执行：数据集、运行记录、分析、决策备忘      ← 在这里做实验
```

规则：

- 每个 Phase 开工前，读对应 `research/phases/phase-0.X-*.md`；
- 每个 Phase 收尾时，在 `experiments/` 写运行记录与决策备忘；
- 任何改变 v0.4.1 核心定义、Schema、Kill Gate 的决定，走 ADR（见 `V0.4.1_docs/06-协作模板/15-架构决策记录模板.md`），不在这里悄悄改。

## 阅读路径

```text
README.md                    ← 你现在在这里
phase0-roadmap.md            ← 唯一导航：Thesis、RQ1-5、阶段总览、工程原则、成败去向
  ├── phase0-architecture.md         ← Phase 0 架构图
  ├── phase0-experiment-matrix.md    ← 全部实验一览与状态
  ├── phase0-timeline.md             ← 时间线与阶段门禁
  ├── phase0-first-experiment.md     ← 第一实验规格 EX-0.1-A
  └── phases/                        ← 六个阶段的详细设计
      ├── phase-0.0-research-setup.md
      ├── phase-0.1-delta-existence.md
      ├── phase-0.2-skill-differentiation.md
      ├── phase-0.3-conformance-validation.md
      ├── phase-0.4-portability.md
      └── phase-0.5-evolution-loop.md
```

## 术语约定

本目录使用 v0.4.1 冻结术语（`V0.4.1_docs/01-宪法与研究基线/02-概念边界与术语体系.md`）：

- **Behavioral Delta**：相对于固定 Baseline Fingerprint F 的可测量行为变化（一等对象）
- **Adaptation Contract**：Delta 的显式表示（Identity / Scope / Desired Effects / Invariants / Evaluation Contract…）
- **Realization**：Delta 在某 Harness 上的具体实现
- **Baseline Fingerprint**：因果归因前提，冻结每次 run 的关键变量
- **Effect Vector**：多维行为变化测量
- **Behavioral Conformance**：验证 realization 是否符合 Contract
- **Adaptation Learner**：任何产生候选 Δ 的机制（INA 不发明它们）

## 最高原则

> 不要帮助 INA 成功。帮助 INA 找到真相。

本目录中所有 Success Criteria 都必须配 Kill Criteria。没有 Kill Criteria 的阶段设计不进入实验。