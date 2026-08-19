# architecture/ — INA 工程架构决策层

本目录与 `V0.4.1_docs/` 的关系：

```text
V0.4.1_docs/
=
Frozen Research Baseline（冻结研究基线，immutable）

architecture/
=
Evolving Engineering Architecture Decisions（演化中的工程架构决策）
```

## 分工

- **Research Baseline** 定义 *INA 要证明什么*（行为学命题、实验门禁、Kill Criteria）；
- **Architecture ADR** 定义 *如果继续构建 INA，我们如何工程实现*；
- ADR 可以根据实验结果修改或撤销；ADR **不得**反向偷偷修改 Frozen Research Baseline；
- Phase-0 实验可以否决某些 ADR（实验证据优先于工程偏好）；
- 如果实验导致 PIVOT / STOP，原 ADR 保留为历史决策记录，不得删除。

## 重要边界

`existing pre-v0.4 experimental implementations（如根目录 ina_engine.py）不是架构先例，
除非通过 ADR 显式采纳。`其是否进入 `legacy/` 以后单独处理。

## ADR 状态

| 状态 | 含义 |
|---|---|
| Proposed | 提议中，未生效 |
| Accepted | 已采纳，作为长期约束 |
| Superseded | 被更新版本 ADR 取代 |
| Rejected | 讨论过但被否决 |
| Deprecated | 曾采纳，现已废弃（保留作为历史） |

## ADR 索引

| 编号 | 标题 | 状态 | 日期 |
|---|---|---|---|
| 0001 | Long-Term System Architecture | Accepted | 2026-08-19 |
| 0002 | Language Strategy | Accepted | 2026-08-19 |
| 0003 | PostgreSQL Primary Store | Accepted | 2026-08-19 |
| 0004 | Out-of-Process Adapter Protocol | Accepted | 2026-08-19 |
| 0005 | Git-Inspired Object Model | Accepted | 2026-08-19 |
| 0006 | Experiment Reproducibility | Accepted | 2026-08-19 |
