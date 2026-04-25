# 加密货币交易学习资源库总览

> 当前资源库已经从“宏观 + 风控 + 链上 + 一本交易书”的基础形态，扩到“宏观 / 风险纪律 / 风险结构 / 链上 / 执行”五个层面。
> 新增整合指南现在默认包含：框架说明 + 完整正例 + 高压反例 + 练习题 + 评分点。
> 关键历史事件已开始落成 `resources/cases/` 下的案例 dossier，供概念课和案例技能直接复用；每份 dossier 现在都应包含“原始证据包”，帮助老师按当时信息集上课。
> 关键技能已开始落成 `resources/question_banks/` 下的标准题库与评分 rubric，供练习课直接抽题。
> 抽象指南中的核心链路现在优先配结构图（mermaid），上课时可直接拿图解释机制，不必只靠口头描述。
> 使用原则：先按技能点读取 `teacher/session_briefing.md` 或 `teacher/skill_graph.md` 中的“参考资源”，再回到本文件找具体材料。
> 发布原则：公开仓库默认只发布自有教学材料、案例、题库和索引；第三方书籍、文章、报告的本地转写文件属于 local-only source material，见 `resources/source_materials_manifest.md` 与 `PUBLICATION_POLICY.md`。

---

## 目录结构

| 目录 | 主要主题 | 当前定位 |
|------|---------|---------|
| `resources/01_macro/` | 货币、通胀、比特币货币逻辑、宏观周期 | 主线A 基础层 |
| `resources/02_risk/` | 风险管理、托管风险、稳定币、DeFi 风险 | 主线B 风险结构层 |
| `resources/03_onchain/` | 链上指标、周期读数、估值框架 | 主线A 周期强化层 |
| `resources/04_trading/` | 衍生品、微观结构、执行决策、交易实操 | 主线B 执行层 |
| `resources/cases/` | 历史事件 dossier | 关键案例的完整教学包 |
| `resources/question_banks/` | 标准题库与评分 rubric | 关键技能的练习入口 |
| `resources/case_library_index.md` | 概念课案例索引（含难度分层） | 跨主线案例入口 |

---

## 公开可发布资源索引

### 1. 宏观 / 货币基础

| 文件 | 类型 | 适用技能 | 用途 |
|------|------|---------|------|
| `bitcoin_whitepaper_guide.md` | 导读 | SK-006 ~ SK-010 | 白皮书、PoW、UTXO、网络结构 |
| `lyn_alden_3_reasons_bitcoin.md` | 文章导读 | SK-001 ~ SK-005 | 货币属性、比特币定位、宏观连接 |

### 2. 风险纪律 / 风险结构

| 文件 | 类型 | 适用技能 | 用途 |
|------|------|---------|------|
| `stablecoin_liquidity_risk_guide.md` | 新增整合指南 | SK-019、SK-027、SK-028、SK-055 | 稳定币、流动性断裂、风险传导 |
| `ethereum_defi_risk_structure_guide.md` | 新增整合指南 | SK-028、SK-029、SK-055 | DeFi 风险层次、授权、桥、预言机 |

### 3. 链上周期

| 文件 | 类型 | 适用技能 | 用途 |
|------|------|---------|------|
| `glassnode_onchain_metrics_guide.md` | 整合指南 | SK-031 ~ SK-042、SK-052 ~ SK-056 | MVRV / SOPR / NUPL / Realized Cap |

### 4. 执行 / 微观结构 / 衍生品

| 文件 | 类型 | 适用技能 | 用途 |
|------|------|---------|------|
| `exchange_microstructure_guide.md` | 新增整合指南 | SK-027、SK-043、SK-045、SK-056 | 盘口、深度、滑点、闪崩 |
| `derivatives_and_funding_rate_guide.md` | 新增整合指南 | SK-026、SK-043、SK-044、SK-056 | 永续、交割、资金费率、清算螺旋 |
| `execution_decision_framework_guide.md` | 新增整合指南 | SK-019 ~ SK-030、SK-045、SK-050、SK-051、SK-057 | 从假设到下单、退出、复盘的执行链 |
| `SK-057_personal_strategy_template.md` | 模板 | SK-057 | 毕业策略文档的可填写模板 |

### 5. 案例 Dossier

| 文件 | 类型 | 适用技能 | 用途 |
|------|------|---------|------|
| `ww2_pow_cigarette_money_dossier.md` | 案例档案 | SK-001、SK-002 | 商品货币、三个职能、六个属性 |
| `1933_gold_confiscation_dossier.md` | 案例档案 | SK-002、SK-003 | 可携带性、可得性与政策约束 |
| `1871_rai_stones_dossier.md` | 案例档案 | SK-001 ~ SK-003 | 所有权记账、可携带性边界 |
| `1971-08_nixon_shock_dossier.md` | 案例档案 | SK-001 ~ SK-005 | 美元脱锚、价值储存与制度约束 |
| `2020-2022_monetary_expansion_inflation_dossier.md` | 案例档案 | SK-004 | 货币扩张、资产先涨与 CPI 传导 |
| `decision_quality_vs_result_quality_dossier.md` | 案例档案 | SK-019 | 决策质量 vs 结果质量 |
| `2022-11_ftx_bank_run_dossier.md` | 案例档案 | SK-027 | 托管风险、可得性与信用挤兑 |
| `mango_markets_oracle_manipulation_dossier.md` | 案例档案 | SK-028 | 预言机操纵、多层攻击面与机制失效 |
| `spot_perpetual_delivery_execution_dossier.md` | 案例档案 | SK-043 | 现货、永续、交割工具选择 |
| `2023-10_btc_three_framework_decision_dossier.md` | 案例档案 | SK-052 | 宏观、链上、结构三框架协同 |
| `2022-05_ust_luna_depeg_dossier.md` | 案例档案 | SK-055 | 脱锚、赎回链与死亡螺旋 |
| `2020-03-12_btc_liquidity_crash_dossier.md` | 案例档案 | SK-053 | 流动性危机、恐慌出清与三层判断 |
| `2021-11-08_btc_cycle_top_dossier.md` | 案例档案 | SK-054 | 顶部信号、分发与离场纪律 |
| `2025-10_crypto_flash_crash_dossier.md` | 案例档案 | SK-043、SK-056 | 杠杆拥挤、薄盘口与清算螺旋 |

### 6. 题库 / 评分 Rubric

| 文件 | 类型 | 适用技能 | 用途 |
|------|------|---------|------|
| `SK-004_inflation_mechanism_bank.md` | 题库 | SK-004 | 通胀传导链辨析与案例判断 |
| `SK-019_probability_vs_result_bank.md` | 题库 | SK-019 | 决策质量 vs 结果质量训练 |
| `SK-020_cognitive_bias_bank.md` | 题库 | SK-020 | 交易偏差识别与复盘改写 |
| `SK-021_expectancy_bank.md` | 题库 | SK-021 | 期望值、胜率与赔率计算 |
| `SK-022_023_position_risk_bank.md` | 题库 | SK-022、SK-023 | 风险金额、仓位与 1% 法则 |
| `SK-024_025_exit_rules_bank.md` | 题库 | SK-024、SK-025 | 止损、止盈与风险收益比 |
| `SK-026_liquidation_mechanism_bank.md` | 题库 | SK-026 | 爆仓机制、杠杆与强平边界 |
| `SK-027_custody_risk_bank.md` | 题库 | SK-027 | 托管风险、提现与资产可得性 |
| `SK-028_defi_protocol_risk_bank.md` | 题库 | SK-028 | DeFi 分层攻击面 |
| `SK-029_030_opsec_journal_bank.md` | 题库 | SK-029、SK-030 | OpSec、授权、交易日志与复盘 |
| `SK-031_042_onchain_metrics_bank.md` | 题库 | SK-031 ~ SK-042 | 链上指标定义、联合读法与周期复盘 |
| `SK-043_instrument_choice_bank.md` | 题库 | SK-043 | 工具选择、路径与风险结构 |
| `SK-044_051_execution_toolkit_bank.md` | 题库 | SK-044 ~ SK-051 | 资金费率、滑点、技术结构与执行规则 |
| `SK-052_three_framework_synthesis_bank.md` | 题库 | SK-052 | 三框架协同判断与分层处理 |
| `SK-053_056_case_synthesis_bank.md` | 题库 | SK-053 ~ SK-056 | 重大案例综合复盘 |

---

## 本轮新增重点专题

1. `resources/04_trading/exchange_microstructure_guide.md`
   解决“看得见价格，看不见流动性”的问题。
2. `resources/04_trading/derivatives_and_funding_rate_guide.md`
   把杠杆、永续、资金费率、爆仓机制接到同一框架里。
3. `resources/02_risk/stablecoin_liquidity_risk_guide.md`
   补齐稳定币、赎回、脱锚、传导链。
4. `resources/02_risk/ethereum_defi_risk_structure_guide.md`
   补齐智能合约之外的 DeFi 风险层次。
5. `resources/04_trading/execution_decision_framework_guide.md`
   把交易从“判断方向”推进到“定义失效、计算仓位、执行和复盘”。
6. `resources/case_library_index.md`
   给概念课补一层“技能点 -> 入门 / 标准 / 高压反例”案例入口。
7. `resources/cases/`
   给关键案例技能补一层可直接开课的 dossier。
8. `resources/question_banks/`
   给关键技能补一层可直接练习和判分的标准题库。
9. `resources/04_trading/SK-057_personal_strategy_template.md`
   给毕业综合补一份可直接提交和评审的策略文档模板。

---

## 建议使用顺序

1. 新进主线A 时，先用 `01_macro` 打底，再接 `03_onchain`。
2. 新进主线B 时，先用 `execution_decision_framework_guide.md` 建立执行骨架。
3. 涉及交易所、滑点、闪崩时，补 `exchange_microstructure_guide.md`。
4. 涉及杠杆、永续、资金费率、强平时，补 `derivatives_and_funding_rate_guide.md`。
5. 涉及 FTX / LUNA / DeFi / 托管与授权风险时，优先读 `02_risk` 新增专题。
6. 进入 `SK-001 ~ SK-004 / SK-019 / SK-027 / SK-028 / SK-043 / SK-052 ~ SK-056` 时，优先直接打开对应 dossier。
7. 进入 `SK-004 / SK-019 ~ SK-056` 的练习课时，优先先看对应题库 / 评分 rubric；链上和执行段使用合并题库覆盖相邻技能。
8. 进入 `SK-057` 时，先读评分表，再直接从 `SK-057_personal_strategy_template.md` 起草，不要从空白文档开始。

---

## 本地原始资料索引

以下材料可作为教师备课参考，但默认不进入公开仓库；公开文档只引用标题或来源名称，不依赖本地原文路径。

| 公开引用方式 | 类型 | 适用技能 | 用途 |
|-------------|------|---------|------|
| 《The Bitcoin Standard》 | local-only 书籍来源 | SK-001 ~ SK-004 | 健全货币、货币史、属性框架 |
| 《Broken Money》 | local-only 书籍来源 | SK-001 ~ SK-005、SK-011 ~ SK-018 | 通胀、法币结构、跨国货币问题 |
| ARK Invest Bitcoin research report | local-only 研究报告来源 | SK-004、SK-011 ~ SK-018、SK-031 ~ SK-042 | 宏观与机构视角的周期框架 |
| Emerging Tech Bitcoin/Crypto research report | local-only 研究报告来源 | SK-006 ~ SK-010 | 技术原理补充 |
| Binance Academy: A Beginner's Guide to Risk Management | local-only 文章来源 | SK-019 ~ SK-026 | 风险管理基础 |
| Binance Academy: Five Risk Management Strategies | local-only 文章来源 | SK-021 ~ SK-026 | 风险纪律与仓位框架 |
| Binance Academy: Stop-Loss and Take-Profit Levels | local-only 文章来源 | SK-023 ~ SK-025 | 止损止盈与赔率 |
| Binance Academy: What Is a Trading Journal and How to Use One | local-only 文章来源 | SK-030、SK-057 | 交易日志与复盘 |
| 《Trading in the Zone》 | local-only 书籍来源 | SK-019 ~ SK-030 | 概率思维、结果导向、纪律 |
| 《Cryptoassets》 | local-only 书籍来源 | SK-031 ~ SK-042 | 链上估值与资产框架 |
| 《The Art and Science of Technical Analysis》 | local-only 书籍来源 | SK-046 ~ SK-057 | 技术结构、执行与风险收益 |
| 《The Crypto Trader》 | local-only 书籍来源 | SK-043 ~ SK-057 | 加密交易案例与执行 |

---

## 资源统计

- 宏观 / 货币公开教学材料：2 份
- 风险纪律 / 风险结构公开教学材料：2 份
- 链上周期公开教学材料：1 份
- 执行 / 微观结构 / 衍生品公开教学材料：4 份
- 案例 dossier：14 份
- 题库 / 评分 rubric：15 份
- 索引 / 发布治理文档：3 份
- local-only 原始资料：12 份

**公开可发布教学材料：41 份；本地原始资料：12 份。**

公开可发布教学材料包含当前文件、`resources/case_library_index.md` 与 `resources/source_materials_manifest.md`；local-only 原始资料默认由 `.gitignore` 排除。
