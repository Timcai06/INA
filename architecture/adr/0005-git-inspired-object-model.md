# ADR-0005: Git-Inspired Object Model

- Status: Accepted
- Date: 2026-08-19
- Decision Owners: INA 首席系统架构师 / INA Phase 0 研究组
- Related Research Baseline: V0.4.1（Verified Behavioral Adaptation Control Plane，2026-08-18 冻结）

## Context

INA 要追踪 Behavioral Delta 的生命周期：谁提出、基于哪个 Baseline、内容如何规范化为精确证据、
被批准或否决、如何回滚、如何溯源。如果状态是"数据库里一行可变记录"，则任何修改都会丢失证据。

## Decision

**INA 的领域对象采用 Git-inspired object model。**

- 采纳 Git 的核心思想，但**不是克隆 Git**：
  - **Content-addressed immutable objects**：对象内容 → 规范化 → 哈希（digest）→ 作为身份；
  - **Mutable refs**：指针（引用）可变，指向特定 digest；refs 是唯一可变点；
  - **Lineage**：每个对象记录 parent digest，形成可回溯链；
  - **Commits 作为状态变化的最小单元**：批准、否决、回滚、升级都是新 commit，不是改写历史。
- **Cognitive State 不是简单数组**：Cognitive State 的组合/派生是 INA 独有的领域语义，
  其组合规则必须显式定义并验证，**禁止用"对象数组累加"含糊表达**；
- 大制品不进入对象树（见 ADR-0003 Artifact Store），对象引用其 digest。

## Architecture

```text
Refs (mutable) ──► Commits (immutable) ──► Content Objects (immutable, digest-addressed)
                       │
                       └──► Lineage: parent chain, 可回溯任何历史状态
```

典型对象：`AdaptationContract` / `BehavioralDelta` / `BaselineFingerprint` / `EvalRun` /
`ConformanceResult` / `Approval` / `Revocation`。

## Consequences

### Positive

- 每次行为变化可审计、可回滚、可推导"从哪个 Baseline 演进而来"；
- Content-addressing 天然支持并发（多个提案互不覆盖）与去重；
- 与 ADR-0003 契合：PG 存 refs/index，对象/制品存 Artifact Store。

### Negative / Trade-offs

- 对象模型比"可变记录"复杂，写入路径需要纪律（先建对象，再移动 ref）；
- Git 名称会带来"是不是要存进 git 仓库"的误解，需文档澄清；
- 垃圾回收/对象过期策略需要设计（未来成本）。

## Rejected Alternatives

- **可变记录模型（一行状态到处改）**：丢失历史与证据链，与"验证的适应控制"核心价值冲突，拒绝；
- **完整克隆 Git 语义**：Git 的树/提交模型与 INA 领域对象不完全吻合，且引入无用复杂度，拒绝；
- **事件溯源作为唯一模型**：事件溯源适合存储事件流，但 INA 更需要"对象+refs+lineage"的读取模型，
  未来可在 commit 内嵌事件明细，不整体采用。

## Revisit Triggers

- 实验证明 Delta 生命周期比预期简单（如"纯文本替换即可"），对象模型过度设计——降级为轻量记录；
- 多 agent 协作场景暴露 refs 合并冲突无法解决（此时考虑扩展合并语义或改模型）。

## Relationship to Phase-0 Experiments

- Phase-0 不要求实现对象模型；但实验产物必须满足其雏形要求：
  `git_commit` + `git_dirty` + `git_diff_hash` 作为 run 的定位字段（见 ADR-0006）；
- EX-0.1-A 的 delta/ 目录即未来 `BehavioralDelta` 对象的雏形，要求"定稿即冻结、修改即新版本"。
