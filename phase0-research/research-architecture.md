---
文档版本: 0.1
项目阶段: Phase 0 — Behavioral Evolution Validation
最后更新: 2026-08-18
---

# Phase 0 Architecture Diagram

> 本图描述 **Phase 0 实验架构**，不是产品架构。每个方框都对应一个可运行脚本或一份数据文件。

## 1. 总体实验环

```mermaid
flowchart LR
    subgraph PRE[Phase 0.0 前置]
        PIP[测量管道校准<br/>已知变化注入] --> OK{管道检测到<br/>已知变化？}
        OK -- 否 --> KILL0[Phase 0 结束<br/>无法测量]
        OK -- 是 --> FP[Baseline Fingerprint<br/>冻结机制]
    end

    subgraph RUN[每次实验 run]
        BASE[Baseline Agent<br/>模型 + 固定 prompt 模板]
        FP --> BASE
        DELTA[Adaptation Contract<br/>结构化行为变化]
        APP[Application<br/>确定性注入]
        BASE --> APP
        DELTA --> APP
        APP --> OUT[行为输出<br/>+ trace + 成本]
    end

    subgraph MEAS[测量层]
        OUT --> RULE[规则指标<br/>accuracy / F1 / flip rate]
        OUT --> REG[回归指标<br/>方差 / 扰动不变性 / 附带损伤]
        OUT --> HUMAN[人工盲评<br/>Rubric + kappa]
        OUT --> CONF[Conformance Score<br/>Phase 0.3 引入]
    end

    subgraph DECIDE[判决层]
        RULE --> VERDICT{Go / No-Go<br/>预注册阈值}
        REG --> VERDICT
        HUMAN --> VERDICT
        CONF --> VERDICT
        VERDICT -- Go --> ADOPT[采纳 + 版本化<br/>Delta Registry（git 级）]
        VERDICT -- No-Go --> REVISE[修订 / 拒绝<br/>决策备忘]
    end

    subgraph LOOP[Phase 0.5 闭环（可行性单环）]
        RUN --> TRAJ[轨迹收集]
        TRAJ --> FAIL[失败识别<br/>人工 + 规则]
        FAIL --> EXTRACT[Delta 提取<br/>人工主导]
        EXTRACT --> DELTA
    end

    ADOPT --> REG[Delta Registry<br/>versioned / rollback]
    REG -. Phase 1+ .-> APP
```

## 2. Delta 是什么 / 不是什么

```mermaid
flowchart LR
    subgraph IS[Delta 是]
        A1[显式 artifact<br/>Adaptation Contract]
        A2[固定 Fingerprint 上<br/>可测量行为变化]
        A3[携带 Evaluation Contract<br/>可判定生效]
        A4[身份 / 版本 / 谱系 / 证据]
        A5[可移除、可回滚]
    end
    subgraph NOT[Delta 不是]
        B1[自然语言 Prompt]
        B2[Skill 能力包]
        B3[Memory 事实存储]
        B4[权重更新 / Fine-tuning]
        B5[Trajectory 行为记录]
    end
```

## 3. 组件与 Phase 0 代码边界

| 组件 | Phase 0 形态 | 允许的代码 | 禁止的代码 |
|---|---|---|---|
| Baseline Agent | 单模型 + 固定 prompt 模板 | run 脚本 | Harness 开发 |
| Delta Artifact | YAML / JSON Adaptation Contract | schema 校验脚本 | Schema 编译器 |
| Application | 确定性注入（同模板追加结构化块） | 注入函数 | 服务 |
| Measurement | 指标计算脚本 + 分析 notebook | Python 脚本 | Dashboard |
| Registry | git 目录 + 文件命名约定 | 文件约定 | 数据库服务 |
| Loop | 人工主导提取 + 脚本辅助 | 提取辅助脚本 | 自动 Evolution 系统 |

## 4. 数据流约定

```text
experiments/phase-0.X-*/data/     ← 数据集（JSONL + annotation 协议）
experiments/phase-0.X-*/runs/     ← 每次 run 的输出 + Fingerprint 快照
experiments/phase-0.X-*/analysis/ ← 指标计算、图表、决策备忘
```

任何 run 必须包含：`baseline_fingerprint.yaml` + 输入输出 JSONL + 所用 Delta 的 hash（文档 14 第 2 节）。