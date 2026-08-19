---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
阶段: 0.0
---

# Phase 0.0 — Research Setup

> 对应实验：EX-0.0-1（测量管道校准）
> 上游文档：V0.4.1_docs 09（评测体系）、14（实验方案）、12（路线图）

## Objective

建立实验基础，并证明**测量管道本身可靠**——在开始测量真实 Delta 之前，先证明管道能测出已知变化。这一阶段不产生任何研究结论。

## Research Question

前置问题（测量学问题，不是 INA 研究问题）：

> 我们能否可靠地测量"Agent 行为变化"？（如果连已知注入的变化都测不出，后续一切测量无意义。）

## Experiment

**EX-0.0-1 管道校准**：

1. 构造最小任务（20 条固定判断题）与最小基线（单模型 + 固定 prompt）；
2. 人为注入**已知**行为变化（如：在 prompt 中明确"所有 X 类问题一律回答 NEUTRAL"——变化方向与幅度已知）；
3. 跑完整管道（run → 指标计算 → 报告）；
4. 重复 5 次，检查检出率与假阳性率；
5. 同时校验：Fingerprint 工具能检测配置 drift；隐藏集机制可用。

## Implementation Scope

- 目录约定（`experiments/` 结构与命名）；
- 数据集格式（JSONL schema）与标注协议模板；
- 评测脚本（指标计算：accuracy / macro-F1 / flip rate / kappa / 方差）；
- Fingerprint 采集与 diff 工具（最小 Python）；
- 预注册模板（`runs/preregistration.md`）；
- 单任务 run 脚本骨架。

## Forbidden Scope

- 任何真实 Delta 实验（未校准前不得测真实对象）；
- 多模型、多 Harness、Agent 框架、服务、API、Dashboard；
- 数据集大规模构造（20–40 条校准即可）；
- 数据库与持久化服务（JSONL + git）。

## Success Criteria

- 校准检出率 ≥ 0.95，假阳性 ≤ 0.05（EX-0.0-1 阈值）；
- 相同 seed 重复运行结果完全一致（可复现性基线）；
- Fingerprint 工具能捕获一次故意注入的 drift；
- 预注册机制可用（阈值冻结后 git 历史可审计）。

## Kill Criteria

- 检出率 < 0.8 或假阳性 > 0.2（管道不可信）；
- 同 seed 结果不可复现（环境不可控，任何实验无意义）；
- 无法在一个工作周内搭起最小管道（工具链不可行）。

> Phase 0.0 的 Kill 意味着：**INA 无法被测量，Phase 0 整体结束**（无法测量 = 无法证伪 = 研究不可进行）。

## Deliverables

```text
experiments/ 目录约定 + README
数据格式规范（JSONL schema）
评测脚本（含指标测试）
Fingerprint 工具 + drift 检测测试
预注册模板
EX-0.0-1 校准报告
```

## 出口门禁

Phase 0.0 通过 → 进入 Phase 0.1（Delta Existence）。
Phase 0.0 失败 → 停止或重构测量方案（走 ADR），不得带病进入 0.1。