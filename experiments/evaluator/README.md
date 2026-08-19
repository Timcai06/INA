---
用途: 指标计算脚本（最小 Python）
---

# experiments/evaluator/

存放指标计算脚本。**只服务于判决，不做框架。**

- `metrics_rule.py` — 规则指标：accuracy / macro-F1 / flip rate / kappa / 附带损伤 / 混淆位移
- `metrics_behavior.py` — 行为指标：Effect Vector 维度、理由一致性、特异性
- `metrics_regression.py` — 回归指标：run 方差、扰动不变性、Sham 对照差异、移除回退
- `run_agent.py` — 单次 run 脚本（四臂共用：baseline / skill / delta / sham 注入）
- `tests/` — 脚本自测（用已知输出验证指标计算正确性，对应 Phase 0.0 管道校准）

纪律：指标计算必须有自测；same seed 必须完全可复现；不允许 LLM Judge 进入主判决路径。