# ADR-0006: Experiment Reproducibility

- Status: Accepted
- Date: 2026-08-19
- Decision Owners: INA Phase 0 研究组
- Related Research Baseline: V0.4.1（Verified Behavioral Adaptation Control Plane，2026-08-18 冻结）

## Context

Phase-0 实验的结论将决定 INA 是否继续。如果实验无法精确复现、无法定位"当时到底跑了什么代码、
什么数据、什么参数"，判决就没有科学价值。EX-0.0-1 已证明：`seed=42 + temperature=0 +
think:false + presence_penalty=0` 在本地 Ollama qwen3.5:9b 上可完全复现（重复运行输出一致）。
该确定性是实验可复现的物理基础，必须成为制度。

## Decision

**Phase-0 实验采用三级实验模型，并强制执行 git 记录纪律。**

### 三级实验模型

| 级别 | 名称 | 证据等级 | 要求 |
|---|---|---|---|
| E0 | Exploratory（探索） | 不构成 Gate 证据 | 记录 `git_commit` / `git_dirty` / `git_diff_hash`；结论仅作提示 |
| E1 | Pilot（试点） | 支持性证据 | 本地 commit + clean 工作区；记录完整 digest 字段 |
| E2 | Formal（正式预注册） | 判决证据 | 全部冻结（代码/数据/阈值/提示词）；正式实验在 clean commit 上运行；记录全部 digest 字段 |

### Git 纪律

1. **no push ≠ no commit**：远程推送与否不影响本地提交义务；任何可判决的实验必须跑在 committed 状态上；
2. **实验前冻结**：正式实验开始前，代码、数据集、Delta、阈值全部 commit，记录该 commit SHA；
3. **结果必须落盘**：每次 run 的输出（`outputs.jsonl`、fingerprint、results summary）随结果提交；
4. **禁止事后修改**：冻结后的 Delta 文本与数据集，正式实验阶段不得改写；如需修改 → 新版本文件 + 新 commit。

### 正式实验（E2）必须记录的最小字段

```text
model_id / model_blob_sha256 / runtime_id / runtime_version
prompt_system / prompt_template / delta_version / delta_sha256
dataset_hash / item_hashes / thresholds / sampling_params
seed / temperature / presence_penalty / think / concurrency
git_commit / git_dirty / git_diff_hash / timestamp_utc / host_id
```

## Consequences

### Positive

- 任何结论可追溯：给定 commit + 数据集 hash + 参数，任何人都能复现；
- 预注册制度防止"看到结果再改阈值"的造假路径；
- E0 便宜、E2 严格，成本与证据等级匹配。

### Negative / Trade-offs

- 每个正式实验多一步 commit/校验开销（可接受）；
- 强纪律要求实验代码保持小而清楚，天然反对混沌式脚本；
- 人工步骤（如人工盲评）不在 git 纪律覆盖内，需在 decision memo 单独标注状态。

## Rejected Alternatives

- **实验不提交、靠本地目录"应该还在"**：无法复现、无法审计，拒绝；
- **所有实验一律 E2**：探索期会因提交摩擦变慢，拒绝；
- **阈值可在结果出来后调整**：等效于造假，拒绝（预注册阈值必须写在结果之前）。

## Revisit Triggers

- 模型行为出现不可复现性（同 seed 不同输出）——立即升级记录要求并排查；
- 远端模型/运行时升级（如 qwen3.5:9b 被替换）——实验必须重跑或显式记录版本切换；
- PIVOT/STOP：本制度继续适用新方向。

## Relationship to Phase-0 Experiments

- EX-0.1-A（四臂预注册实验）按 E2 执行；
- EX-0.0-1 及真实后端标定按 E0 执行（其结论仅作提示，不构成 Gate 证据）；
- 本 ADR 的字段清单直接定义 `fingerprint.py` 的元数据结构与未来 registry schema（ADR-0003）。
