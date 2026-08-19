# ADR-0004: Out-of-Process Adapter Protocol

- Status: Accepted
- Date: 2026-08-19
- Decision Owners: INA 首席系统架构师 / INA Phase 0 研究组
- Related Research Baseline: V0.4.1（Verified Behavioral Adaptation Control Plane，2026-08-18 冻结）

## Context

Execution Plane 不属于 INA（ADR-0001），因此 INA 与 Agent Runtime / Harness / 工具 之间的
一切能力边界，必须通过**适配器（Adapter）**沟通。如果适配器与 INA 核心同进程耦合，
会造成：语言绑定爆炸（每种 runtime 一个库）、版本撕裂、不可审计、无法沙箱。

## Decision

**INA 核心与 Agent 运行时之间使用 out-of-process, language-agnostic Adapter Protocol。**

- Adapter = 独立进程，实现语言不限（Rust/Python/TS/Go…）；
- INA 通过协议调用 Adapter，Adapter 通过协议回传结果；
- 传输层（Transport）初选：**stdio + NDJSON**（单机最小可用）；
- 后续可扩展 transport（TCP、Unix socket、命名管道），协议层不变；
- 能力面（Capability Surface）最小集：
  `fingerprint` / `realize` / `execute` / `collect` / `cleanup`

## Architecture

```text
INA Control/Conformance Plane
        │  Adapter Protocol (capabilities, request/response, status)
        ▼
┌─────────────────────────────┐
│ Adapter Process (任何语言)    │
│ - fingerprint               │
│ - realize                   │
│ - execute                   │
│ - collect                   │
│ - cleanup                   │
└──────────┬──────────────────┘
           ▼
   Agent Runtime / Harness / Tools
```

### 核心不变式（Invariants）

1. **Adapter 不是 Agent**。Adapter 是 INA 与外部运行时的能力翻译器，不承载 INA 语义；
2. **fingerprint 由 INA 定义，Adapter 负责执行采样**（确定性采样参数由 INA 下发）；
3. **execute 结果必须可收集（collect）、可清理（cleanup）**，不允许副作用泄漏；
4. **协议基于能力声明**：Adapter 上报自己支持的能力，INA 按能力调度；
5. **任何语言都可以实现 Adapter**：语言战略（ADR-0002）只约束 INA 核心，不约束 Adapter。

## Consequences

### Positive

- 解耦：新增一个 Agent 运行时 = 新增一个 Adapter 进程，不改 INA 核心；
- 沙箱与审计：所有能力调用可记录、可校验；
- 实验友好：Phase-0 evaluator 的 `run_agent.py --backend` 结构天然映射到该协议。

### Negative / Trade-offs

- 引入 IPC 开销（单机内可接受，NDJSON 极轻）；
- 适配器协议需要版本化与兼容性管理（未来成本）；
- 多 Adapter 并存时能力面收敛需要纪律。

## Rejected Alternatives

- **进程内库/插件方案**：语言绑定爆炸、无法审计，拒绝；
- **HTTP REST 作为唯一 transport**：本地单机场景过重，且难以流式交互，拒绝（REST 可作未来
  远端 transport 之一，但协议层须保持 transport-agnostic）；
- **MCP 作为唯一标准**：MCP 生态有借鉴价值，但其能力模型（工具调用为中心）不完整覆盖
  fingerprint/collect/cleanup 语义，暂不绑定；未来若 MCP 扩展出完整生命周期能力，可重新评估。

## Revisit Triggers

- 出现需要 INA 核心直接接触 Agent Runtime 的不可调和证据；
- MCP（或类似标准）演进出完整 fingerprint/collect/cleanup 能力模型；
- 分布式执行成为硬需求（此时协议层复用，仅换 transport）。

## Relationship to Phase-0 Experiments

- 实验不需实现完整协议；`run_agent.py --backend` 的 dispatch 结构是协议雏形，予以保留；
- EX-0.1-A 的受控采样参数（seed、temperature、think off）是 fingerprint 能力必须支持的参数子集，
  未来协议要能传输并校验这些参数。
