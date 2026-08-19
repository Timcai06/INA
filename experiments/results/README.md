---
用途: 预注册、运行记录、人工盲评、决策备忘
---

# experiments/results/

存放 Experiment 001 的全部证据：

- `preregistration.md` — 阈值冻结 + 隐藏集 hash + 统计约定（git commit 后不可修改）
- `runs/` — N=10 × 4 臂完整输出（含 Fingerprint 快照、输入输出 JSONL、注入块 hash）
- `human-review.md` — 人工盲评记录（2 名评员 + Rubric + kappa + delta-consistent 判定）
- `metrics-summary.csv` — 全部指标汇总
- `decision-memo.md` — Go / No-Go 判决（模板见 experiments/README.md）

纪律：负面结果与正面结果同等记录；预注册后不得修改阈值。