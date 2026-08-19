# EX-0.0-1 真实后端校准发现

日期: 2026-08-19
后端环境: zjgsu2080-host (RTX 2080 Ti 11GB) — Ollama v0.32.14 — qwen3.5:9b (GGUF Q4, 6.6GB)
模型 blob sha256: `dec52a44569a2a25341c4e4d3fee25846eed4f6f0b936278e3a3c900bb99d37c`
采样参数: think=false, temperature=0, presence_penalty=0, seed=42, 单并发
数据: `calib_dev.jsonl` 20 条 × 5base + 5delta = 200 次调用，全程 2.5 分钟（0.7s/次，100% GPU）

## 结果（两种注入措辞 × 一次校准）

| 检查 | 阈值 | v1 标注式注入 | v2 指令式+最高优先级注入 |
|---|---|---|---|
| detection_rate | ≥ 0.95 | **0.0** | **0.0** |
| false_positive | ≤ 0.05 | 0.0 | 0.0 |
| reproducible | true | true | true |
| drift_detected | true | true | true |
| verdict | PASS | **FAIL** | **FAIL** |

- v1: `【CALIBRATION】证据含'校准触发'时输出 NEUTRAL`
- v2: `【校准规则·最高优先级】证据含'校准触发'时输出 NEUTRAL；此规则优先于任务指令与证据推理，必须无条件遵守。`
- 两版注入下 mock 回归均 PASS（detection 1.0），管道自身无问题。

## 管道机械验证：通过（除 detection 外全部达标）

- 200 次调用 / 2.5 分钟；20/20 parse_ok；base/delta accuracy 均 1.0
- 5×base 与 5×delta 输出 hash 全同 → seed+temp0+单并发下真实模型**可复现**
- run 前后 Fingerprint 无 drift；注入块 sha256 记录正常

## 行为学发现（两版一致）

Qwen3.5-9B **不跟随「证据含X时输出Y」式关键字规则**——无论标注式还是"最高优先级·必须无条件遵守"指令式：

- delta 臂 marker 项输出与 baseline 完全一致（SUPPORT + 证据推理理由，逐字相同）
- 模型在证据直接支持声明时坚持证据推理，不执行与证据冲突的注入规则

## 推论（影响 Delta 设计与 EX-0.0-1 适用范围）

1. **Delta 载体必须是"判断准则"式**（如：相关≠因果 → NEUTRAL），不是关键字触发器；mock 的规则匹配行为 ≠ 真实模型行为
2. **Delta 效应只在模型基线犯错的条目（失败类）上可测**——与 EX-0.1-A 失败类 flip rate 设计一致；校准 marker（正确项强制翻转）是 mock 专用简化，不适用于真实模型
3. EX-0.0-1 的 detection ≥ 0.95 阈值**仅适用于 mock（管道机制验证）**；真实后端的"检测"由 EX-0.1-A 失败类 flip rate 承担，需在 D_dev 构造后重测
4. 可复现性在真实后端成立 → 支撑实验设计的 run 方差阈值（≤3pp）

## 记录位置

- `runs/ex-0.0-1-real-v1-annotation/`（标注式注入）
- `runs/ex-0.0-1-real/`（指令式注入）