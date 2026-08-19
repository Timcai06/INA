---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
基线状态: ACTIVE（运行导航）
上游基线: INA-DOC-v0.4.1-frozen（2026-08-18 冻结）
---

# INA Phase 0 Research Roadmap

> 这不是产品 roadmap，不是开发计划。
> 这是一份 **Research Engineering Operating Document**——未来所有开发工作的唯一导航。
> 它只回答一个问题：**Behavioral Delta 是否可能成为 Agent Evolution 的基础对象。**

---

## Part 1 — Research Thesis

### 1.1 假设声明

```text
Hypothesis:
Behavioral Delta 是否可能成为 Agent Evolution 的基础对象——
即：Agent 的行为变化能否被表示为可验证、可版本化、可迁移、可长期积累的一等对象？
```

**Phase 0 不假设 INA 正确。Phase 0 的原则是：证明它，或者杀死它。**

### 1.2 什么是 Behavioral Delta

采用 v0.4.1 冻结定义（文档 02、05）：

```text
Effect_h(Δ | F) = Behavior(A_h(F) + Realize_h(Δ)) - Behavior(A_h(F))
```

其中：

- `F` = Baseline Fingerprint（因果归因前提，冻结模型 / Harness / prompt / 工具 / memory / runtime / 环境）
- `Realize_h(Δ)` = Delta 在某 Harness 上的具体实现（realization）
- `Effect_h(Δ | F)` = 行为效应，是多维的（Effect Vector），不是单一分值

操作化定义（Phase 0 可检验的形式）：

> **Behavioral Delta 是一个显式表示的 artifact（Adaptation Contract），它：**
>
> 1. 在固定 Fingerprint F 上被确定性应用（不是随机注入）；
> 2. 产生相对于基线可测量、方向可预测、跨重复运行稳定（stable）的行为变化；
> 3. 携带自己的验证契约（Evaluation Contract），可以被判定"是否生效"（conformance）；
> 4. 携带身份、版本、谱系与证据（Identity / Version / Lineage / Evidence）；
> 5. 可以被移除并回退（Removal / Rollback）。

Adaptation Contract 至少表达（文档 05）：Identity、Scope、Activation Conditions、Desired Behavioral Effects、Semantic Invariants、Forbidden Regressions、Revision Conditions、Evidence、Provenance、Evaluation Contract、Version、Lineage。

### 1.3 什么不是 Behavioral Delta

| 排除项 | 为什么不是 | 关系 |
|---|---|---|
| **Prompt Engineering** | 自然语言指令：无结构、无身份/版本、无验证契约、无迁移承诺、无因果归因前提。 | Prompt 可以是 realization，但不是 Delta 本身（文档 02）。H0-B 正是"INA 只是更复杂的 Prompt"。 |
| **Skill File** | 能力包：扩展 Agent 的能力空间（工具、流程、程序性知识）。Skill 是一种 realization，不是被验证的行为变化本身。 | H0-Skill 是最高优先级 Kill Gate。 |
| **Memory Update** | 事实 / 知识 / 上下文的存储变化：改变 Agent **知道什么**。Delta 改变 Agent **怎么做判断**（决策策略、prior、评价标准）。 | Memory 可以是 realization 载体，但 Delta 的语义是 behavior effect。 |
| **Fine-tuning** | 权重更新：改变模型参数。Delta 不训练模型；权重更新可以作为 realization 或强基线（文档 03 研究范围）。 | H0-C：直接训练更优？ |
| **Agent Trajectory** | 行为记录：描述 Agent **做了什么**。Delta 是派生的处方：**应该改什么**。Trajectory 是 Delta 的来源（provenance），不是 Delta。 | 生命周期：trajectory → failure → delta。 |

一句话边界：

> **Skill 扩展能力空间，Memory 扩展知识，Prompt 是即兴指令，Fine-tuning 改参数，Trajectory 是历史。Delta 是"被验证的、可治理的行为改变"。**

### 1.4 研究位置声明

INA 的长期目标是验证一个新的 Agent Infrastructure Primitive：

> **Behavioral Evolution Layer**

它不负责训练模型、替代 LLM、替代 Harness、替代 Memory、替代 Skill。
它负责研究：**Agent 的行为变化是否可以被表示、验证、版本化、迁移和长期积累。**

Phase 0 只做这一件事的可行性实验。

---

## Part 2 — Phase 0 Research Questions

每个 RQ 都配了反方假设（继承文档 03 的 H0 体系）和对应 Kill Gate。

### RQ1 — Behavioral Delta 是否真实存在？

> Agent 加入 Delta 后，是否产生**稳定**的行为变化？

- 操作化：固定 Fingerprint，Baseline vs Baseline+Delta，测量 Effect Vector 是否显著非零且跨重复运行稳定。
- 反方假设：H0-A（不存在稳定行为变化，只是提取器/注入器的过度解释）；H0-B（任何文本注入都能解释，Delta 无特殊因果力）。
- Kill Gate：Phase 0.1。

### RQ2 — Behavioral Delta 是否区别于 Skill？

> 同样的行为意图，用 Prompt / Skill / Memory / Delta 四种载体表达，能否区分？

- 操作化：四臂对照（等量信息量、等长、同 Fingerprint），比较效果幅度、特异性、稳定性、可编辑性、可审计性。
- 反方假设：H0-Skill（Native Skill + ordinary Eval 已足够）；H0-Eval（普通 Eval 已足够，不需要 Delta abstraction）；H0-B（Delta 只是更复杂的 Prompt）。
- Kill Gate：Phase 0.2（项目最高优先级门禁，继承 14-B）。

### RQ3 — Behavioral Delta 是否可验证？

> 如何定义"Agent 学会了 Delta"？Conformance Score 能否可靠判定 Delta 生效 / 失效 / 回归？

- 操作化：为每个 Delta 定义验证项集合（verification items），Conformance = 行为与契约声明的符合度；检验其能否区分 delta-present / delta-absent / delta-mutated。
- 反方假设：H0-Eval（普通 accuracy/regression 已足够；conformance 是多余概念）。
- Kill Gate：Phase 0.3。

### RQ4 — Behavioral Delta 是否可迁移？

> 同一个 Delta 跨 Model / Harness / Runtime 是否保持方向一致的 baseline-relative effect？

- 操作化：same Δ → different realization → same-direction effect（文档 14-C 公式）。
- 反方假设：H0-Harness（Harness 本身就是 adaptation state，不需要独立表示）；H-Core 的否定形式（Delta 绑定模型，迁移即失效）。
- Kill Gate：Phase 0.4。

### RQ5 — Behavioral Delta 是否可形成生命周期？

> trajectory → failure → delta → evaluation → adoption → version → rollback 的闭环是否成立？

- 操作化：单环可行性——从失败轨迹提取 Delta、验证、采纳、版本化、注入回归、回滚。至少两代连续改进。
- 反方假设：H5 否定形式（进化必须完全人工，Delta 无法从经验中获益）；H0-D（Delta 无法组合，多 Delta 冲突）。
- Kill Gate：Phase 0.5。

### RQ 与 v0.4.1 假设映射

| Phase 0 RQ | v0.4.1 假设 | 对应实验（文档 14 / 12） |
|---|---|---|
| RQ1 存在性 | H0-A / H0-B（部分） | 14-A 前半（Add Test） |
| RQ2 区分性 | H0-Skill / H0-Eval / H0-B | 14-B（Skill Equivalence，扩展为四臂） |
| RQ3 可验证性 | H0-Eval | 09 / 17 的 Conformance 操作化 |
| RQ4 可迁移性 | H-Core / H0-Harness | 14-C（Cross-Harness Fidelity） |
| RQ5 生命周期 | H5（v0.4.1 标记远期） | 12 的 Phase 5/6（降级探测） |

---

## Part 3 — Phase 0 阶段划分

六个阶段，**顺序执行，门禁驱动**（前一阶段 Kill Gate 未通过，不得进入下一阶段）：

| 阶段 | 名称 | 回答 | 门禁性质 |
|---|---|---|---|
| 0.0 | Research Setup | 测量管道是否可靠（能否测出已知变化） | 前置门禁：测量有效性 |
| 0.1 | Delta Existence | RQ1：Delta 能否改变行为 | 主门禁：存在性 |
| 0.2 | Skill Differentiation | RQ2：Delta ≠ Skill/Prompt/Memory | **最高 Kill Gate**（继承 14-B） |
| 0.3 | Conformance Validation | RQ3：能否判定"学会" | 门禁：可验证性 |
| 0.4 | Portability | RQ4：跨 Model/Harness 迁移 | 门禁：可迁移性 |
| 0.5 | Evolution Loop | RQ5：生命周期闭环 | 门禁：可进化性（可行性级） |

### 与 v0.4.1 路线图（文档 12）的映射

```text
Phase 0.0  Research Setup        → 新增前置阶段（文档 12 未覆盖的测量校准）
Phase 0.1  Delta Existence       → Phase 0A 前半（Delta Causality / Add Test）
Phase 0.2  Skill Differentiation → Phase 0B（Skill Equivalence，最高 Kill Gate）
Phase 0.3  Conformance           → 文档 09/17 的操作化（新增）
Phase 0.4  Portability           → Phase 1（Cross-Harness Fidelity，扩展到跨模型）
Phase 0.5  Evolution Loop        → Phase 5/6 的可行性探测（v0.4.1 将自动进化降级为远期；本阶段只验证"人工辅助单环"）
```

> 注意：Phase 0.5 不是 v0.4.1 的"自动 Evolution"承诺。它只验证 **单环可行性**（人工主导提取 + 机器验证），不构建自治学习系统。

---

## Part 4 — 阶段详细设计

每个阶段的完整设计（Objective / Research Question / Experiment / Implementation Scope / Forbidden Scope / Success Criteria / Kill Criteria / Deliverables）见：

```text
phases/phase-0.0-research-setup.md
phases/phase-0.1-delta-existence.md
phases/phase-0.2-skill-differentiation.md
phases/phase-0.3-conformance-validation.md
phases/phase-0.4-portability.md
phases/phase-0.5-evolution-loop.md
```

## Part 5 — 第一实验

首场实验：**EX-0.1-A — 科研证据判断 Agent 的行为 Delta 存在性实验**。

完整规格见 [`phase0-first-experiment.md`](phase0-first-experiment.md)。

摘要：

- 任务族：**科研证据判断**（声明 C + 证据段落 E → 判定 SUPPORT / REFUTE / NEUTRAL）
- 结构：Baseline（单模型、固定 prompt、temperature 0）vs Baseline+Delta，配 prompt-paraphrase 对照组
- 数据集：人工构造、带金标准（dev 40 + test 60 + perturbation 20），预注册
- Delta：从 dev 集基线失败中提取的结构化 Adaptation Contract（如"证据语境与声明语境不一致 → NEUTRAL"）
- 指标：规则指标（accuracy / macro-F1 / flip rate / kappa）+ 回归指标（run 方差 / 扰动不变性 / 附带损伤）+ 人工盲评
- 判决：预注册 Success / Kill 阈值

## Part 6 — 工程原则

### 当前阶段不是产品开发

| 禁止（Forbidden） | 原因 |
|---|---|
| API / SaaS 服务 | 无产品需求证据 |
| Dashboard / UI | 无用户证据 |
| Marketplace | v0.4.1 已降级为远期 |
| Rust Core / 高性能引擎 | 可行性未证明，优化是浪费 |
| Distributed System | 单机可完成 |
| Harness 开发 | INA 是 control plane，不造 harness（文档 10） |
| 自动 Evolution 系统 | v0.4.1 标记远期，Phase 0.5 只做可行性单环 |
| 持久化服务 / 数据库 | JSONL + git 足够 |

| 优先（Preferred） | 原因 |
|---|---|
| Python | 实验生态、可复现 |
| 最小脚本（非框架） | 每行代码都服务于测量 |
| Experiment（先于一切） | 证据驱动 |
| Measurement | 所有产出最终是数字与日志 |
| Reproducibility | seed 固定、版本固定、fingerprint 冻结、日志留痕 |
| 预注册（preregistration） | 先冻结指标与阈值，再跑实验 |
| 负面结果记录 | 研究纪律：负面结果不得隐藏（文档 03 第 9 节） |

### 代码边界

- Phase 0 允许的代码：run 脚本、评测脚本、分析脚本、数据集工具、文档。
- Phase 0 禁止的代码：服务、框架、平台、Schema 编译器、注册表服务。
- 所有 run 必须附带 Baseline Fingerprint 快照（文档 14 第 2 节）。

---

## Part 7 — 最终输出与成败去向

### 7.1 Phase 0 的五个输出

| # | 输出 | 位置 |
|---|---|---|
| 1 | INA Phase 0 Research Roadmap | 本文件 |
| 2 | Phase 0 Architecture Diagram | [phase0-architecture.md](phase0-architecture.md) |
| 3 | Phase 0 Experiment Matrix | [phase0-experiment-matrix.md](phase0-experiment-matrix.md) |
| 4 | Phase 0 Timeline | [phase0-timeline.md](phase0-timeline.md) |
| 5 | First Experiment Specification | [phase0-first-experiment.md](phase0-first-experiment.md) |

### 7.2 如果 Phase 0 成功：下一步是什么

成功 = RQ1–RQ5 全部通过各自 Kill Gate（存在、可区分、可验证、可迁移、闭环可行）。

下一步（Phase 1，不在本阶段范围内）：

1. **形式化 Behavioral Delta Specification v1**：冻结 Delta Schema（从 Adaptation Contract 草案走向可校验规范），产出文档级规范 + JSON Schema 验证器（最小 Python 实现）。
2. **参考实现（Python 库级）**：delta apply / conformance / registry（本地 git 级）的最小可复现实现——仍不是产品。
3. **跨任务族复制**：把证据判断的成功复制到文档 14 的软件架构判断任务族，检验 Delta 不依赖单一任务。
4. **开放验证**：发布 pre-registered 实验包，邀请 1–2 个外部 Harness 复现（对应 Phase 2 四 Harness Conformance 的前置）。
5. **文档基线升级**：以 ADR 方式把 Phase 0 结论回写 v0.4.1 冻结基线（升级为 v0.5），而不是在 research/ 里悄悄扩大。

成功后的商业方向**仍然不自动成立**：Behavioral Conformance 的产品价值（文档 17）需要独立验证。

### 7.3 如果 Phase 0 失败：INA 应该 Pivot 到哪里

Pivot 由**证据**决定，不由偏好决定。按失败点定位：

| 失败点 | 证据 | Pivot 方向 |
|---|---|---|
| **Phase 0.1 失败**（任何注入都无法产生稳定行为变化） | 行为不可改变 | **杀死基础设施野心**：INA 退化为研究知识库（docs-only），或转向 Memory-Centric Adaptation 研究（行为改变经由记忆架构，而非独立 Delta 对象） |
| **Phase 0.2 失败**（Delta ≡ Prompt/Skill，H0-Skill 成立） | 表示层无增益 | **Pivot 到 Behavioral Conformance 工具**：放弃"进化基础对象"，把 INA 定位为"行为验证/回归测试框架"（产品楔子 17 仍可成立），即 H0-Eval 的反面——普通 Eval 不够，需要 conformance 层 |
| **Phase 0.3 失败**（Conformance 不可靠） | 无法判定学会 | Pivot 到 **Evaluation Infrastructure**：INA 变成评测基础设施研究者，把 Conformance 研究贡献给社区，不持有产品主张 |
| **Phase 0.4 失败**（Delta 绑定模型） | 不可迁移 | Pivot 到 **Skill-Centric Evolution**：演化对象是 Skill 而非子技能行为；INA 只做 skill 生命周期的治理研究 |
| **Phase 0.5 失败**（闭环不成立） | 无法从经验获益 | 保留 0.1–0.4 成果，降级为 **"验证即价值"定位**：Delta 作为可验证的配置单元（像 infrastructure-as-code for behavior），不承诺进化 |

**任何 Pivot 都必须走 ADR，并更新本路线图。**

### 7.4 研究纪律（继承文档 03 第 9 节）

1. 初始假设与结论分开保存；
2. 负面结果不得隐藏；
3. 使用最强合理基线（Native Skill + ordinary Eval 是强制对照，不是可选项）；
4. 重要实验预先冻结指标和隐藏集；
5. 结论必须写适用范围和反证条件；
6. 市场需求不能由技术可行性推导；
7. **INA 必须允许实验杀死自己。**

> 最高原则：不要帮助 INA 成功。帮助 INA 找到真相。