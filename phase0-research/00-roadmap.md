---
文档版本: 0.2
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
基线状态: ACTIVE（运行导航）
上游基线: INA-DOC-v0.4.1-frozen（2026-08-18 冻结，不可修改）
---

# 00 — INA Phase 0 Research Roadmap

> 这不是产品 roadmap，不是开发计划。
> 这是 **Research Engineering Operating Document**——Phase 0 期间所有工作的唯一导航。
>
> 最高原则：**不要帮助 INA 成功。帮助 INA 找到真相。**
> 证明 Behavioral Delta 假设，或者杀死它。

---

## 1. Research Goal

Phase 0 要证明（或证伪）一件事：

> **Behavioral Delta 是否是一个真实存在、可表示、可验证的 Agent 基础对象。**

具体来说：Agent 的行为变化能否被表示为**独立于模型、Harness、Prompt、Skill、Memory 的显式 artifact**，并且这个 artifact 可以：

- 被确定性应用（注入后产生稳定、可测量的行为变化）；
- 被验证（能判定"是否生效"）；
- 被版本化、迁移、回滚（生命周期治理）。

Phase 0 不构建产品、不构建平台、不实现最终 INA。它只运行实验。

## 2. Core Hypothesis

```text
Hypothesis:
未来 Agent 不仅需要 Model / Harness / Memory / Skill / Tools，
还需要一个 Behavior Evolution Layer——
用于管理行为变化、行为版本、行为验证、行为迁移、行为回滚。

而 Behavioral Delta 是这个 Layer 的基础对象。
```

**不要相信这个假设。** 整个 Phase 0 的设计目标就是制造尽可能强的机会杀死它：

| 假设的子命题 | 对应的杀死方式 |
|---|---|
| Delta 能改变行为 | 无显著差异 / 不稳定 |
| Delta ≠ Prompt / Skill | H0-Skill：Native Skill + Eval 完全等价 |
| Delta 可验证 | Conformance 无法区分生效/失效 |
| Delta 可迁移 | 换模型/Harness 即失效 |
| Delta 支持演化 | 无法从经验中获益 |

采用 v0.4.1 冻结定义（文档 02）：

```text
Effect_h(Δ | F) = Behavior(A_h(F) + Realize_h(Δ)) - Behavior(A_h(F))
```

- `F` = Baseline Fingerprint（因果归因前提）
- `Realize_h(Δ)` = Delta 在某 Harness 上的 realization
- Delta 的显式表示 = Adaptation Contract（文档 05 的 11 字段）

## 3. Research Questions

### RQ1 — Behavioral Delta 是否能改变 Agent 行为？

> 加入 Delta 后，Agent 是否产生**稳定、可测量**的行为变化？

- 操作化：固定 Fingerprint，Baseline vs Baseline+Delta，Effect Vector 显著非零且跨重复运行稳定。
- 反方假设：H0-A（不存在稳定行为变化）；H0-B 弱形式（变化来自任意文本注入）。
- Kill Gate：Phase 0.1（Experiment 001）。

### RQ2 — Behavioral Delta 是否区别于 Skill？

> 同样的行为意图，用 Skill / Prompt / Memory / Delta 表达，能否区分？

- 操作化：四臂对照（等量信息、等长、同 Fingerprint），比较效果与治理属性（可编辑、可审计、可回滚、可预测变异）。
- 反方假设：H0-Skill（最高优先级 Kill Gate）；H0-Eval（普通 Eval 已足够）；H0-B（Delta ≡ 更复杂的 Prompt）。
- Kill Gate：Phase 0.2。

### RQ3 — Behavioral Delta 是否可验证？

> 如何定义"Agent 学会了 Delta"？Conformance Score 能否可靠判定生效 / 失效 / 回归？

- 操作化：为每个 Delta 定义验证项集，Conformance = 行为与契约声明的符合度；检验其区分 delta-present / delta-absent / delta-mutated 的能力。
- 反方假设：H0-Eval（普通 accuracy/regression 已足够，Conformance 无独立信息量）。
- Kill Gate：Phase 0.3。

### RQ4 — Behavioral Delta 是否可迁移？

> 同一个 Delta 跨 Model / Harness / Runtime 是否保持方向一致的 baseline-relative effect？

- 操作化：same Δ → different realization → same-direction effect（文档 14-C）。
- 反方假设：H0-Harness（Harness 即 adaptation state）；H-Core 否定形式（Delta 绑定模型）。
- Kill Gate：Phase 0.4。

### RQ5 — Behavioral Delta 是否支持持续演化？

> trajectory → failure → delta → evaluation → adoption → version → rollback 闭环是否成立？

- 操作化：人工主导提取 + 机器验证的单环可行性，≥ 2 代连续改进。
- 反方假设：H5 否定形式（提取必须完全人工，Delta 无法从经验获益）；H0-D（多 Delta 无法组合）。
- Kill Gate：Phase 0.5。

> 注意：RQ5 只验证"人工主导、机器验证"的单环。无人工门禁的自动 Evolution 在 v0.4.1 中标记为远期，不在 Phase 0 范围。

## 4. Phase Plan

顺序执行，门禁驱动。前一阶段 Kill Gate 未通过，不得进入下一阶段。

| 阶段 | 名称 | 回答 | 门禁性质 |
|---|---|---|---|
| 0.0 | Research Setup | 测量管道是否可靠 | 前置门禁（测量有效性） |
| 0.1 | Behavioral Delta Existence | RQ1 | 主门禁（存在性） |
| 0.2 | Skill Differentiation | RQ2 | **最高 Kill Gate**（继承 14-B） |
| 0.3 | Conformance Validation | RQ3 | 门禁（可验证性） |
| 0.4 | Portability | RQ4 | 门禁（可迁移性） |
| 0.5 | Evolution Loop | RQ5 | 门禁（闭环可行性） |

### Phase 0.1 — Behavioral Delta Existence

- **Objective**：证明 Delta 能改变 Agent 行为——固定 Fingerprint 上注入结构化 Adaptation Contract，产生稳定、方向可预测、可归因的行为变化。
- **Experiment**：Experiment 001（Behavioral Delta Existence Test，见 [`01-experiment.md`](01-experiment.md)）：单模型、单 Harness、科研证据判断任务、四臂对照（Baseline / Skill / INA Delta / Sham Delta）。
- **Success Criteria**：失败类 flip rate ≥ 0.6；失败类 accuracy 提升 ≥ 20pp；附带损伤 ≤ 5pp；run 方差 ≤ 3pp；扰动不变性 |Δ| ≤ 3pp；人工盲评 delta-consistent ≥ 0.7；Sham 明显更差。
- **Kill Criteria**：G1 vs G0 无统计显著差异；变化不稳定（方差 > 5pp）；附带损伤 > 20pp；无法从 dev 集提取实测失败。
- **Deliverables**：数据集（含金标准与标注协议）、Delta artifact（contract YAML + hash）、预注册文档、N=10 完整 run 记录 + Fingerprint、指标汇总 + 盲评记录、decision-memo.md。

### Phase 0.2 — Skill Differentiation

- **Objective**：强制判断 INA Delta 是否只是换了一种说法的 Skill / Prompt。H0-Skill 是本项目最高优先级 Kill Gate。
- **Experiment**：四臂对照升级（同一行为意图：Prompt / Native Skill / Memory / INA Delta，等量控制）+ Sham / Wrong-domain 对照；评价不只看准确率，还包括治理维度（可编辑、可审计、可回滚、变异可预测、维护成本）。
- **Success Criteria**：Delta 在 ≥ 1 个治理维度显著优于全部对手，且效果不劣；Sham / Wrong-domain 明显更差。
- **Kill Criteria**：**H0-Skill 成立**（Skill + ordinary Eval 全部等价或更优 → 停止或 Pivot）；H0-B 成立（去除结构后效果完全由自然语言解释）；Sham ≈ 真 Delta。
- **Deliverables**：四臂实验输出（含等量控制证明）、Skill Equivalence Report、治理维度对比、继续 / Pivot / Stop ADR 建议。

### Phase 0.3 — Conformance Validation

- **Objective**：定义并验证"什么叫 Agent 学会了 Delta"——Conformance Score 能区分生效 / 失效 / 变异，并检测回归。
- **Experiment**：为 Delta 构建验证项集；三条件测量（present / absent / mutated）；回归注入检测；与普通 accuracy 的信息量对比。
- **Success Criteria**：present/absent 间距 ≥ 2σ；mutated 可检测；回归检出率 ≥ 0.9；分数跨 run 稳定（SD ≤ 0.05）；相对普通 Eval 有信息量增量。
- **Kill Criteria**：无法区分 present / absent；分数方差过大（SD > 0.1）；与普通 accuracy 完全冗余（H0-Eval 成立）。
- **Deliverables**：Conformance Score 规范 v0.1（公式 + 加权 + 边界情形）、验证项集、EX-0.3-A/B 结果、冗余度分析、decision-memo.md。

### Phase 0.4 — Portability

- **Objective**：验证 Delta 是否脱离模型与 Harness 存在——同一 Contract 跨 Model / Harness 产生方向一致的 baseline-relative effect。
- **Experiment**：EX-0.4-A 跨模型（3 模型，不同家族 ≥ 2）；EX-0.4-B 跨 Harness（2 Harness，Harness 选择走 ADR）；Paired Replay；各自 Fingerprint。
- **Success Criteria**：方向一致率 ≥ 0.8，效应保留率 ≥ 0.5；cross-harness fidelity ≥ 0.5（provisional）且方向一致、作用域一致。
- **Kill Criteria**：任一模型方向相反或效应消失；fidelity < 0.5 或方向不一致；每个 Harness 都需重写 Delta 本体。
- **Deliverables**：Harness Selection ADR、Paired Replay 结果、Cross-Model/Harness Effect Vector、Fidelity Report、decision-memo.md。

### Phase 0.5 — Evolution Loop

- **Objective**：验证闭环可行性——trajectory → failure → delta → evaluation → adoption → version → rollback 是否成立（人工主导、机器验证）。
- **Experiment**：EX-0.5-A 单环可行性（科研证据判断任务族，2 代）：提取 Delta v1 → 验证 → 采纳版本化 → 注入冲突回归 → 回滚 → 第 2 代重复。
- **Success Criteria**：≥ 2 代连续改进（Conformance 单调不降且第 2 代有提升）；回滚成功率 1.0；提取的 Delta 全部通过验证；每步有 provenance。
- **Kill Criteria**：无法从失败轨迹提取出有效 Delta；第 2 代无提升且无合理解释；回滚失败；多 Delta 冲突失控。
- **Deliverables**：2 代演化完整日志、Delta Registry 示例（v1 / v1.1 冲突 / v2 + lineage）、Conformance 逐代曲线、回滚演练报告、RQ5 判决。

### Phase 0.0 — Research Setup（前置）

- **Objective**：证明测量管道本身可靠——在测量真实 Delta 前，先证明能测出**已知**注入的变化。
- **Experiment**：EX-0.0-1 管道校准（最小任务 + 已知变化注入 + 5 次重复 + Fingerprint drift 检测）。
- **Success Criteria**：检出率 ≥ 0.95，假阳性 ≤ 0.05；同 seed 完全可复现；Fingerprint 工具能捕获故意 drift。
- **Kill Criteria**：检出率 < 0.8 或假阳性 > 0.2；不可复现。→ 无法测量 = INA 无法被证伪 = Phase 0 整体结束。
- **Deliverables**：目录约定、数据格式、评测脚本、Fingerprint 工具、预注册模板、校准报告。

## 5. 详细设计导航

```text
00-roadmap.md            ← 本文件（唯一导航）
01-experiment.md            ← 第一实验规格（Behavioral Delta Existence Test）
research-architecture.md          ← Phase 0 实验架构图
experiment-matrix.md     ← 全部实验一览（EX-0.0-1 … EX-0.5-A）
timeline.md              ← 指示性时间线与门禁
phases/
├── phase-0.0-research-setup.md
├── phase-0.1-delta-existence.md
├── phase-0.2-skill-differentiation.md
├── phase-0.3-conformance-validation.md
├── phase-0.4-portability.md
└── phase-0.5-evolution-loop.md
```

每份 phases/ 文档包含完整 8 章节（Objective / Research Question / Experiment / Implementation Scope / Forbidden Scope / Success Criteria / Kill Criteria / Deliverables）。

## 6. 工程原则

### 当前阶段不是产品开发

| 禁止 | 允许 |
|---|---|
| 大规模重构 | 实验框架 |
| 产品化 / API / SaaS | Benchmark |
| Marketplace | Evaluator |
| Rust Core / 分布式 / 复杂 Runtime | Schema / Prototype |

| 优先 |
|---|
| Python |
| 实验可重复性（seed 固定、版本固定、Fingerprint 冻结） |
| 数据记录（JSONL + git，负面结果同权） |
| 可验证结果（预注册阈值 + 隐藏集纪律） |

### 代码边界

- Phase 0 允许的代码：run 脚本、评测脚本、分析脚本、数据集工具、Delta schema 校验脚本。
- Phase 0 禁止的代码：服务、框架、平台、注册表服务、自动 Evolution 系统。
- `ina_engine.py` 是 v0.3 时代遗留原型（符号规则引擎），不在 Phase 0 范围，不修改、不依赖。

## 7. 与 v0.4.1 冻结基线的映射

| Phase 0 | v0.4.1（文档 12/14） | 说明 |
|---|---|---|
| 0.0 Setup | 新增前置 | 测量校准，文档 12 未覆盖 |
| 0.1 Existence | Phase 0A / 14-A（Add Test 部分） | 存在性 |
| 0.2 Differentiation | Phase 0B / 14-B | **最高 Kill Gate** |
| 0.3 Conformance | 09 / 17 操作化 | 新增 |
| 0.4 Portability | Phase 1 / 14-C | 扩展到跨模型 |
| 0.5 Evolution Loop | Phase 5/6 可行性探测 | 只做人工主导单环 |

`V0.4.1_docs/` 是冻结理论基线，**不得修改**。任何改变其核心定义、Schema、Kill Gate 的决定走 ADR。

## 8. 如果 Phase 0 成功 / 失败

### 成功（RQ1–RQ5 全部通过）→ 下一步

1. **Behavioral Delta Specification v1**：冻结 Delta Schema（JSON Schema 验证器，最小 Python 实现）；
2. **参考实现（库级）**：delta apply / conformance / git 级 registry——仍不是产品；
3. **跨任务族复制**：证据判断 → 软件架构判断（文档 14 任务族），检验不依赖单任务；
4. **开放验证**：pre-registered 实验包 + 1–2 个外部 Harness 复现；
5. **文档基线升级**：以 ADR 把结论回写冻结基线（升级 v0.5）。

### 失败 → Pivot 地图（由证据定位，不由偏好决定）

| 失败点 | 证据 | Pivot |
|---|---|---|
| 0.1（行为不可变 / 不可测） | 无稳定变化 | 杀死基础设施野心 → docs-only 知识库 或 Memory-Centric Adaptation 研究 |
| 0.2（H0-Skill 成立） | Delta ≡ Skill/Prompt | Pivot 到 **Behavioral Conformance 工具**（产品楔子 17 仍可成立） |
| 0.3（不可验证） | Conformance 不可靠 | Pivot 到 **Evaluation Infrastructure**（贡献 Conformance 研究，不持有产品主张） |
| 0.4（绑定模型） | 不可迁移 | Pivot 到 **Skill-Centric Evolution**（演化对象是 Skill） |
| 0.5（闭环不成立） | 无法从经验获益 | 降级为 **"验证即价值"**：Delta 作为可验证配置单元（infrastructure-as-code for behavior），不承诺进化 |

**任何 Pivot / Stop 必须走 ADR，并更新本路线图。**

## 9. 研究纪律（继承文档 03 第 9 节）

1. 初始假设与结论分开保存；
2. 负面结果不得隐藏；
3. 使用最强合理基线（Native Skill + ordinary Eval 是强制对照，不是可选项）；
4. 重要实验预先冻结指标和隐藏集；
5. 结论必须写适用范围和反证条件；
6. 市场需求不能由技术可行性推导；
7. **INA 必须允许实验杀死自己。**