---
用途: 基线配置与 Fingerprint
---

# experiments/baseline/

存放 Experiment 001 的**基线定义**：

- `baseline_fingerprint_template.yaml` — Fingerprint 采集模板（文档 14 第 2 节格式）
- `system_prompt_v1.txt` — 固定 System Prompt 模板（四臂共用，记录 sha256）
- `run-<NNN>/` — 每次 run 前采集的 Fingerprint 快照（或统一放 results/runs/，本目录只放模板与基线配置）

纪律：Fingerprint 缺失或 drift 的 run 作废，不计入正式统计。