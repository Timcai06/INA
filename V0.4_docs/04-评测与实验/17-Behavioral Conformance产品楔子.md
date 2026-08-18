---
文档版本: v0.4
项目阶段: Research + Phase-0 Engineering
最后更新: 2026-08-18
基线状态: FROZEN
冻结日期: 2026-08-18
---

[返回文档矩阵](../00-文档矩阵与阅读路径.md)

# Behavioral Conformance 产品楔子

> 本文档不是完整 PRD。它只回答：第一产品是什么，为谁解决什么问题，MVP 包含什么，以及真正的壁垒可能在哪里。

## 1. User

第一批用户：

> 同时使用 2 个及以上 Coding Agent，并维护团队级 Agent 行为/工程原则的 AI-native software team。

典型画像：

- 团队使用多个 Coding Agent Harness（通过 Harness Selection Criteria 候选列表选择）；
- 团队有明确的工程原则（如"不把用户偏好当证据""重大决策必须保留竞争方案"）；
- 团队不确定这些原则在不同模型 / Harness / 版本中是否真的生效；
- 团队需要可审计的证据，而不是"感觉上 Agent 听话了"。

## 2. Pain

他们的问题不是：

```text
没有 Memory
```

而是：

```text
我们不知道团队要求的 Agent 行为
在不同模型 / Harness / 版本中是否真的生效。
```

具体表现：

| 痛点 | 描述 |
|---|---|
| 行为不可见 | 不知道 Agent 是否真的在遵循某个决策原则 |
| 跨 Harness 不一致 | 同一原则在 Claude Code 和 Codex 上表现不同 |
| 版本升级后退化 | 模型更新后，之前生效的行为策略失效 |
| 无法审计 | 无法证明"我们的 Agent 确实在做 X" |
| 无法回滚 | 发现策略有问题时，无法安全地回到之前的状态 |

## 3. Product

第一产品：

# INA Behavioral Conformance

核心命令：

```bash
ina test <policy>
```

这个命令回答一个问题：

> 给定一个 behavioral policy（Behavioral Delta Manifest），它在指定的 Harness 上是否真的产生了预期的 baseline-relative behavioral effect？

## 4. MVP 范围

### MVP Core（Phase 0A/0B 阶段）

| 组件 | 说明 |
|---|---|
| Behavioral Delta Manifest | YAML/JSON 格式的 adaptation contract |
| Single-Harness Adapter | 支持一个候选 Harness |
| Baseline Fingerprint Capture | 自动采集和验证 Agent 基线指纹 |
| Baseline / Adapted Paired Replay | 同一任务在 Base Agent 和 Agent + Δ 上的对比执行 |
| Effect Vector Evaluation | 多维度行为变化测量（不是单一分值） |
| Against-Prior Test | 验证 Δ 是否真正改变了 Agent 的 prior |
| Regression Test | 验证目标行为改善的同时其他能力没有退化 |
| Baseline Drift Detection | 检测模型 / Harness 升级后的基线漂移 |
| CI Report | 结构化报告，可集成到 CI 流程 |

### Conditional Expansion（Phase 1+，只有 INA 未被 H0-Skill 杀死后才加入）

| 组件 | 说明 |
|---|---|
| Cross-Harness Fidelity | 验证同一 Δ 在不同 Harness 上是否产生方向一致的效果 |
| 2–4 Harness Adapters | 支持 Harness Selection Criteria 候选列表中的 2-4 个 |
| Compiler | Harness-specific realization 编译 |
| Compatibility Matrix | Δ × Harness × Model 的兼容性矩阵 |

### 不包含

| 组件 | 排除原因 |
|---|---|
| Dashboard | MVP 阶段不需要可视化，CLI + CI Report 足够 |
| Marketplace | 验证问题未解决时市场无意义 |
| Auto-learning | INA-seq 等学习方法是远期目标 |
| Memory SaaS | 不是第一产品的核心 |
| Huge Registry | 最小化即可 |
| Consumer App | 目标用户是团队，不是个人 |

## 5. 核心工作流

```text
用户编写 Behavioral Delta Manifest
        ↓
ina test <policy> --harness <candidate-a>,<candidate-b>
        ↓
┌─────────────────────────────────────┐
│ 对每个 Harness:                      │
│   1. Capture Baseline Fingerprint   │
│   2. Validate Fingerprint Integrity │
│   3. Baseline 执行 (Agent only)     │
│   4. Adapted 执行 (Agent + Δ)       │
│   5. Fingerprint Equality Check     │
│   6. Effect Vector 提取             │
│   7. Against-Prior 验证             │
│   8. Regression 检查                │
└─────────────────────────────────────┘
        ↓
Cross-Harness Fidelity 计算（如适用）
        ↓
CI Report (PASS / FAIL + 详情)
```

产品输出必须明确展示：

```text
Policy / Contract Version
Baseline Fingerprint
Harness Version
Model Version
Realization Hash
Evaluation Contract Version
Conformance Result
```

产品价值中增加：

> 模型或 Harness 升级后，自动识别 Baseline Drift 并要求重新验证。

## 6. Moat 分析

### 不是壁垒

```text
YAML Schema
```

Schema 是公开的，任何人都可以定义自己的 adaptation contract。

### 可能是壁垒

| 壁垒 | 说明 |
|---|---|
| Behavioral probe corpus | 经过验证的行为测试用例集，覆盖多种任务族 |
| Cross-harness trajectories | 在多个 Harness 上执行的 paired replay 数据 |
| Realization-effect dataset | 同一 Δ 在不同 realization 下的效果数据 |
| Compatibility matrix | Δ × Harness × Model 的兼容性矩阵 |
| Evaluation methodology | 行为变化的测量方法论和指标体系 |
| Enterprise policy lineage | 企业级策略的版本、审计和回滚记录 |

这些壁垒的共同特点：

> 需要大量实际执行才能积累，不是一次性编写可以获得的。

## 7. 定价原则（暂定）

| 层级 | 内容 | 定价方式 |
|---|---|---|
| Free | 基础 conformance 测试 | 免费 |
| Pro | 完整 cross-harness + CI 集成 | 订阅 |
| Enterprise | 私有部署 + 策略治理 + 审计 | 企业授权 |

定价的前提是：conformance 结果有实际价值。

## 8. 成功标准

### MVP 成功

- [ ] 2+ 个 Harness 上的 paired replay 可自动执行
- [ ] Effect Vector 可量化
- [ ] Against-Prior 测试可检测 behavioral change
- [ ] Cross-Harness Fidelity 可计算
- [ ] CI Report 可集成

### 产品成功

- [ ] 有团队实际使用 ina test 验证策略
- [ ] conformance 结果影响团队的 Harness 选择
- [ ] 企业客户为策略治理付费

## 9. 风险

| 风险 | 缓解 |
|---|---|
| YAML Schema 不是壁垒 | 投资 probe corpus 和 effect dataset |
| Harness 变化太快 | Adapter 抽象层，快速适配 |
| 行为测量不准确 | 多维度 Effect Vector，不依赖单一指标 |
| 用户不需要 cross-harness | 验证用户实际需求，不假设 |

## 10. 与文档矩阵的关系

| 关联文档 | 关系 |
|---|---|
| 01-项目总纲 | 本卷是 01 中"产品楔子不再暂缓"的具体化 |
| 09-评测体系 | 本卷的 eval 方法来自 09 的新 eval 类型 |
| 12-路线图 | 本卷对应路线图的 Phase 0A/0B/1 |
| 13-风险登记 | 本卷的风险与 13 中的 R1-R9 交叉 |
