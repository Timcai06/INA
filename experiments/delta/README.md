---
用途: Adaptation Contract 与版本记录
---

# experiments/delta/

存放**Behavioral Delta（Adaptation Contract）**的权威副本：

- `ac-evidence-discipline-v1.yaml` — 第一个 Delta（科研证据判断纪律）
- `ac-evidence-discipline-v1.yaml.sha256` — 内容 hash（每次注入前校验）
- `registry.md` — 版本记录（v1 / v1.1 冲突 / v2…，含 lineage 与 provenance）

规则：

- Delta 本体与 realization（注入渲染）分开记录；
- 任何修改 = 新版本，不允许覆盖历史文件；
- 预注册后修改 Delta 必须重新预注册（或走 ADR）。