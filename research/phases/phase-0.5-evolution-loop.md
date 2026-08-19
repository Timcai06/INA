---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
阶段: 0.5
---

# Phase 0.5 — Evolution Loop

> 对应实验：EX-0.5-A（闭环单环可行性）
> 回答：**RQ5**
> 上游文档：V0.4.1_docs 06（提取编译执行与学习闭环）、08（谱系与回滚）、03（H5；v0.4.1 将自动进化降级为远期）

## Objective

验证：**Agent 是否可以持续进化——trajectory → delta → verification 的闭环是否成立。**

**范围纪律**：v0.4.1 明确"无人工门禁的自动 Evolution"不在本阶段。Phase 0.5 只验证**人工主导、机器验证**的单环可行性：失败轨迹能否成为 Delta 的来源，Delta 能否被验证、采纳、版本化，回归能否被检测、回滚能否执行。不构建自治学习系统。

## Research Question

> RQ5：Behavioral Delta 是否可以形成生命周期——trajectory → failure → delta → evaluation → adoption → version → rollback？

反方假设：H5 否定形式（提取必须完全人工，Delta 无法从经验中获益）；H0-D（Delta 无法稳定组合，多 Delta 冲突）。

## Experiment

**EX-0.5-A — 闭环单环可行性**（科研证据判断任务族，2 代）：

1. **第 1 代**：运行 Agent 于任务套件 → 收集轨迹 → 识别失败（规则 + 人工）→ 人工主导提取 Delta v1 → Conformance 验证（Phase 0.3 工具）→ 采纳 + 版本化（git 级 registry）→ 重跑任务套件；
2. **回归演练**：人为注入冲突 Delta（v1.1，含错误字段）→ Conformance 检测下降 → 回滚到 v1；
3. **第 2 代**：在 v1 基线上重复提取 → Delta v2 → 验证采纳 → 重跑；
4. 记录每代 Conformance 的单调性、每次操作的 provenance（谁、何时、依据什么证据）。

## Implementation Scope

- 轨迹收集与失败标注工具（最小）；
- Delta 提取辅助脚本（人工主导：脚本做统计提示，人做决策）；
- 本地 git 级 Delta Registry 约定（文件命名 + 版本 + lineage 字段）；
- 回滚演练脚本（复用 run 管道）；
- 演化日志模板（每代：来源轨迹 → 决策理由 → 验证结果）。

## Forbidden Scope

- 自动 Delta 提取 / 自治演化（无人工门禁）——v0.4.1 明确远期；
- Registry 服务 / 数据库（git + 文件约定足够）；
- 多任务族泛化（只验证证据判断单族闭环）；
- 任何"进化成功"的营销式表述（只记录数字）。

## Success Criteria

- **≥ 2 代连续改进**：每代 Conformance 相对上一代单调不降，且第 2 代有实际提升；
- **回滚成功率 1.0**：注入回归 → 检测 → 回滚 → 行为恢复（回滚后 conformance 回到 v1 水平）；
- 提取的 Delta 均能通过 Phase 0.3 验证（提取物不是垃圾）；
- 生命周期每步有 provenance 记录（可审计）。

## Kill Criteria

1. 无法从失败轨迹提取出任何通过验证的 Delta（提取机制不成立，H5 否定）；
2. 第 2 代无提升且无合理解释（进化不收敛）；
3. 回滚失败或回滚后行为未恢复（治理承诺不成立）；
4. 多 Delta 叠加导致冲突失控（H0-D 倾向成立，组合不可行）。

## Deliverables

```text
2 代演化完整日志（trajectory → delta → verify → version → rollback）
Delta Registry 示例（v1 / v1.1 冲突 / v2，含 lineage）
Conformance 逐代曲线
回滚演练报告
evolution-loop-summary.md：RQ5 判决
Phase 0 综合报告输入
```

## 出口门禁

通过 → **Phase 0 成功**：汇总 RQ1–RQ5 证据 → 综合报告 + ADR（继续 → roadmap 7.2 的 Phase 1；或修正范围）。
失败 → **Phase 0 失败**：按 roadmap 7.3 定位 Pivot（闭环不成立 → 降级为"验证即价值"定位：Delta 作为可验证配置单元，不承诺进化），走 ADR。

## 本阶段与 v0.4.1"远期 Evolution"的关系

```text
v0.4.1 远期：无人工门禁的自动 Evolution（H5 全量）
Phase 0.5 只验证：人工主导提取 + 机器验证 + 版本化 + 回滚（H5 可行性子集）

若 Phase 0.5 通过 → 自动 Evolution 才有资格进入后续研究议程
若 Phase 0.5 失败 → 自动 Evolution 从议程中删除
```