---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
阶段: 0.3
---

# Phase 0.3 — Conformance Validation

> 对应实验：EX-0.3-A（判定能力）、EX-0.3-B（回归检测）
> 回答：**RQ3**
> 上游文档：V0.4.1_docs 09（评测体系）、17（Behavioral Conformance 产品楔子）

## Objective

定义并验证：**什么叫"Agent 学会了 Delta"。**

设计 Conformance Score——一个 Delta 携带验证项集合（verification items），Score = 行为与契约声明的符合度。本阶段证明该分数可靠：能区分 delta-present / delta-absent / delta-mutated，并能检测回归。

## Research Question

> RQ3：Behavioral Delta 是否可验证？如何定义"Agent 学会了 Delta"？

反方假设：H0-Eval（普通 accuracy / regression 已足够，conformance 是多余概念，无独立信息量）。

## Experiment

**EX-0.3-A — 判定能力**：

1. 为 Phase 0.1 的 Delta 构建验证项集（每项：输入 + 契约要求的输出，覆盖 activation / invariant / forbidden regression）；
2. 三条件测量：delta-present（G1）/ delta-absent（G0）/ delta-mutated（改字段）；
3. Conformance Score = 验证项符合率（可加权），计算三条件的分数分布与间距。

**EX-0.3-B — 回归检测**：

1. 注入回归场景：冲突 Delta 叠加、Delta 与任务约束冲突、Delta 部分失效；
2. 检查 Conformance Score 是否下降并定位失效项；
3. 与普通 accuracy 对比：conformance 是否提供**独立**信息（信息量增量检验）。

## Implementation Scope

- Conformance Score 定义与计算脚本（v0.1，显式写出公式与加权规则）；
- 验证项集构造工具与记录格式；
- 回归注入脚本（复用 run 管道）；
- 与普通 Eval 的信息量对比分析。

## Forbidden Scope

- 把 Conformance 写成产品服务（本阶段只是测量概念）；
- 多任务泛化宣称（只在证据判断任务族上验证）；
- 无权重理由的加权（每个权重必须有来源：invariant 权重 > effect 权重 > 其他）。

## Success Criteria

- present / absent 分数间距 ≥ 2σ（可区分）；
- mutated 分数落在 absent 侧或显著低于 present（变异可检测）；
- 回归检出率 ≥ 0.9（EX-0.3-B）；
- 分数跨 N=10 run 稳定（SD ≤ 0.05）；
- conformance 相对普通 accuracy 有信息量增量（独立预测失效场景）。

## Kill Criteria

1. 分数无法区分 present / absent（"是否学会"不可判定）→ RQ3 失败；
2. 分数方差过大（SD > 0.1，不可靠）；
3. conformance 与普通 accuracy 完全冗余（H0-Eval 成立，无独立价值——此证据移交 0.2 的 Kill Gate 综合判决）。

## Deliverables

```text
Conformance Score 规范 v0.1（公式 + 加权 + 边界情形）
验证项集（含构造日志与覆盖分析）
EX-0.3-A / EX-0.3-B 结果
与普通 Eval 的冗余度分析
decision-memo.md
```

## 出口门禁

通过 → 进入 Phase 0.4（Portability）。
失败 → RQ3 死亡：若只是分数实现问题可修订重试一次（需 ADR）；若本质不可判定，按 roadmap 7.3 定位 Pivot 到 Evaluation Infrastructure。