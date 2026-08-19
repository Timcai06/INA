---
文档版本: 0.2
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
目录性质: 实验执行目录（仅可行性实验）
---

# experiments/ — INA Phase 0 实验目录

## 这个目录是什么

Phase 0 的**实验执行现场**：数据集、运行记录、指标计算、决策备忘。

只做一件事：**为 Behavioral Delta 的存在性、区分性、可验证性、可迁移性、生命周期收集证据**（RQ1–RQ5）。

## 这个阶段只做可行性实验

- ✅ 允许：数据集构造、单模型 run、指标计算、人工盲评、预注册、决策备忘、最小 Python 脚本
- ❌ 禁止：产品/平台代码、服务、API、Dashboard、Marketplace、Rust Core、分布式系统、自动 Evolution、完整 INA Runtime

> 判断标准：**这里的每样东西都必须服务于一个研究问题的判决。** 不服务于判决的东西不进这个目录。

## 目录布局（对应 Experiment 001 规格）

```text
experiments/
├── README.md                ← 本文件（运行协议）
├── baseline/                ← 基线配置：Baseline Fingerprint 模板与快照
├── delta/                   ← Adaptation Contract（YAML + sha256）与版本记录
├── data/                    ← 数据集（dev/test/pert）+ 标注协议
├── evaluator/               ← 指标计算脚本（rule / behavior / regression）
└── results/                 ← 预注册、run 记录、人工盲评、决策备忘
```

## 运行协议（每个 run 必须满足）

1. **预注册先行**：正式实验前冻结阈值与统计约定（`results/preregistration.md`），git commit；
2. **Fingerprint 必带**：每次 run 前采集 `baseline_fingerprint.yaml`，run 后复核无 drift（文档 14 第 2 节）；无 Fingerprint 的 run 不计入正式统计；
3. **Delta 留 hash**：所用的 Adaptation Contract 以文件保存（`delta/`）并记录 sha256；realization 与 Delta 本体分开记录；
4. **固定 seed**：temperature 0 或固定 seed，可复现；
5. **隐藏集纪律**：D_test 在预注册前不暴露给模型与标注者；
6. **负面结果同权**：失败的 run 与成功的 run 一样保留、一样记录。

## 决策备忘（results/decision-memo.md）模板

每次 Go / No-Go / Pivot 判决必须产出：

```yaml
实验ID:
日期:
判决: Go | No-Go | Pivot
依据:            # 逐条列出预注册阈值 vs 实测值
失败点:          # No-Go 时定位（roadmap 第 8 节）
反方解释:        # 最可能推翻本判决的解释
遗留风险:
需要ADR: 是/否
```

## 与 phase0-research/ 的关系

```text
phase0-research/（阶段计划）定义：做什么、证明什么、何时杀死 → 开工前读
experiments/（实验执行）产出：数据、数字、判决 → 收尾时写
```

规则：**实验结论不得直接修改 phase0-research/ 中的设计；需要改变方向时走 ADR**（`V0.4.1_docs/06-协作模板/15-架构决策记录模板.md`）。