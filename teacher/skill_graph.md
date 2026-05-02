# 技能图谱（skill_graph.md）

> 本文件的技能明细是系统唯一状态权威。
> 概览、当前可学习技能、掌握记录、今日延迟验证、今日复习队列、间隔复习时间表由 `python3 tools/learning_state.py sync` 自动重建。
> `概念课完成` 字段会结合 `homework_log.md` 与 `session_archive.md` 自动补齐重修日期。
> `首次掌握日期` 与 `最近达标日期` 会结合 `homework_log.md` 自动校正。
> `主要参考资源` 会按技能点自动映射到资源库中的核心材料。
> 不要手动编辑状态字段，通过指令操作。

---

## 概览

| 项目 | 数值 |
|------|------|
| 总技能点数 | 57 |
| 已掌握 | 3 |
| 待延迟验证 | 0 |
| 学习中 | 0 |
| 未解锁 | 52 |
| 今日延迟验证到期 | 0 |
| 今日复习到期 | 3 |
| 今日调度策略 | 默认冻结新课 |

---

## 当前可学习的技能点

（按双主线展示；前置技能已掌握，或无前置依赖）

### 主线A：货币 / 宏观 / 周期

> 先建立货币与宏观框架，再用链上数据强化周期判断。

- SK-004：通货膨胀的机制

### 主线B：风险 / 执行 / 交易结构

> 尽早训练风险纪律，并逐步进入交易执行与结构判断。

- SK-019：概率思维 vs 结果导向

> 今日调度策略：默认冻结新课
> 当前有 3 个技能点复习到期。默认冻结新课，先清理复习债；只有用户明确要求时才打破。
> 当前系统日期：2026-05-02。

---

## 技能点目录

> 格式说明：每次练习课后，Claude Code 更新"状态"、"最后练习"、"历史准确率"、"复习到期"；掌握相关日期由日志自动回算；"主要参考资源" 按技能点自动映射。
> 掌握标准：中强度，10题答对8题。

---

## 第一阶段：宏观框架（SK-001 ~ SK-018）

---

### SK-001：货币的三个职能

- **描述**：能准确说明交换媒介、价值储存、记账单位三个职能，并能举例区分
- **前置技能**：无
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-001_003_money_foundations_bank.md`；`resources/cases/ww2_pow_cigarette_money_dossier.md`；`resources/cases/1933_gold_confiscation_dossier.md`；`resources/cases/1871_rai_stones_dossier.md`；`resources/cases/1971-08_nixon_shock_dossier.md`；《The Bitcoin Standard》；《Broken Money》；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：✅ 已掌握
- **概念课完成**：2026-04-07
- **首次掌握日期**：2026-03-09
- **最近达标日期**：2026-04-07
- **延迟验证到期**：—
- **延迟验证通过日期**：2026-04-07
- **最后练习**：2026-04-07
- **历史准确率**：[10/10, 7/10, 4/6, 7/10, 5/10, 8/10]
- **复习到期**：2026-04-14
- **复习轮次**：0

---

### SK-002：货币的六个属性

- **描述**：能列举并解释稀缺、耐久、便携、可分、可验、可替换六个属性，并用它们评价任意一种货币
- **前置技能**：SK-001
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-001_003_money_foundations_bank.md`；`resources/cases/ww2_pow_cigarette_money_dossier.md`；`resources/cases/1933_gold_confiscation_dossier.md`；`resources/cases/1871_rai_stones_dossier.md`；`resources/cases/1971-08_nixon_shock_dossier.md`；《The Bitcoin Standard》；《Broken Money》；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：✅ 已掌握
- **概念课完成**：2026-03-12（重修 2026-04-07，重修2 2026-04-08）
- **首次掌握日期**：2026-04-08
- **最近达标日期**：2026-04-08
- **延迟验证到期**：—
- **延迟验证通过日期**：2026-04-08
- **最后练习**：2026-04-08
- **历史准确率**：[6/10, 4/10, 6/10, 5/10, 7/10, 9/10]
- **复习到期**：2026-04-15
- **复习轮次**：0

---

### SK-003：健全货币 vs 不健全货币的判定标准

- **描述**：给定一种货币，能用六属性框架判断其健全程度，并说明最薄弱的属性是哪条
- **前置技能**：SK-002
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-001_003_money_foundations_bank.md`；`resources/cases/ww2_pow_cigarette_money_dossier.md`；`resources/cases/1933_gold_confiscation_dossier.md`；`resources/cases/1871_rai_stones_dossier.md`；`resources/cases/1971-08_nixon_shock_dossier.md`；《The Bitcoin Standard》；《Broken Money》；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：✅ 已掌握
- **概念课完成**：2026-04-08（重修 2026-04-09）
- **首次掌握日期**：2026-04-09
- **最近达标日期**：2026-04-09
- **延迟验证到期**：—
- **延迟验证通过日期**：2026-04-09
- **最后练习**：2026-04-09
- **历史准确率**：[7/10, 6/10, 8/10]
- **复习到期**：2026-04-16
- **复习轮次**：0

---

### SK-004：通货膨胀的机制

- **描述**：能解释货币供给增加如何通过购买力稀释传导到物价，区分货币通胀与价格通胀
- **前置技能**：SK-003
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/2020-2022_monetary_expansion_inflation_dossier.md`；`resources/question_banks/SK-004_inflation_mechanism_bank.md`；《Broken Money》（见“法币稀释与购买力传导”相关章节）；ARK Invest Bitcoin research report（local-only source material；见“流动性先推升资产、再传导到消费”相关段落）
- **状态**：⬜ 未学
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-005：法币体系的结构性缺陷

- **描述**：能说明法币的信任依赖和无上限发行两个核心缺陷，并联系SK-003的健全货币标准
- **前置技能**：SK-004
- **掌握标准**：10题答对8题
- **主要参考资源**：《Broken Money》；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`；ARK Invest Bitcoin research report（local-only source material）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-006：双花问题的定义及传统解法

- **描述**：能解释什么是双花问题，以及传统数字支付为何必须依赖中介才能解决
- **前置技能**：SK-005
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/01_macro/bitcoin_whitepaper_guide.md`；Emerging Tech Bitcoin/Crypto research report（local-only source material）；《The Bitcoin Standard》
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-007：区块链如何解决双花

- **描述**：能解释分布式账本的结构，说明为什么去中心化账本可以在没有中介的情况下防止双花
- **前置技能**：SK-006
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/01_macro/bitcoin_whitepaper_guide.md`；Emerging Tech Bitcoin/Crypto research report（local-only source material）；《The Bitcoin Standard》
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-008：工作量证明：矿工的角色与激励机制

- **描述**：能解释矿工做什么、为什么诚实挖矿比攻击网络更有利可图
- **前置技能**：SK-007
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/01_macro/bitcoin_whitepaper_guide.md`；Emerging Tech Bitcoin/Crypto research report（local-only source material）；《The Bitcoin Standard》
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-009：UTXO 模型

- **描述**：能解释比特币如何用UTXO追踪所有权，与账户模型的核心区别是什么
- **前置技能**：SK-007
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/01_macro/bitcoin_whitepaper_guide.md`；Emerging Tech Bitcoin/Crypto research report（local-only source material）；《The Bitcoin Standard》
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-010：21万枚硬上限的来源及货币学含义

- **描述**：能解释2100万上限如何被编码进协议，以及它对货币属性的意义
- **前置技能**：SK-008
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/01_macro/bitcoin_whitepaper_guide.md`；Emerging Tech Bitcoin/Crypto research report（local-only source material）；《The Bitcoin Standard》
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-011：私钥 / 公钥 / 地址的关系与安全逻辑

- **描述**：能说明三者的派生关系，解释为什么丢失私钥意味着永久失去比特币
- **前置技能**：SK-009
- **掌握标准**：10题答对8题
- **主要参考资源**：《Broken Money》；ARK Invest Bitcoin research report（local-only source material）；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-012：减半机制

- **描述**：能解释减半是什么、何时触发（每21万个区块）、每次减半后供给如何变化
- **前置技能**：SK-010
- **掌握标准**：10题答对8题
- **主要参考资源**：《Broken Money》；ARK Invest Bitcoin research report（local-only source material）；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-013：减半周期的价格传导逻辑

- **描述**：能用供给冲击→需求不变→价格上升的逻辑链解释减半与价格的关系，并能指出该逻辑的局限
- **前置技能**：SK-012
- **掌握标准**：10题答对8题
- **主要参考资源**：《Broken Money》；ARK Invest Bitcoin research report（local-only source material）；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-014：Stock-to-Flow 比率

- **描述**：能计算S2F比率，对比比特币与黄金的S2F值，并解释该指标的含义与争议
- **前置技能**：SK-013
- **掌握标准**：10题答对8题
- **主要参考资源**：《Broken Money》；ARK Invest Bitcoin research report（local-only source material）；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-015：比特币四个历史周期的共同结构

- **描述**：能描述上涨→过热→崩盘→积累四阶段的共同特征，并能对应到历史时间线
- **前置技能**：SK-013
- **掌握标准**：10题答对8题
- **主要参考资源**：《Broken Money》；ARK Invest Bitcoin research report（local-only source material）；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-016：网络效应与比特币市场占有率

- **描述**：能解释比特币的网络效应如何形成护城河，以及为什么山寨币在价值储存叙事上难以取代它
- **前置技能**：SK-010
- **掌握标准**：10题答对8题
- **主要参考资源**：《Broken Money》；ARK Invest Bitcoin research report（local-only source material）；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-017：宏观因素对比特币的影响

- **描述**：能解释利率变化、QE周期、风险资产相关性如何影响比特币价格，举出具体历史案例
- **前置技能**：SK-015
- **掌握标准**：10题答对8题
- **主要参考资源**：《Broken Money》；ARK Invest Bitcoin research report（local-only source material）；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-018：机构视角的比特币估值框架

- **描述**：能解释TAM模型和黄金对标两种估值逻辑，说明各自的假设前提和局限性
- **前置技能**：SK-014, SK-017
- **掌握标准**：10题答对8题
- **主要参考资源**：《Broken Money》；ARK Invest Bitcoin research report（local-only source material）；`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

## 第二阶段：风险管理（SK-019 ~ SK-030）

---

### SK-019：概率思维 vs 结果导向

- **描述**：能区分决策质量与结果质量，解释为什么好决策可能产生坏结果，给出实际交易例子
- **前置技能**：无
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/decision_quality_vs_result_quality_dossier.md`；`resources/question_banks/SK-019_probability_vs_result_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-019：概率思维 vs 结果导向”）；《Trading in the Zone》（见“决策质量独立于结果质量”相关章节）
- **状态**：⬜ 未学
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-020：交易中的主要认知偏差

- **描述**：能识别FOMO、损失厌恶、确认偏误在具体交易场景中的表现，并说明各自如何扭曲决策
- **前置技能**：SK-019
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-020_cognitive_bias_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-020：交易中的主要认知偏差”）；《Trading in the Zone》（见“概率思维、情绪与偏差”相关章节）；Binance Academy: A Beginner's Guide to Risk Management（local-only source material；见风险纪律与行为偏差部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-021：期望值计算

- **描述**：给定胜率和盈亏比，能计算一笔交易的期望值，并判断是否值得入场
- **前置技能**：SK-019
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-021_expectancy_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-021：期望值”）；《Trading in the Zone》（见期望值、样本量与结果噪音相关章节）；Binance Academy: A Beginner's Guide to Risk Management（local-only source material；见风险回报与长期生存部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-022：仓位大小 vs 风险金额的区别

- **描述**：能清晰说明仓位大小（买了多少币）与风险金额（最多亏多少钱）是两个不同概念，不可混淆
- **前置技能**：SK-021
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-022_023_position_risk_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-021：期望值”“SK-022 / SK-023：风险金额与仓位”“SK-024 / SK-025：止损与止盈”）；Binance Academy: Stop-Loss and Take-Profit Levels（local-only source material；见止损距离与风险收益比部分）；Binance Academy: Five Risk Management Strategies（local-only source material；见单笔风险与账户保护部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-023：1% 法则：仓位计算

- **描述**：给定账户规模、止损距离，能用1%法则计算正确仓位大小
- **前置技能**：SK-022
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-022_023_position_risk_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-021：期望值”“SK-022 / SK-023：风险金额与仓位”“SK-024 / SK-025：止损与止盈”）；Binance Academy: Stop-Loss and Take-Profit Levels（local-only source material；见止损距离与风险收益比部分）；Binance Academy: Five Risk Management Strategies（local-only source material；见单笔风险与账户保护部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-024：止损的设置原理

- **描述**：能解释止损为什么必须在入场前设定，以及入场后再设止损的心理陷阱
- **前置技能**：SK-023
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-024_025_exit_rules_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-024 / SK-025：止损与止盈”）；Binance Academy: Stop-Loss and Take-Profit Levels（local-only source material；见止损、止盈与风险收益比部分）；Binance Academy: Five Risk Management Strategies（local-only source material；见退出纪律与风险控制部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-025：止盈的设置原理与风险收益比

- **描述**：能解释1:2和1:3风险收益比的含义，并在给定止损距离时计算对应的止盈位
- **前置技能**：SK-024
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-024_025_exit_rules_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-024 / SK-025：止损与止盈”）；Binance Academy: Stop-Loss and Take-Profit Levels（local-only source material；见止损、止盈与风险收益比部分）；Binance Academy: Five Risk Management Strategies（local-only source material；见退出纪律与风险控制部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-026：爆仓机制：强制平仓价格计算

- **描述**：给定入场价、杠杆倍数、保证金，能计算爆仓价；能解释为什么爆仓不等于亏完本金
- **前置技能**：SK-023
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-026_liquidation_mechanism_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-026：爆仓机制与生存边界”）；`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“实战检查表”与爆仓机制相关段落）；Binance Academy: Five Risk Management Strategies（local-only source material；见账户保护与连续亏损控制部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-027：托管风险：CEX 破产的影响

- **描述**：能解释中心化交易所持有用户资产的结构，用FTX案例说明平台破产时用户面临什么风险
- **前置技能**：SK-019
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/2022-11_ftx_bank_run_dossier.md`；`resources/question_banks/SK-027_custody_risk_bank.md`；`resources/04_trading/exchange_microstructure_guide.md`（见“理解盘口的第一原则”和“CEX 余额不等于链上托管”相关段落）；`resources/02_risk/stablecoin_liquidity_risk_guide.md`（见交易对手方与流动性断裂传导部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-028：智能合约风险：DeFi 协议漏洞

- **描述**：能说明智能合约漏洞的主要类型（重入攻击、预言机操纵等），以及普通用户如何规避
- **前置技能**：SK-027
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/mango_markets_oracle_manipulation_dossier.md`；`resources/question_banks/SK-028_defi_protocol_risk_bank.md`；`resources/02_risk/ethereum_defi_risk_structure_guide.md`（见预言机、授权、桥与协议分层风险部分）；`resources/02_risk/stablecoin_liquidity_risk_guide.md`（见机制失效如何向市场扩散部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-029：OpSec 基础

- **描述**：能识别钓鱼攻击、SIM换卡、恶意合约授权三类威胁的特征，并说明对应的防护措施
- **前置技能**：SK-027
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-029_030_opsec_journal_bank.md`；`resources/02_risk/ethereum_defi_risk_structure_guide.md`（见授权、前端钓鱼、桥与钱包暴露面部分）；`resources/02_risk/stablecoin_liquidity_risk_guide.md`（见交易对手方与链上转移风险部分）；`resources/04_trading/execution_decision_framework_guide.md`（见“复盘时必须问的四个问题”）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-030：交易日志的建立与复盘方法

- **描述**：能说明交易日志应记录哪些字段，以及如何用日志识别自身的系统性错误模式
- **前置技能**：SK-025
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-029_030_opsec_journal_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-030：交易日志”与“复盘时必须问的四个问题”）；Binance Academy: What Is a Trading Journal and How to Use One（local-only source material；见日志字段与复盘用途部分）；《Trading in the Zone》（见复盘纪律与情绪记录相关章节）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

## 第三阶段：链上数据（SK-031 ~ SK-042）

---

### SK-031：链上数据的本质

- **描述**：能解释链上数据测量的是什么（链上行为），不能测量什么（场外、CEX内部转账），以及这对指标解读的意义
- **前置技能**：SK-009
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-032：Realized Cap 的定义与计算逻辑

- **描述**：能解释Realized Cap的计算方式（每枚BTC按最后移动时的价格计算），以及它和Market Cap的本质区别
- **前置技能**：SK-031
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-033：Market Cap vs Realized Cap 的差值含义

- **描述**：能解释两者差值代表全网未实现盈亏，说明差值极大和极小时各自意味着什么市场状态
- **前置技能**：SK-032
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-034：MVRV 比率

- **描述**：能给出MVRV的计算公式，解释高值（>3.5）和低值（<1）的市场含义，对应到历史周期顶底
- **前置技能**：SK-033
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-035：MVRV-Z Score

- **描述**：能解释为什么要对MVRV做标准化处理，以及历史极值区间（>7为顶部，<0为底部）的统计含义
- **前置技能**：SK-034
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-036：NUPL：全网未实现净盈亏

- **描述**：能说明NUPL的五个区间（投降/希望/乐观/信念/欣快），并对应到牛熊市不同阶段
- **前置技能**：SK-033
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-037：SOPR 的定义与基础含义

- **描述**：能解释SOPR的计算方式（卖出价/买入价），以及>1代表获利卖出、<1代表亏损卖出的含义
- **前置技能**：SK-031
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-038：SOPR 在牛市与熊市的不同读法

- **描述**：能解释牛市中SOPR回踩1.0是支撑信号、熊市中SOPR被1.0压制是阻力信号这两种截然相反的解读
- **前置技能**：SK-037
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-039：LTH vs STH 的分类标准与行为差异

- **描述**：能说明155天的分类门槛，解释LTH和STH在市场顶底的典型行为模式差异
- **前置技能**：SK-034
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-040：三指标联合读法

- **描述**：给定一个时间点的MVRV、NUPL、SOPR数值，能综合判断当前处于周期哪个阶段，说明三者是否一致
- **前置技能**：SK-035, SK-036, SK-038
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-041：链上数据的局限性

- **描述**：能识别洗盘交易和交易所内部转账对链上数据的干扰，以及哪些场景下链上数据会失真
- **前置技能**：SK-040
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-042：复盘练习：用链上数据还原2020-2022周期

- **描述**：能用MVRV/NUPL/SOPR定位2020年3月底部、2021年4月局部顶、2021年11月周期顶、2022年6月底部各时间点的指标状态
- **前置技能**：SK-040, SK-041
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-031_042_onchain_metrics_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；《Cryptoassets》（见链上估值与市场周期相关章节）；ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

## 第四阶段：交易实操（SK-043 ~ SK-057）

---

### SK-043：现货、永续合约、交割合约的核心区别

- **描述**：能从持仓成本、到期机制、风险结构三个维度说明三种工具的区别，以及各自适合什么场景
- **前置技能**：SK-026
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/spot_perpetual_delivery_execution_dossier.md`；`resources/question_banks/SK-043_instrument_choice_bank.md`；`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“SK-043：现货、永续、交割”）；`resources/04_trading/exchange_microstructure_guide.md`（见“SK-043：现货、永续合约、交割合约”）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-044：资金费率

- **描述**：能解释资金费率的锚定机制，说明正负资金费率各自意味着什么市场状态，以及极端资金费率作为情绪指标的含义
- **前置技能**：SK-043
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-044_051_execution_toolkit_bank.md`；`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“SK-044：资金费率”）；`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”中的 Trigger / Execution）；`resources/04_trading/exchange_microstructure_guide.md`（见“理解盘口的第一原则”）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-045：流动性与滑点

- **描述**：给定交易规模和市场深度，能判断是否应该用市价单，以及限价单在什么情况下必须优先
- **前置技能**：SK-043
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-044_051_execution_toolkit_bank.md`；`resources/04_trading/exchange_microstructure_guide.md`（见“SK-045：流动性与滑点”）；`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“实战检查表”）；`resources/04_trading/execution_decision_framework_guide.md`（见“最小下单模板”与 Execution）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-046：支撑位与阻力位的识别

- **描述**：能在K线图上识别有效支撑和阻力，解释价格为什么在这些位置停顿（历史成交密集、心理整数关口等）
- **前置技能**：SK-015
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-044_051_execution_toolkit_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”“最小下单模板”）；《The Art and Science of Technical Analysis》（见结构、量价与形态相关章节）；《The Crypto Trader》（见执行计划与案例复盘相关章节）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-047：成交量分析

- **描述**：能识别量价关系的四种基本组合（量增价涨/量减价涨/量增价跌/量减价跌），并说明各自的含义
- **前置技能**：SK-046
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-044_051_execution_toolkit_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”“最小下单模板”）；《The Art and Science of Technical Analysis》（见结构、量价与形态相关章节）；《The Crypto Trader》（见执行计划与案例复盘相关章节）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-048：移动平均线

- **描述**：能计算MA，解释金叉死叉的信号含义，同时说明为什么MA在震荡市中频繁产生假信号
- **前置技能**：SK-046
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-044_051_execution_toolkit_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”“最小下单模板”）；《The Art and Science of Technical Analysis》（见结构、量价与形态相关章节）；《The Crypto Trader》（见执行计划与案例复盘相关章节）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-049：K线形态：有效信号与被高估的信号

- **描述**：能区分有统计支撑的K线形态（如吞没形态）和被散户高估的形态，说明形态必须结合成交量才有效
- **前置技能**：SK-047
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-044_051_execution_toolkit_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”“最小下单模板”）；《The Art and Science of Technical Analysis》（见结构、量价与形态相关章节）；《The Crypto Trader》（见执行计划与案例复盘相关章节）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-050：入场条件的定义

- **描述**：能将"感觉要涨了"转化为可执行的规则化入场条件（价格条件+成交量条件+周期确认），不依赖感觉
- **前置技能**：SK-025, SK-049
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-044_051_execution_toolkit_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”“最小下单模板”）；《The Art and Science of Technical Analysis》（见结构、量价与形态相关章节）；《The Crypto Trader》（见执行计划与案例复盘相关章节）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-051：出场条件的定义

- **描述**：能说明固定止损、固定止盈、追踪止损三种出场策略的适用场景和各自的权衡
- **前置技能**：SK-050
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/question_banks/SK-044_051_execution_toolkit_bank.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”“最小下单模板”）；《The Art and Science of Technical Analysis》（见结构、量价与形态相关章节）；《The Crypto Trader》（见执行计划与案例复盘相关章节）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-052：三框架协同决策

- **描述**：给定一个假设场景，能用宏观周期+链上信号+技术结构三套框架共同判断是否入场，并说明三者不一致时如何处理
- **前置技能**：SK-040, SK-050
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/2023-10_btc_three_framework_decision_dossier.md`；`resources/question_banks/SK-052_three_framework_synthesis_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“2. MVRV Ratio”“3. SOPR”“4. NUPL”）；`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-053：案例：2020年3月崩盘

- **描述**：能描述崩盘的宏观背景（COVID流动性危机），分析当时链上指标状态，并说明那个时间点的正确决策逻辑
- **前置技能**：SK-052
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/2020-03-12_btc_liquidity_crash_dossier.md`；`resources/question_banks/SK-053_056_case_synthesis_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“2. MVRV Ratio”“3. SOPR”）；`resources/04_trading/execution_decision_framework_guide.md`（见“复盘时必须问的四个问题”）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-054：案例：2021年11月周期顶部

- **描述**：能识别顶部出现前链上指标和技术结构给出的离场信号，判断自己是否会在当时离场，并说明为什么大多数人没有
- **前置技能**：SK-052
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/2021-11-08_btc_cycle_top_dossier.md`；`resources/question_banks/SK-053_056_case_synthesis_bank.md`；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“2. MVRV Ratio”“4. NUPL”）；《The Art and Science of Technical Analysis》（见顶部结构与离场确认相关章节）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-055：案例：2022年LUNA崩盘

- **描述**：能解释LUNA的算法稳定币机制，分析风险是如何从UST脱锚传导到整个市场的，以及哪些早期信号可以提前识别
- **前置技能**：SK-027, SK-052
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/2022-05_ust_luna_depeg_dossier.md`；`resources/question_banks/SK-053_056_case_synthesis_bank.md`；`resources/02_risk/stablecoin_liquidity_risk_guide.md`（见脱锚、赎回与信心断裂传导部分）；`resources/02_risk/ethereum_defi_risk_structure_guide.md`（见机制风险与协议暴露面部分）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-056：案例：2025年10月加密市场闪崩

- **描述**：能解释高杠杆环境（OI历史峰值）如何在宏观冲击触发时形成清算螺旋，分析链上数据（>90%持仓盈利、去杠杆特征）是否提供了提前预警，以及资金费率极值作为预警信号的作用
- **前置技能**：SK-026, SK-044, SK-052
- **掌握标准**：10题答对8题
- **主要参考资源**：`resources/cases/2025-10_crypto_flash_crash_dossier.md`；`resources/question_banks/SK-053_056_case_synthesis_bank.md`；`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“SK-056：闪崩案例”）；`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“2. MVRV Ratio”“4. NUPL”）；`resources/04_trading/exchange_microstructure_guide.md`（见“SK-056：2025年10月加密市场闪崩”）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

### SK-057：毕业综合：个人交易策略文档

- **描述**：能产出一份包含入场规则、出场规则、仓位管理原则、风险上限、周期判断框架的完整个人交易策略文档
- **前置技能**：SK-030, SK-053, SK-054, SK-055, SK-056
- **掌握标准**：文档完整覆盖五个核心模块，并按毕业策略文档评分表通过盛言评审
- **主要参考资源**：`resources/04_trading/SK-057_personal_strategy_template.md`；`resources/04_trading/execution_decision_framework_guide.md`（见“SK-057：毕业策略文档评分表”“SK-057：可填写模板”）；Binance Academy: What Is a Trading Journal and How to Use One（local-only source material；见日志字段与复盘样例部分）；《The Crypto Trader》（见完整策略样例与交易复盘相关章节）
- **状态**：🔒 未解锁
- **概念课完成**：—
- **首次掌握日期**：—
- **最近达标日期**：—
- **延迟验证到期**：—
- **延迟验证通过日期**：—
- **最后练习**：—
- **历史准确率**：[]
- **复习到期**：—
- **复习轮次**：0

---

## 掌握记录（按时间）

> 由 `teacher/homework_log.md` 的首次“掌握”事件自动生成。
> 记录首次达标时的通过方式、累计练习次数、主要失败类型，以及是否经过延迟验证，不受后续回退或重学影响。

| 技能点 | 首次掌握日期 | 通过方式 | 最终准确率 | 首次达标耗费次数 | 主要失败类型 | 延迟验证 |
|-------|---------|---------|-----------|----------------|-------------|---------|
| SK-001 | 2026-03-09 | 首练通过 | 10/10 | 1 | 无 | 未记录 |
| SK-002 | 2026-04-08 | 概念重修后通过 | 9/10 | 6 | 概念混淆×5；应用偏差×4；边界遗漏×4 | 未记录 |
| SK-003 | 2026-04-09 | 概念重修后通过 | 8/10 | 3 | 应用偏差×2；概念混淆；推导断链 | 未记录 |

---

## 今日延迟验证

> 由最近一次练习达标自动生成，默认安排在 24-72 小时内回测独立提取能力。
> 延迟验证未通过前，不进入稳定掌握，也不解锁依赖它的新技能点。

*（空）*

---

## 今日复习队列

> 由 `skill_graph.md` 的技能明细和系统日期自动生成。
> 会话开始时优先处理最该先清的技能点。
> 排序依据：上次复习是否勉强维持 / 未通过、逾期天数、最近错误模式数量。

- SK-001：货币的三个职能（第1次复习到期 2026-04-14，已逾期 18 天；优先原因：最近错误模式 1 类；已逾期 18 天）
- SK-002：货币的六个属性（第1次复习到期 2026-04-15，已逾期 17 天；优先原因：最近错误模式 1 类；已逾期 17 天）
- SK-003：健全货币 vs 不健全货币的判定标准（第1次复习到期 2026-04-16，已逾期 16 天；优先原因：最近错误模式 2 类；已逾期 16 天）

---

## 间隔复习时间表

> 以当前“最近达标日期”为基准自动推算。通过复习后，系统会滚动刷新“复习到期”。

| 技能点 | 第1次复习到期 | 第2次到期 | 第3次到期 | 第4次到期 |
|-------|------------|---------|---------|---------|
| SK-001 | 2026-04-14 | 2026-05-05 | 2026-07-04 | 2026-10-02 |
| SK-002 | 2026-04-15 | 2026-05-06 | 2026-07-05 | 2026-10-03 |
| SK-003 | 2026-04-16 | 2026-05-07 | 2026-07-06 | 2026-10-04 |

---

## 状态图例

> 若状态显示 `✅ 待延迟验证`，表示已通过当次练习，但尚未完成 24-72 小时后的短测。

| 图标 | 状态 | 含义 |
|------|------|------|
| 🔒 | 未解锁 | 前置技能点未掌握 |
| ⬜ | 未学 | 可以开始，尚未进行概念课 |
| 🔵 | 概念已完成 | 概念课已完成，等待练习课 |
| 🟡 | 学习中 | 练习课进行中，未达掌握标准 |
| ✅ | 已掌握 | 达到掌握标准 |
| 🔄 | 复习到期 | 间隔复习时间到 |
| 💚 | 长期掌握 | 完成第3次及以上复习 |
