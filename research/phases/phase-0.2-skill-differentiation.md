---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
阶段: 0.2
---

# Phase 0.2 — Skill Differentiation

> 对应实验：EX-0.2-A（四臂对照）
> 回答：**RQ2**
> 上游文档：V0.4.1_docs 14-B（Skill Equivalence，**项目最高优先级 Kill Gate**）、03（H0-Skill / H0-B / H0-Eval）

## Objective

强制判断：**INA Delta 是否只是换了一种说法的 Skill / Prompt？**

同样的行为意图，用四种载体表达，控制一切信息变量后，比较其效果与治理属性。如果 Native Skill + ordinary Eval 完全等价或更优——**项目停止或 Pivot**（H0-Skill 成立）。

## Research Question

> RQ2：Behavioral Delta 是否区别于 Skill / Prompt / Memory？

反方假设：H0-Skill（Skill + 普通 Eval 已足够）；H0-B（Delta 只是更复杂的 Prompt）；H0-Eval（普通 Eval 已足够，Delta abstraction 无必要）。

## Experiment

**EX-0.2-A 四臂对照**（同一任务族、同一 Fingerprint、同一行为意图）：

| 臂 | 载体 | 形态 |
|---|---|---|
| A | Prompt | 等量自然语言指令（即 G2 升级版） |
| B | Native Skill | 等量原则写成 Agent Skill 文件（文档 14 14-B 定义） |
| C | Memory | 同一意图写成记忆条目（事实/策略形式） |
| D | INA Delta | 结构化 Adaptation Contract + Realization |

**必须控制**：自然语言信息量、token 长度、示例数量、工具权限、模型版本、Harness 版本、评测任务、Baseline Fingerprint（文档 14 第 6 节）。

**评价维度**（不只看准确率）：效果幅度、特异性（作用域控制）、稳定性、Causal Attribution、Editability、Auditability、Rollback、Mutation Predictability、Maintenance Cost。

**附加对照**：Sham Delta（结构一致但原则错误）与 Wrong-domain Delta（无关领域）必须明显更差（文档 14 14-A 门禁）。

## Implementation Scope

- 四种载体的等量构造工具（长度/信息量校验）；
- Skill / Memory / Prompt 臂的最小实现（复用 Phase 0.1 的 run 管道）；
- 治理维度评测（编辑/回滚/审计的脚本化演练）；
- 消融报告模板。

## Forbidden Scope

- 不等量对照（信息量或长度失控的实验无效）；
- 只比准确率（忽略治理维度）；
- 跳过 Sham / Wrong-domain 对照；
- 多 Harness（本阶段仍单 Harness，跨 Harness 是 0.4）。

## Success Criteria

- Delta 在**至少一个治理维度**显著优于全部对手（Editability / Auditability / Rollback / Scope Control / Mutation Predictability 之一），且效果不劣于对手；
- Sham / Wrong-domain 明显更差（结构有意义，不是"怎么都行"）。

## Kill Criteria

1. **H0-Skill 成立**：Native Skill + ordinary Eval 在效果、迁移、维护、审计、复杂度上全部等价或更优 → **项目停止或 Pivot**（最高 Kill Gate）；
2. H0-B 成立：去除 JSON/结构后效果完全由自然语言解释（Delta ≡ Prompt）；
3. H0-Eval 成立：普通 Eval 与 Conformance 在判定上无差异（此条与 0.3 联动，0.2 记录证据）；
4. Sham / Wrong-domain 与真 Delta 无差异（结构无意义）。

## Deliverables

```text
四臂实验配置与输出（等量控制证明）
Native Skill 基线实现
Skill Equivalence Report
治理维度对比表
Sham / Wrong-domain 结果
继续 / Pivot / Stop ADR 建议
```

## 出口门禁

- INA 有 ≥ 1 项可量化治理优势 → 进入 Phase 0.3（Conformance Validation）；
- H0-Skill / H0-B 成立 → **停止或 Pivot**（roadmap 7.3 定位），走 ADR。这是整个 Phase 0 最重要的决定点。