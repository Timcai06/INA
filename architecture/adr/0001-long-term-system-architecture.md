# ADR-0001: Long-Term System Architecture

- Status: Accepted
- Date: 2026-08-19
- Decision Owners: INA 首席系统架构师 / INA Phase 0 研究组
- Related Research Baseline: V0.4.1（Verified Behavioral Adaptation Control Plane，2026-08-18 冻结）

## Context

Phase-0 实验代码目前是纯 Python + 文件系统的轻量管道。存在两种长期路线：
A) "先快速 Python MVP，未来整体重构正式系统"（Disposable MVP）；
B) 现在就冻结长期分层架构，实验代码与生产架构在逻辑边界上对齐，但不要求实验期实现生产组件。

路线 A 的风险：实验证明的语义（Behavioral Delta、Fingerprint、Conformance）在重构中丢失或变形，
且"快速 MVP"的领域对象边界随意，导致未来架构从实验结果中无法追溯。

## Decision

**INA 不采用 Disposable MVP Architecture 路线。**

> INA 不采用"先快速做一个 Python MVP，未来再整体重构正式系统"的工程路线。

Python 仍然允许并鼓励用于 Phase-0 research experiments、evaluation、benchmark、data analysis 和 research tooling。

```text
Research implementation ≠ Production architecture
```

## Architecture

### 长期分层

```text
Adaptation Learners
        │
        ▼
Candidate Behavioral Delta
        │
        ▼
┌────────────────────────────┐
│     INA Control Plane      │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│   INA Conformance Plane    │
└─────────────┬──────────────┘
              │
              ▼
        Adapter Protocol
              │
              ▼
┌────────────────────────────┐
│   Agent Execution Plane    │
│ Harness / Tools / Memory   │
│ Model / Runtime            │
└────────────────────────────┘
```

- **Control Plane** 拥有：Adaptation Contract、Behavioral Delta semantics、Scope、Invariants、
  Evaluation Contract、Approval、Revocation、Rollback、Version、Lineage、Cognitive State。
- **Conformance Plane** 拥有：Baseline Fingerprint、Paired Replay、Effect Extraction、Evaluation、
  Regression、Conformance、Validation Artifact。
- **Execution Plane 不属于 INA**。它属于 Codex / Claude Code / OpenCode / Future Harness / Custom
  enterprise agent。INA 不重新实现 Agent Runtime。

### 长期核心模块（逻辑边界，非物理包）

```text
ina-core
ina-schema
ina-artifact
ina-lineage
ina-fingerprint
ina-conformance
ina-runner
ina-adapter-protocol
ina-cli
ina-registry
```

> 逻辑模块边界先冻结，物理 package / crate 拆分以后可以调整。

## Consequences

### Positive

- 实验期产出的领域对象（契约、指纹、运行记录）与长期系统使用同一逻辑边界，未来可追溯、可迁移；
- "Execution Plane 不属于 INA" 防止重复造 Agent Runtime，与 ADR-0004 适配器协议互相支撑；
- 分层不阻碍 Phase-0：本 ADR 冻结的是方向，不是要求实验期实现全部组件。

### Negative / Trade-offs

- 实验代码需要付出少量成本保持领域对象边界清晰（不能"随手写个 dict 就完事"）；
- "不采用 Disposable MVP" 意味着未来重构无法以"反正要重写"为由丢弃实验语义。

## Rejected Alternatives

- **Disposable MVP（先 Python 全栈，后整体重写）**：实验语义丢失风险高，拒绝。
- **实验期即启动完整分层实现**：与 Phase-0"只做可行性判决"目标冲突，拒绝（见 ADR-0002/0003 的边界）。

## Revisit Triggers

- 实验证明 Behavioral Delta 概念不成立（STOP）：整个 Control/Conformance 分层失去存在理由；
- Phase-0 实验暴露出与分层假设不可调和的行为学事实（例如 Delta 无法与 Harness 解耦）。

## Relationship to Phase-0 Experiments

- 本 ADR 与 EX-0.1-A 无直接依赖；实验可在本 ADR 生效下照常进行；
- 实验结论（尤其是 Delta 载体形式：判断准则式 vs 触发器式）将直接影响 Control Plane 的契约语义设计；
- 若实验 PIVOT，本 ADR 保留为历史记录，新方向以新 ADR 或修订版记录。
