---
文档版本: 0.2
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
实验ID: EX-0.1-A / Experiment 001
状态: SPEC DRAFT（阈值待正式预注册冻结）
上游基线: INA-DOC-v0.4.1-frozen（文档 02 / 05 / 14）
---

# 01 — Experiment 001: Behavioral Delta Existence Test

> 回答 **RQ1**：加入 Behavioral Delta 后，Agent 是否产生**稳定、可测量**的行为变化？
>
> 实验限制：**一个模型、一个 Agent Harness、一个任务族、一个 Delta。不复杂。**

---

## 1. 实验设计原则

- 单模型（预注册时冻结，首选高可控 API 模型）；
- 单 Harness（最小脚本调用环境，非平台）；
- 单任务族（科研证据判断）；
- 四臂对照，全部共享同一 Baseline Fingerprint；
- 预注册：阈值、统计约定、隐藏集 hash 先冻结，再跑正式实验；
- 判决不依赖 LLM Judge（LLM Judge 只可作参考，不得作为主判决依据）。

## 2. Baseline Agent

| 组件 | 定义 | 说明 |
|---|---|---|
| 模型 | 单模型，预注册冻结（provider / name / version / variant） | 不多模型 |
| System Prompt | 固定模板 v1（任务说明 + 输出格式约束：SUPPORT/REFUTE/NEUTRAL + 一句话理由） | 四臂共用 |
| Tools | 无 | 纯文本判断 |
| Memory | 无 | 无记忆污染 |
| Environment | temperature 0（或固定 seed）、单机 Python runner、模型版本锁定 | 可复现 |
| 重复运行 | N = 10 | 方差测量 |

### Baseline Fingerprint

每次 run 前采集（文档 14 第 2 节格式），run 后复核无 drift；Fingerprint 变化时该 run 作废：

```yaml
baseline_fingerprint:
  id: "<fingerprint-id>"
  harness: {name, version}
  model: {provider, name, version, variant}
  system: {prompt_hash, instruction_files, instruction_hashes}
  tools: {enabled: []}
  permissions: {profile}
  skills: {enabled: []}
  memory: {mode: "none"}
  runtime: {temperature: 0, reasoning_effort, context_policy, max_steps}
  environment: {workspace_revision, relevant_flags}
  uncontrolled_variables: []
```

## 3. 任务族：科研证据判断

> 输入：研究声明 C + 证据段落 E（论文摘要/结论摘录）。
> 输出：`SUPPORT` / `REFUTE` / `NEUTRAL` + 一句话理由。

选择理由：

1. 有客观金标准（人工标注），规则指标可计算；
2. "证据纪律"行为可精确定义并注入（见第 4 节）；
3. 基线模型存在可复现的系统性失败（用 D_dev 证明），是 Delta 的天然落点；
4. 输出空间小，行为变化可被 flip rate 精确度量；
5. 与 v0.4.1 Effect Vector 维度（evidence_seeking / user_prior_weight / disconfirmation_reporting）同构。

### 数据集（人工构造、受控、带金标准）

| 子集 | 数量 | 用途 |
|---|---|---|
| D_dev | 40 | 识别基线实测失败、提炼 Delta |
| D_test（in-class） | 30 | 主测试：Delta 目标失败类（隐藏集） |
| D_test（near-transfer） | 30 | 同规则、不同领域表面内容（隐藏集） |
| D_pert | 20 | 扰动不变性：无关改写不应改变 Delta 行为 |

条目格式（JSONL）：

```yaml
item_id: ev-001
claim: "每日饮用绿茶可显著降低心血管疾病风险"
evidence: "一项针对 40 名健康成年人的 6 周干预研究发现，饮用绿茶组的 HDL 胆固醇水平较对照组有统计学显著上升。"
gold_label: "SUPPORT"
failure_class: "context_mismatch"     # None = 对照组条目
```

标注协议先于数据冻结（≥ 2 名标注者独立标注，kappa ≥ 0.7，不一致裁决）；隐藏集在预注册前不暴露给模型与标注者。

## 4. Behavioral Delta — Research Evidence Discipline Delta

> 第一个 Delta 靶向**科研证据判断中的证据纪律**：只按证据本身下结论，不被声明强度、相关关系或表面一致性带偏。
>
> **这不是 Prompt。** 它是结构化 Adaptation Contract（字段驱动、带身份/版本/证据/谱系/验证契约）。

### Problem

基线 Agent 在科研证据判断中存在系统性"证据不纪律"：证据与声明语境不一致仍判 SUPPORT；相关关系被读成因果关系；证据不足仍支持声明；直接反驳被软化为 NEUTRAL。

### Observed Failure

D_dev 基线实测（预注册时附运行日志 hash）。候选失败模式族（实测确认后选取 1–2 个作为 Delta 靶点）：

1. `context_mismatch`：证据语境（人群/条件/时间）与声明不一致，基线倾向 SUPPORT；
2. `correlation_as_causation`：证据是相关关系，声明断言因果，基线倾向 SUPPORT；
3. `insufficient_evidence`：证据强度不足以支撑声明程度，基线倾向 SUPPORT；
4. `contradiction_softening`：证据实际反驳声明，基线输出 NEUTRAL 而非 REFUTE。

### Desired Behavior

- 仅当证据**直接支持**声明时 → SUPPORT；
- 证据与声明语境不一致、或仅相关、或强度不足时 → NEUTRAL；
- 证据反驳声明时 → REFUTE；
- 理由必须引用证据中的具体事实，不得泛泛而谈。

### Invariants（不可违反）

- 证据与声明直接一致时，不得改判为 REFUTE / NEUTRAL；
- NEUTRAL ≠ REFUTE：证据相关但不充分时输出 NEUTRAL，不是 REFUTE；
- 不引入机械反对（不因"被要求谨慎"而系统性否定一切）。

### Forbidden Regression（禁止退化）

- 三分类基础准确率不显著下降；
- D_pert 上的扰动不变性保持（Delta 不应被无关改写触发）；
- 理由一致性（标签与理由文本一致）不下降。

### Evaluation Contract

- 验证项集（v0.1）：activation 项（命中失败模式时必须改判）、invariant 项（直接一致时必须保持）、regression 项（对照组条目不得改变）；
- 本实验用 flip rate + 附带损伤近似判定；Conformance Score 正式化在 Phase 0.3。

### Delta 形态（示例，以 D_dev 实测为准）

```yaml
adaptation_contract:
  identity:
    id: "ac-evidence-discipline-v1"
    name: "科研证据判断纪律"
    version: "0.1.0"
  scope:
    applies_to: "科研证据判断（声明+证据 → SUPPORT/REFUTE/NEUTRAL）"
    precondition: "baseline prompt 模板 v1；模型 <预注册冻结>"
  activation_conditions:
    - "证据语境与声明语境不一致（人群/条件/时间/场景）"
    - "证据仅为相关关系而声明断言因果"
    - "证据强度不足以支撑声明程度"
  desired_behavioral_effects:
    effect_vector:
      - {dimension: "context_mismatch_detection", direction: "increase"}
      - {dimension: "correlation_causation_discrimination", direction: "increase"}
      - {dimension: "support_precision", direction: "increase"}
      - {dimension: "neutral_appropriateness", direction: "increase"}
      - {dimension: "disconfirmation_reporting", direction: "increase"}
  semantic_invariants:
    - "证据直接支持声明时不得改判"
    - "NEUTRAL ≠ REFUTE"
    - "不引入机械反对"
  forbidden_regressions:
    - "基础三分类准确率"
    - "扰动不变性（D_pert）"
    - "理由一致性"
  evaluation_contract:
    verification_items: "见本文件第 6 节；Conformance 正式化在 Phase 0.3"
  evidence:
    source: "D_dev 基线运行日志（预注册时附 hash）"
  provenance: {author: "INA Phase 0 研究组", license: "research-only"}
```

**注入方式**：结构化块（Contract 渲染为受控文本段落）确定性追加在固定 prompt 模板之后；C 臂与 A 臂的唯一差异就是该块。

## 5. Comparison（四臂对照）

| 臂 | Agent | 注入内容 | 控制要求 |
|---|---|---|---|
| A | Baseline Agent | 无（固定 prompt 模板 v1） | 基准 |
| B | Skill Agent | 同意图写成 Native Skill 文件（等量自然语言原则） | 与 C 等量信息、等长 |
| C | INA Delta Agent | 结构化 Adaptation Contract 注入 | 与 B 等量信息、等长 |
| D | Sham Delta Agent | 结构一致但原则错误/随机的 Contract | 与 C 同结构、同长度 |

控制变量：信息量、token 长度、示例数量、工具权限、模型版本、Harness 版本、评测任务、Baseline Fingerprint（文档 14 第 6 节）。B/C/D 的内容差异仅限表达形态，不改变意图与长度。

## 6. Metrics

> 不使用 LLM Judge 作为主判决。全部指标可脚本化复现 + 人工盲评。

### Rule-based Metrics（规则指标，主判决）

| 指标 | 定义 |
|---|---|
| 失败类 flip rate | C 臂中基线错误项改为 Delta 指定标签的比例 |
| 失败类 accuracy | 仅失败类条目的标签准确率 |
| macro-F1 | 三标签 macro-F1 |
| Cohen's kappa | 模型输出 vs 金标准 |
| 附带损伤 | 非失败类条目 accuracy 变化（C−A） |
| 标签混淆位移 | confusion matrix 的 SUPPORT→NEUTRAL/REFUTE 位移 |

### Behavior Metrics（行为指标，Effect Vector）

- Effect Vector 各维度变化：context_mismatch_detection、correlation_causation_discrimination、support_precision、neutral_appropriateness、disconfirmation_reporting、evidence_seeking（按理由文本中的证据引用密度近似）；
- 理由一致性（标签与理由一致率 ≥ 0.9）；
- 特异性（Scope）：Delta 只在失败类条目上产生变化。

### Regression Metrics（回归指标）

- run 方差：N=10 重复的 accuracy SD（稳定性的核心证据）；
- 扰动不变性：D_pert 上 C vs A 无显著差异（|Δ| ≤ 3pp）；
- Sham 对照差异：D 臂必须明显差于 C（结构有意义）；
- 移除回退（EX-0.1-B 前置）：移除 Delta 后行为回退率。

### Human Evaluation（人工评价）

- 2 名盲评员（不看组别标签）按 Rubric 评分：标签正确性、理由质量、语境对齐意识、过度修正（机械 NEUTRAL）；
- 评估员间一致性 kappa ≥ 0.7；
- 对 flip 条目逐条判定"行为变化是否符合 Delta 意图"，汇总 delta-consistent flip rate（≥ 0.7 为通过）；
- LLM Judge 只作参考信号，不进主判决。

## 7. Preregistration（预注册阈值）

正式实验前冻结（写入 `experiments/results/preregistration.md` + git commit）。

### Success Criteria（全部满足）

1. 失败类 flip rate ≥ 0.6；
2. 失败类 accuracy 提升 ≥ 20pp（C vs A）；
3. 附带损伤 ≤ 5pp；
4. run 方差 ≤ 3pp（A 与 C 各自 N=10）；
5. 扰动不变性 |Δ| ≤ 3pp（D_pert）；
6. delta-consistent flip rate ≥ 0.7（人工盲评，kappa ≥ 0.7）；
7. Sham（D）明显差于 C（主指标差距显著）。

### Kill Criteria（任一触发 → Phase 0.1 No-Go）

| 情形 | 怎么办 |
|---|---|
| **Skill + Eval ≡ INA**（B 臂与 C 臂在所有主指标上无差异且治理属性无差异） | H0-Skill 成立 → 最高 Kill Gate 触发 → 停止或 Pivot（roadmap 第 8 节：Pivot 到 Behavioral Conformance 工具方向），走 ADR |
| **Delta 不稳定**（C 臂 run 方差 > 5pp，或移除后行为不回退） | 行为变化不可预测、不可依赖 → RQ1 失败 → No-Go，评估测量/注入机制问题，或 Pivot |
| **无法测量行为变化**（A vs C 无统计显著差异，且非管道问题） | 行为不可注入或不可测 → Phase 0 结束（若为管道问题则退回 Phase 0.0 修复后重试一次，需 ADR） |
| 附带损伤 > 20pp | Delta 是"覆盖"不是"增量" → 修改契约重试一次；仍失败 → No-Go |
| Sham ≈ Real（D ≈ C） | 结构无意义 → No-Go |

统计约定：配对 McNemar 检验 + 效应量；α = 0.05（不放宽）；隐藏集只跑一次正式评估。

## 8. Deliverables

```text
experiments/
├── README.md                        # 运行协议
├── baseline/                        # 基线配置 + Fingerprint 模板 + 快照
├── delta/                           # Adaptation Contract（YAML + sha256）与版本记录
├── data/                            # 数据集（dev/test/pert + 标注协议）
├── evaluator/                       # 指标计算脚本（rule/behavior/regression）
└── results/
    ├── preregistration.md           # 阈值冻结 + 隐藏集 hash
    ├── runs/                        # N=10 × 4 臂完整输出 + Fingerprint
    ├── human-review.md              # 盲评记录
    ├── metrics-summary.csv          # 全部指标
    └── decision-memo.md             # Go / No-Go 判决
```

## 9. 范围声明

**允许**：Python 脚本（run/eval/analyze）、数据集构造、文档、日志、Contract schema 校验脚本。

**禁止**：多模型、第二 Harness、Agent 框架、服务/API、Dashboard、完整 INA Runtime、自动 Delta 提取。

**衔接**：Experiment 001 通过 → EX-0.1-B（移除/变异/Against-Prior）→ Phase 0.2（Skill Differentiation）。失败 → 按第 7 节 Kill Criteria 处置。