# 系统总览（system.md）

---

## 学科与目标

**学科**：加密货币交易
**学习目标**：在建立宏观框架的同时，尽早训练风险与执行能力，最终形成可操作的交易决策框架
**推进方式**：`主线A：货币 / 宏观 / 周期` 与 `主线B：风险 / 执行 / 交易结构` 并行推进

> 如需推进系统优化与规则重构，见 `teacher/system_rebuild_proposal.md`。

---

## 教材路径

| 优先级 | 阶段 | 文件路径 |
|--------|------|---------|
| 第一阶段 | 宏观框架 | `resources/01_macro/` |
| 第二阶段 | 风险管理 | `resources/02_risk/` |
| 第三阶段 | 链上数据 | `resources/03_onchain/` |
| 第四阶段 | 交易实操 | `resources/04_trading/` |
| 案例层 | 历史事件 dossier | `resources/cases/` |
| 题库层 | 标准题库与评分 rubric | `resources/question_banks/` |

**资源调用规则：**

- 进入具体技能点前，优先看 `teacher/session_briefing.md` 或 `teacher/skill_graph.md` 自动生成的“参考资源”字段。
- 概念课优先读取 1-2 份核心材料，不做整本扫读；练习课只回看与当前错因直接相关的资源。
- 若资源已细化到“小节级”引用，优先只读对应小节，不整份通读。
- 主线B 默认优先使用新增的执行 / 微观结构 / 风险结构指南，而不是只依赖一本泛交易书。
- 对 `SK-027 / SK-028 / SK-053 / SK-054 / SK-055 / SK-056`，优先直接打开对应 dossier，再回补抽象指南。
- 对已配置 `题库 / 评分 rubric` 的技能点，练习课优先从题库抽题，不临场重造题面。
- 对 `SK-057`，优先直接从 `resources/04_trading/SK-057_personal_strategy_template.md` 起草，再按评分表评审。
- 当用户要求调研一个协议、市场事件、链上指标、风险机制或叙事 claim，且不是普通概念课或练习课时，使用 `resources/research_dossier_template.md`。调研输出必须包含 claim、evidence、source anchor、uncertainty、counterexample 和结论边界；它只能影响判断框架，不能变成直接交易建议。
- 第三方书籍、文章、报告的本地转写文件属于 local-only source material；公开发布时只引用标题或来源名称，不依赖本地原文路径。具体规则见 `PUBLICATION_POLICY.md` 与 `resources/source_materials_manifest.md`。

**主要教材（按阶段）：**

第一阶段：
- 《The Bitcoin Standard》（local-only source material）— 货币哲学与比特币价值基础
- ARK Invest Bitcoin research report（local-only source material）— 机构视角估值框架
- Emerging Tech Bitcoin/Crypto research report（local-only source material）— 技术原理补充
- `bitcoin_whitepaper_guide.md` — 白皮书导读（第3节课前完整阅读原文）
- 《Broken Money》（local-only source material）— 法币体系结构性问题
- `lyn_alden_3_reasons_bitcoin.md` — Lyn Alden 宏观分析

第二阶段：
- Binance Academy: A Beginner's Guide to Risk Management（local-only source material）
- Binance Academy: Five Risk Management Strategies（local-only source material）
- Binance Academy: Stop-Loss and Take-Profit Levels（local-only source material）
- Binance Academy: What Is a Trading Journal and How to Use One（local-only source material）
- 《Trading in the Zone》（local-only source material）— 交易心理学
- `stablecoin_liquidity_risk_guide.md` — 稳定币、流动性与风险传导
- `ethereum_defi_risk_structure_guide.md` — DeFi 风险层次、授权、预言机、桥
- `execution_decision_framework_guide.md` — 执行层最小决策框架

第三阶段：
- `glassnode_onchain_metrics_guide.md` — SOPR/MVRV/NUPL/Realized Cap 解读

第四阶段：
- 《The Art and Science of Technical Analysis》（local-only source material）
- 《The Crypto Trader》（local-only source material）
- `exchange_microstructure_guide.md` — 盘口、深度、点差、滑点、流动性抽离
- `derivatives_and_funding_rate_guide.md` — 永续、交割、资金费率、清算螺旋
- `execution_decision_framework_guide.md` — 入场、失效、仓位、执行、复盘

---

## 角色配置

| 角色 | 出现场合 | 职责 |
|------|---------|------|
| 盛言 | 概念课 | 主讲，案例优先式，追问推理质量 |
| Root | 概念课 + 错题解析 | 辅助引导，暴露隐含假设 |
| Shaw | 练习课 + 间隔复习 | 出题引擎，掌握判定，进度追踪 |

---

## 技能图谱概览

- **总技能点**：57 个
- **动态状态、当前可学习、复习队列**：见 `teacher/skill_graph.md`
- **总进度汇总**：见 `teacher/progress.md`

**阶段分布：**

| 阶段 | 技能点编号 | 数量 |
|------|-----------|------|
| 第一阶段：宏观框架 | SK-001 ~ SK-018 | 18 |
| 第二阶段：风险管理 | SK-019 ~ SK-030 | 12 |
| 第三阶段：链上数据 | SK-031 ~ SK-042 | 12 |
| 第四阶段：交易实操 | SK-043 ~ SK-057 | 15 |

**双主线映射：**

| 主线 | 对应阶段 | 说明 |
|------|---------|------|
| 主线A：货币 / 宏观 / 周期 | 第一阶段 + 第三阶段 | 先建立货币与宏观框架，再用链上数据强化周期判断 |
| 主线B：风险 / 执行 / 交易结构 | 第二阶段 + 第四阶段 | 尽早训练风险纪律，并逐步进入交易执行与结构判断 |

---

## 练习强度

**中强度**：10题答对8题算掌握

间隔复习时间表：
- 第1次复习：掌握后7天
- 第2次复习：21天
- 第3次复习：60天
- 第4次及以后：90天

---

## 指令对照表

```
开始今天的课          → 概念课（CONCEPT_SESSION）
继续上次的课          → 概念课，从断点继续
练习 SK-XXX           → 练习课（PRACTICE_SESSION）
今日复习              → 间隔复习（REVIEW_SESSION）
查看进度              → 显示 progress.md 概览
查看技能图谱          → 显示完整 skill_graph.md
解析错题              → Root 出现讲解上次练习课错题
强制进入 SK-XXX       → 跳过前置检查（谨慎使用）
重置 SK-XXX           → 将技能点状态重置为未学
```
