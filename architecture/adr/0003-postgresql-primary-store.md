# ADR-0003: PostgreSQL Primary Store

- Status: Accepted
- Date: 2026-08-19
- Decision Owners: INA 首席系统架构师 / INA Phase 0 研究组
- Related Research Baseline: V0.4.1（Verified Behavioral Adaptation Control Plane，2026-08-18 冻结）

## Context

INA 长期需要存储：契约、指纹、运行记录、验证结果、谱系（lineage）、组织与权限等结构化状态。
实验期使用文件系统 + JSONL/YAML，速度快但缺乏查询、并发、权限与索引能力。
若把所有内容（包括大体积实验产物）都塞进单一存储，会同时破坏查询性能与制品不可变性。

## Decision

**PostgreSQL 是 INA 长期 authoritative structured data store。**

默认存储：Identity、Metadata、Refs、Lineage index、Validation index、Contract state、
Organizations、Permissions、Policy state、Compatibility index、Registry metadata。

**但 PostgreSQL 不负责存储所有内容。** 必须区分两类存储：

```text
PostgreSQL      = structured authoritative metadata / refs / indexes
Artifact Store  = immutable large artifacts
```

Artifact Store 存放：raw trajectories、large model outputs、experiment artifacts、reports、
realizations、snapshots、evaluation evidence。
未来可进入：Object Storage、Content-Addressed Store、OCI Registry。

**Phase-0 阶段允许 filesystem 作为 Artifact Store 实现，但逻辑接口必须提前区分
Metadata Store 与 Artifact Store。不要把 PostgreSQL 当作文件系统。**

## Architecture

```text
Metadata Store（PostgreSQL）        Artifact Store（未来 OCI/CAS/对象存储）
├─ identity / refs / lineage index   ├─ raw trajectories
├─ contract state / registry         ├─ large outputs / evidence
├─ orgs / permissions / policy       ├─ snapshots / reports / realizations
└─ compatibility / validation index  └─（Phase-0: filesystem 即可）
```

## Consequences

### Positive

- 查询、审计、权限、并发正确性由成熟数据库承担；
- 大制品保持不可变、内容寻址友好，不被关系型存储扭曲；
- Phase-0 零负担：文件系统继续用，接口边界提前确定。

### Negative / Trade-offs

- 引入 PostgreSQL 运维成本（长期）；
- 两套存储之间的引用一致性需要纪律（refs 指向 artifact digest，而非内联内容）；
- 过早引入会拖慢实验——故本 ADR 只冻结方向，不要求 Phase-0 部署 PG。

## Rejected Alternatives

- **全文件系统长期方案**：无法支撑组织/权限/索引/并发，拒绝；
- **PostgreSQL 存储一切（含大制品）**：大对象拖垮数据库、破坏不可变制品语义，拒绝；
- **引入 NoSQL（MongoDB 等）作为主存储**：结构化权威元数据用关系型更稳，拒绝。

## Revisit Triggers

- 实验证明谱系/验证数据量级远小于预期，单机 SQLite 级别足够（降级评估）；
- 出现强分布式多站点需求时，评估分布式 SQL 方案；
- PIVOT/STOP 时，本 ADR 随新方向重评。

## Relationship to Phase-0 Experiments

- 实验完全不受影响（文件系统继续）；
- 实验产出的 run/validation 记录结构（`outputs.jsonl` + fingerprint）将作为未来 Metadata Store 的 schema 蓝本；
- EX-0.0-1 证明的可复现字段集合（ADR-0006）直接定义未来 registry 的必存列。
