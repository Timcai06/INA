---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
阶段: 0.4
---

# Phase 0.4 — Portability

> 对应实验：EX-0.4-A（跨模型）、EX-0.4-B（跨 Harness）
> 回答：**RQ4**
> 上游文档：V0.4.1_docs 14-C（Cross-Harness Fidelity）、03（H-Core / H0-Harness）、12（Harness Selection Contract）

## Objective

验证：**Delta 是否脱离模型与 Harness 存在。** 同一个 Delta（同一个 Adaptation Contract）跨模型、跨 Harness，是否产生方向一致的 baseline-relative effect。

> 注意：跨 Harness 比较不是输出相同，而是**方向一致 + 核心行为变化一致 + 作用域一致**（文档 14 第 7 节）。

## Research Question

> RQ4：Behavioral Delta 是否可迁移——跨 Model / Harness / Runtime 保持效果？

反方假设：H0-Harness（Harness 本身就是完整 adaptation state，不需要独立 control-plane representation）；H-Core 否定形式（Delta 绑定模型，换模型即失效）。

## Experiment

**EX-0.4-A — 跨模型**：

- 同一 Delta，3 个模型（不同家族 ≥ 2；具体模型预注册冻结）；
- 每个模型各自采集 Baseline Fingerprint；
- 指标：方向一致率（Direction(Effect_A) ≈ Direction(Effect_B)）、效应保留率（effect size 相对原模型的比例）。

**EX-0.4-B — 跨 Harness**：

- 前置条件：Phase 0.2 未杀死 INA（最高 Kill Gate 通过）；
- 2 个 Harness，各自 realization（realization surface 需存在结构差异，Harness 选择走 ADR，不得提前写死）；
- 指标：cross-harness fidelity（provisional 阈值 0.5，正式实验前冻结）。

## Implementation Scope

- 多模型 run 配置（复用 run 管道，只换 model 参数）；
- 2 个 Harness Adapter（最小实现：仅 realization 注入 + 输出采集）；
- Paired Replay 基础设施（同一输入集跨组回放）；
- Fidelity 指标计算脚本。

## Forbidden Scope

- 4+ 模型或 4+ Harness（那是 Phase 2 的事）；
- 无 Fingerprint 的跨组比较（归因无效）；
- 自行开发 Harness（用现成执行环境，INA 不造 harness）；
- 输出级等同要求（跨 Harness 只要求方向一致）。

## Success Criteria

- 方向一致率 ≥ 0.8，效应保留率 ≥ 0.5（EX-0.4-A）；
- cross-harness fidelity ≥ 0.5 且方向一致（EX-0.4-B）；
- 核心行为变化与作用域在两个 Harness 上一致（文档 14 第 7 节）。

## Kill Criteria

1. 任一模型上方向相反或效应消失（Delta 绑定模型）→ H-Core 否定；
2. fidelity < 0.5（provisional）或两 Harness 方向不一致 → H0-Harness 倾向成立；
3. 每个 Harness 都需要重写 Delta 本体（而非仅 realization）→ C-02 否定（Delta 不可独立表示）。

## Deliverables

```text
Harness Selection ADR（含理由）
3 模型 × 2 Harness 的 Paired Replay 结果
Cross-Model Effect Vector
Cross-Harness Fidelity Report
Baseline Fingerprint 快照（每个环境）
decision-memo.md
```

## 出口门禁

通过 → 进入 Phase 0.5（Evolution Loop）。
失败 → 按 roadmap 7.3 定位：Delta 绑定模型 → Pivot 到 Skill-Centric Evolution（演化对象是 Skill 而非子技能行为）。走 ADR。