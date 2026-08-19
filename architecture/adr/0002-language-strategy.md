# ADR-0002: Language Strategy

- Status: Accepted
- Date: 2026-08-19
- Decision Owners: INA 首席系统架构师 / INA Phase 0 研究组
- Related Research Baseline: V0.4.1（Verified Behavioral Adaptation Control Plane，2026-08-18 冻结）

## Context

Phase-0 实验代码为 Python（纯 stdlib，无第三方依赖），运行良好。需要确定长期语言边界，
避免三种错误：a) 实验期禁止使用未来核心语言；b) 实验代码变成无边界混沌；c) 实验期提前大规模实现生产语言组件。

## Decision

**Rust 是 INA 的长期核心工程语言。**

- **Rust** 长期负责：INA Core、CLI、Artifact identity、Canonicalization、Hashing、Fingerprint、
  Contract validation、Lineage、Conformance infrastructure、Local runtime infrastructure、Protocol implementation。
- **Python** 负责：Phase-0 experiments、Evaluators、Benchmarks、Statistical analysis、Research tooling、
  Dataset preparation、Experimental adapters、Exploratory code。
- **TypeScript** 未来负责：Web Console、Product Surface、Frontend、可能的 SDK。
  但目前：**DO NOT IMPLEMENT PRODUCT UI**。

## Architecture

```text
长期核心（Rust）: ina-core / ina-cli / ina-fingerprint / ina-conformance / 协议实现
研究层（Python）: experiments/ / evaluator / benchmark / dataset / 统计分析
产品面（TS，未来）: Web Console / SDK（未实现）
```

### 重要原则

- **不要现在启动大规模 Rust 实现**。本 ADR 决定长期架构语言战略，不是要求 Phase-0 立即 Rust 化；
- Python 实验代码**不是 disposable chaos**：即使是实验代码，也必须遵守正式领域对象边界
  （与 ADR-0001 的逻辑模块一致）；
- 语言切换点（何时开始 Rust）由 Phase-0 判决结果驱动，不由工程偏好驱动。

## Consequences

### Positive

- 核心语义（hash/fingerprint/contract validation/lineage）获得 Rust 的强类型与正确性保证；
- 研究层保持 Python 的迭代速度；实验与生产语言边界清晰，互不拖累；
- 明确禁止现在 Rust 化，保护实验节奏。

### Negative / Trade-offs

- 未来存在一次 Rust 核心实现成本（但按 ADR-0001，不是"重写"，而是按既定边界实现）；
- Python 实验代码需要在边界纪律上投入少量维护成本；
- 双语言长期并存增加工具链复杂度。

## Rejected Alternatives

- **全 Python 长期方案**：核心正确性（hash、并发、协议）与长期维护成本不可接受；
- **全 Rust 从实验第一天开始**：拖慢 Phase-0 判决速度，违反"实验优先"原则；
- **Go 作为核心语言**：类型系统与生态对协议/artifact 基础设施不如 Rust 贴合，暂不采纳
  （但 Adapter 实现语言不受限，见 ADR-0004）。

## Revisit Triggers

- Phase-0 实验证明核心语义比预期简单（例如 Delta 被简化到纯文本变换），Rust 层收益不成立；
- 团队生态出现显著变化（无 Rust 工程能力时重新评估）；
- 实验 PIVOT 到全新架构方向时，语言战略随新方向整体重评。

## Relationship to Phase-0 Experiments

- 实验继续使用 Python，不受本 ADR 约束；
- EX-0.0-1 已证明的确定性（seed+temp0 可复现）是未来 Rust 实现必须保持的语义，写入 ADR-0006。
