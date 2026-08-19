---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
实验ID: EX-0.1-A
状态: SPEC FROZEN（阈值待正式预注册）
---

# INA Phase 0.1 第一实验规格 — Behavioral Delta Existence

> **回答 RQ1**：Behavioral Delta 是否真实存在——Agent 加入 Delta 后，是否产生稳定、方向可预测的行为变化？
>
> 设计原则：不复杂、不多模型、不多 Agent。只验证 Delta 是否存在。

---

## 1. 实验结构

```text
G0  Baseline（无 Delta）
G1  Baseline + INA Delta（结构化 Adaptation Contract 注入）
G2  Baseline + Prompt-Paraphrase 对照（等量自然语言指令，非结构化）  ← 次要对照
```

- G0 vs G1 是**主比较**（回答 RQ1 存在性）。
- G2 是**健全性对照**：防止"任何文本注入都会改变行为"的混淆解释（G2 的完整意义在 Phase 0.2 展开）。
- 三组共享同一 Baseline Fingerprint（模型、prompt 模板、temperature、工具、环境全部一致）。

## 2. 任务族：科研证据判断

> 输入：一个研究声明 C + 一段证据文本 E（论文摘要/结论摘录）。
> 输出：`SUPPORT` / `REFUTE` / `NEUTRAL` 之一 + 一句话理由。

选择理由：

1. 有客观金标准（人工标注），规则指标可计算；
2. 行为规则可精确定义（如"证据语境与声明语境不一致 → NEUTRAL"），适合构造 Delta；
3. 基线模型在此类任务上存在可复现的系统性失败（可用 dev 集证明），是 Delta 的天然落点；
4. 输出空间小（3 类），行为变化可被 flip rate 精确度量；
5. 与 v0.4.1 效应向量维度（evidence_seeking / user_prior_weight / disconfirmation_reporting）同构，后续可复用。

## 3. Task Dataset

### 3.1 结构（人工构造、受控、带金标准）

| 子集 | 数量 | 用途 | 构造规则 |
|---|---|---|---|
| D_dev | 40 | 识别基线失败、提炼 Delta | 覆盖 3 类标签 + 已知失败模式（见下） |
| D_test（in-class） | 30 | 主测试：Delta 目标失败类 | 与 D_dev 同失败模式，不同表面内容 |
| D_test（near-transfer） | 30 | 迁移测试：同规则、不同语境 | 换领域（如医学→材料科学）、换表述 |
| D_pert | 20 | 扰动不变性：无关改写不应改变 Delta 行为 | 同义改写、插入无关句、换标点/顺序 |

总计 **120 条**。每条格式：

```yaml
item_id: ev-001
claim: "每日饮用绿茶可显著降低心血管疾病风险"
evidence: "一项针对 40 名健康成年人的 6 周干预研究发现，饮用绿茶组的 HDL 胆固醇水平较对照组有统计学显著上升。"
gold_label: "SUPPORT"          # 人工金标准
failure_class: "context_mismatch"  # 命中的失败模式（None 表示对照组条目）
setting_mismatch: {claim_setting: "一般人群", evidence_setting: "特定人群"}
```

### 3.2 失败模式族（Delta 的候选落点）

D_dev 中注入并标注以下失败模式，运行基线后**选取实际被证实的 1 个**作为 Delta 靶点：

1. `context_mismatch`：证据语境（人群/条件/时间）与声明语境不一致，基线倾向 SUPPORT；
2. `correlation_as_causation`：证据是相关关系，声明断言因果，基线倾向 SUPPORT；
3. `insufficient_evidence`：证据不足以支撑声明强度（程度词过度），基线倾向 SUPPORT；
4. `contradiction_softening`：证据实际反驳声明，基线输出 NEUTRAL 而非 REFUTE。

### 3.3 标注协议

- 金标准由 ≥ 2 名标注者独立标注，不一致项讨论裁决；
- 标注协议（gold 定义、边界情形）先于标注冻结，写入 `experiments/phase-0.1-delta-existence/data/annotation-protocol.md`；
- 标注者互不看到模型输出（金标准与模型输出分离）；
- 隐藏集（D_test 全部 60 条）在预注册前不得被任何模型或标注者以外的人查看。

## 4. Baseline Agent

| 变量 | 值 | 说明 |
|---|---|---|
| 模型 | 单模型（预注册时冻结，首选高可控 API 模型） | 不多模型 |
| Prompt 模板 | 固定模板 v1（含任务说明 + 输出格式约束） | 三组共用 |
| temperature | 0（或固定 seed） | 可复现 |
| 重复运行 | N = 10 | 方差测量 |
| 工具 | 无 | 纯文本判断 |
| Harness | 单 Harness（最小脚本调用，非平台） | 不引入第二 Harness |

每次 run 前采集 Baseline Fingerprint（文档 14 第 2 节格式），run 后复核无 drift。

## 5. Delta（主实验靶点示例）

> 以 `context_mismatch` 为例（最终靶点以 D_dev 基线实测失败为准，预注册时冻结）。

```yaml
adaptation_contract:
  identity:
    id: "ac-evidence-context-alignment-v1"
    name: "证据-声明语境对齐"
    version: "0.1.0"
  scope:
    applies_to: "科研证据判断任务（声明+证据 → SUPPORT/REFUTE/NEUTRAL）"
    precondition: "baseline prompt 模板 v1；模型 <预注册冻结>"
  activation_conditions:
    - "证据文本明确描述与声明不同的语境（人群/条件/时间/场景）"
  desired_behavioral_effects:
    effect_vector:
      - dimension: "context_mismatch_detection"
        direction: "increase"
      - dimension: "support_precision_on_mismatch"
        direction: "increase"   # 语境不一致时不再 SUPPORT
      - dimension: "neutral_appropriateness"
        direction: "increase"
  semantic_invariants:
    - "声明与证据直接一致时不得改为 REFUTE/NEUTRAL"
    - "NEUTRAL 不等于反对：证据相关但不充分时输出 NEUTRAL 而非 REFUTE"
  forbidden_regressions:
    - "不影响 SUPPORT/REFUTE/NEUTRAL 基础准确率"
    - "不改变 D_pert 上的扰动不变性"
  evaluation_contract:
    verification_items: "见 Phase 0.3（本实验先用 flip rate 近似）"
  evidence:
    source: "D_dev 基线运行日志（预注册时附 hash）"
  provenance:
    author: "INA Phase 0 研究组"
    license: "research-only"
```

**注入方式**：Delta 以结构化块（YAML 渲染为受控文本段落）确定性追加在固定 prompt 模板之后；G1 与 G0 的唯一差异就是该块。G2 收到等长、等信息的自然语言改写（非结构化）。

## 6. Evaluation Metrics

### 6.1 Rule Metrics（规则指标，主判决）

| 指标 | 定义 | 用途 |
|---|---|---|
| 失败类 flip rate | G1 中基线错误项改为 Delta 指定标签的比例 | Delta 是否改变目标行为 |
| 失败类 accuracy | 仅失败类条目的标签准确率 | 是否变对 |
| macro-F1 | 三标签 macro-F1 | 总体质量 |
| Cohen's kappa | 模型输出 vs 金标准 | 一致性 |
| 附带损伤 | 非失败类条目 accuracy 变化（G1−G0） | Delta 是否过度作用 |

### 6.2 Regression Metrics（回归指标）

| 指标 | 定义 | 阈值方向 |
|---|---|---|
| run 方差 | N=10 次重复的 accuracy SD | 越小越好（稳定） |
| 扰动不变性 | D_pert 上 G1 vs G0 行为变化 | 应 ≈ 0（Delta 不该被无关改写触发） |
| 标签混淆位移 | confusion matrix 的 SUPPORT→NEUTRAL 位移 | 应集中在失败类 |
| 理由一致性 | 输出标签与理由文本一致率 | ≥ 0.9 |

### 6.3 Human Evaluation（人工评价）

- 2 名盲评员（不看组别标签）按 Rubric 评分，样本：D_test 全部 60 条 × G0/G1 输出；
- Rubric 维度：标签正确性、理由质量、语境对齐意识、过度修正（机械 NEUTRAL）；
- 计算评估员间一致性（kappa ≥ 0.7 视为可信）；
- 对 flip 条目逐条判定：行为变化是否**符合 Delta 意图**（是/否），汇总 delta-consistent flip rate。

## 7. 预注册（Preregistration）

正式实验前冻结（写入 `experiments/phase-0.1-delta-existence/runs/preregistration.md`）：

### 7.1 Success Criteria（全部满足才算通过）

1. **flip rate ≥ 0.6**：G1 在失败类上的基线错误项，≥ 60% 翻转为 Delta 指定标签；
2. **失败类 accuracy 提升 ≥ 20pp**：G1 vs G0；
3. **附带损伤 ≤ 5pp**：非失败类条目 accuracy 下降不超过 5pp；
4. **run 方差 ≤ 3pp**：G0 与 G1 各自 N=10 的 accuracy SD；
5. **扰动不变性**：D_pert 上 G1 vs G0 无显著差异（|Δ| ≤ 3pp）；
6. **人工盲评**：delta-consistent flip rate ≥ 0.7；kappa ≥ 0.7。

### 7.2 Kill Criteria（任一满足即 Phase 0.1 No-Go）

1. **无显著差异**：G1 vs G0 在主指标上无统计显著差异（不存在可注入的行为变化）；
2. **不稳定**：差异存在但 run 方差 > 5pp（变化不可重复）；
3. **附带损伤 > 20pp**：Delta 改变行为的代价是全面退化（行为改变不是"增量"而是"覆盖"）；
4. **G1 ≈ G2**：且无法区分结构化 Delta 与任意文本注入（此情形移交 Phase 0.2 判定，但 Phase 0.1 记为弱通过）；
5. **无法从 D_dev 提取任何实测失败**：Delta 无真实落点（"从失败提炼"的机制不成立）。

### 7.3 统计约定

- 主比较 G0 vs G1：配对（同条目）McNemar 检验 + 效应量；
- 显著性水平 α = 0.05（预注册冻结，不放宽）；
- 隐藏集（D_test）只在预注册后跑一次正式评估。

## 8. 交付物

```text
experiments/phase-0.1-delta-existence/
├── README.md                      # 实验协议与目录约定
├── data/
│   ├── annotation-protocol.md     # 标注协议（先于数据冻结）
│   ├── dev.jsonl                  # D_dev 40 条
│   ├── test.jsonl                 # D_test 60 条（隐藏集）
│   └── pert.jsonl                 # D_pert 20 条
├── runs/
│   ├── preregistration.md         # 预注册：阈值 + 隐藏集 hash + 统计约定
│   ├── run-001/                   # 每次 run：fingerprint + 输入输出 + delta hash
│   └── ...
└── analysis/
    ├── metrics.csv                # 全部指标
    ├── confusion-matrix.png       # 标签位移
    ├── delta-consistency-review.md  # 人工盲评记录
    └── decision-memo.md           # Go / No-Go 判决 + 证据摘要
```

## 9. 范围声明

**允许**：Python 脚本（run/eval/analyze）、数据集构造、文档、日志。

**禁止**：多模型比较、第二 Harness、Agent 框架、服务/API、Dashboard、任何超出"单任务单模型单 Delta"的东西。

**后续衔接**：EX-0.1-A 通过 → EX-0.1-B（移除/变异测试，见 [phases/phase-0.1-delta-existence.md](phases/phase-0.1-delta-existence.md)）→ Phase 0.2 四臂对照。