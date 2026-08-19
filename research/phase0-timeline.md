---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
---

# Phase 0 Timeline

> 时间线是**指示性**的（indicative），不是承诺。真正的推进由证据门槛决定（文档 12 第 1 节）。
> 周次以人工主导节奏估算，单人兼职约 15 周，全职可压缩到 8–10 周。

## 总览

```text
W1  W2  W3  W4  W5  W6  W7  W8  W9  W10 W11 W12 W13 W14 W15
|--0.0--||----0.1----||--0.2--||-----0.3-----||--0.4--||----0.5----|
  Setup   Existence    Diff     Conformance    Port     Evolution
```

## 逐阶段

| 阶段 | 周次 | 关键活动 | 出口（Gate） |
|---|---|---|---|
| 0.0 Research Setup | W1–2 | 仓库约定、数据格式、评测脚本、Fingerprint 工具、EX-0.0-1 管道校准 | 测量管道通过校准；eval 框架 + 数据集工具可用 |
| 0.1 Delta Existence | W3–5 | 构造科研证据判断数据集（人工标注）、基线失败识别、Delta 编写、EX-0.1-A 主实验、EX-0.1-B 移除/变异 | RQ1 判决：Go / No-Go |
| 0.2 Skill Differentiation | W6–7 | 四臂对照（Prompt/Skill/Memory/Delta）、信息量控制、治理维度评测 | **最高 Kill Gate**：H0-Skill 是否成立 |
| 0.3 Conformance Validation | W8–10 | Conformance Score 设计、验证项集、EX-0.3-A/B | RQ3 判决：可验证性 |
| 0.4 Portability | W11–12 | 跨模型（3 模型）、跨 Harness（2 Harness，须 Harness Selection ADR） | RQ4 判决：可迁移性 |
| 0.5 Evolution Loop | W13–15 | 单环闭环、2 代改进、回滚演练 | RQ5 判决：闭环可行性 |
| 收尾 | W15+ | Phase 0 综合报告、ADR（继续 / Pivot / Stop） | 决策落地 |

## 门禁规则

1. 每个阶段出口是一次 **Gate Review**：对照该阶段预注册阈值，产出 Go / No-Go / Pivot 备忘；
2. No-Go 不自动等于项目停止——按 [roadmap 7.3](phase0-roadmap.md) 的失败点定位 Pivot 方向，走 ADR；
3. 时间超出指示范围**不构成失败**；证据不足才构成失败；
4. 任何阶段提前完成，可以提前进入下一阶段，但**不得跳过**。

## 当前状态

```text
Phase 0.0: 未开始（本路线图冻结后开工）
本周定位:  W0 — 研究程序建立
```