# SK-001 ~ SK-057 内容审计

> 日期：2026-05-02
> 范围：只审计和补强学习内容，不做工程重构。状态字段仍以 `teacher/skill_graph.md` 为权威。

---

## 审计结论

1. SK-001 ~ SK-004 已有案例和题库；SK-001 ~ SK-003 当前复习债已有共享题库入口。
2. 原主要缺口是 SK-005 ~ SK-018 没有稳定题库入口；已补 `resources/question_banks/SK-005_018_macro_bitcoin_cycle_bank.md`。
3. SK-019 ~ SK-030 的风险/执行基础题库完整，但部分题库缺少显式错因/补救；已补 SK-020、SK-024/025、SK-026、SK-028、SK-029/030。
4. SK-031 ~ SK-042 原共享题库覆盖题型，但错因/补救主要集中在 SK-034；已扩展为覆盖每个链上技能。
5. SK-043 ~ SK-056 已有题库和案例，但共享题库需要逐技能补错因；已补 SK-043、SK-044~051、SK-053~056。
6. SK-057 已有可填写策略模板和评审标准；保留当前模板，只用内容标准校验。

---

## Prompt-to-Artifact Checklist

| 要求 | 证据 |
|------|------|
| 逐个检查 SK-001~SK-057 | 本文下方 57 行审计表逐项映射能力、anchor、练习、错因/补救、边界。 |
| 每个 SK 有清晰学习目标 | `teacher/skill_graph.md` 的 `描述` 字段 + 本文 `能力/为什么` 列。 |
| 每个 SK 有 source/case anchor | `teacher/skill_graph.md` 的 `主要参考资源` + 本文 `开场 anchor` 列。 |
| 每个 SK 有练习入口 | `resources/question_banks/` 现有/新增题库，SK-057 使用策略模板。 |
| 每个 SK 有评分要点 | 各题库 `评分 rubric`、题目 `评分要点`、SK-057 模板评审清单。 |
| 每个 SK 有常见误区和补救 | 各题库 `错因与补救方向`，共享题库已扩到对应 SK。 |
| 每个 SK 有边界/反例 | 各题库包含边界、反例构造或不通过原因；本文列出最低边界。 |
| 不重构工程 / 不迁移 JSON / 不建 Web App | 本轮只新增/修改 Markdown 内容和小范围题库索引。 |
| 不发布 third-party raw source | 新增/修改内容只引用标题或仓库路径，遵守 `PUBLICATION_POLICY.md`。 |
| 不写实盘建议 | 所有题库和模板均要求框架判断，不给买卖建议。 |

---

## 逐项审计表

| SK | 能力 / 为什么 | 开场 anchor | 练习入口 | 常见错因 -> 补救 | 边界 / 反例 |
|----|---------------|-------------|----------|------------------|-------------|
| SK-001 | 区分三种货币职能；为后续货币判断打底 | POW 香烟货币、Rai 石、Nixon shock | `SK-001_003_money_foundations_bank.md` | 交换媒介/记账单位混淆 -> 辨析短练 | 能储值不等于好交换媒介 |
| SK-002 | 用六属性评价货币；建立属性框架 | POW 香烟、黄金禁令、Rai 石 | `SK-001_003_money_foundations_bank.md` | 耐久/可替换混淆 -> 属性对照题 | 有价值不等于适合当货币 |
| SK-003 | 判定健全/不健全货币；连接制度约束 | Nixon shock、Rai 石 | `SK-001_003_money_foundations_bank.md` | 把共识当第七属性 -> 两步归因 | 短期可用但长期不健全 |
| SK-004 | 解释货币通胀到价格通胀的传导 | 2020-2022 货币扩张 dossier | `SK-004_inflation_mechanism_bank.md` | 传导断链 -> 三层传导图 | 供给冲击也能涨价 |
| SK-005 | 拆法币结构缺陷；理解购买力风险 | 1971 Nixon shock、《Broken Money》 | `SK-005_018_macro_bitcoin_cycle_bank.md` | 末日叙事 -> 补制度韧性 | 法币短期仍可高效运行 |
| SK-006 | 定义双花与传统中介解法 | Bitcoin whitepaper Introduction | `SK-005_018_macro_bitcoin_cycle_bank.md` | 复制文件=双花 -> 余额重复支付图 | 中介能解决但引入信任成本 |
| SK-007 | 解释区块链防双花机制 | 白皮书时间戳/PoW | `SK-005_018_macro_bitcoin_cycle_bank.md` | 只说“大家都有账本” -> 补排序和成本 | 零确认仍有双花风险 |
| SK-008 | 理解矿工、PoW 和激励 | 白皮书网络与激励 | `SK-005_018_macro_bitcoin_cycle_bank.md` | 只说矿工记账 -> 补收益/成本比较 | 算力集中、费用不足 |
| SK-009 | 用 UTXO 追踪所有权 | 白皮书 UTXO 模型 | `SK-005_018_macro_bitcoin_cycle_bank.md` | 地址余额=账户余额 -> 画输入输出 | CEX 内部账不是链上 UTXO |
| SK-010 | 解释 2100 万上限和货币学意义 | 白皮书 + hard cap 讨论 | `SK-005_018_macro_bitcoin_cycle_bank.md` | 创始人承诺论 -> 节点共识规则 | 理论可改但社会成本极高 |
| SK-011 | 区分私钥/公钥/地址安全逻辑 | 私钥签名链路 | `SK-005_018_macro_bitcoin_cycle_bank.md` | 地址当密码 -> 派生链图 | 多签/托管改变控制权 |
| SK-012 | 解释减半触发和新增供给变化 | Lyn Alden halving | `SK-005_018_macro_bitcoin_cycle_bank.md` | 供应减少 -> 新增供应下降短练 | 费用市场和需求不足 |
| SK-013 | 推导减半到价格的条件链 | Lyn Alden halving cycle | `SK-005_018_macro_bitcoin_cycle_bank.md` | 减半必涨 -> 加需求/流动性条件 | 提前定价或需求下降 |
| SK-014 | 计算并批判 S2F | Lyn Alden S2F | `SK-005_018_macro_bitcoin_cycle_bank.md` | 回测=预测 -> 补模型假设 | 稀缺但无需求不会升值 |
| SK-015 | 识别历史周期结构 | 2020/2021 周期案例 | `SK-005_018_macro_bitcoin_cycle_bank.md` | 背阶段不看证据 -> 阶段证据表 | 未来周期可能变形 |
| SK-016 | 解释网络效应和市占率 | Lyn Alden network effect | `SK-005_018_macro_bitcoin_cycle_bank.md` | 性能更快=取代 BTC -> 货币网络维度 | 监管/叙事迁移会削弱网络 |
| SK-017 | 分析宏观变量对 BTC 的影响 | Lyn Alden macro context | `SK-005_018_macro_bitcoin_cycle_bank.md` | 单因果解释 -> 多变量推导 | 监管/链上冲击可压过宏观 |
| SK-018 | 拆 TAM/黄金对标估值 | ARK/机构估值框架 | `SK-005_018_macro_bitcoin_cycle_bank.md` | 估值目标=预测 -> 假设表 | 采用率或倍数不达预期 |
| SK-019 | 区分决策质量和结果质量 | decision-quality dossier | `SK-019_probability_vs_result_bank.md` | 结果倒推 -> 锁定当时信息集 | 好决策可亏损 |
| SK-020 | 识别认知偏差如何扭曲交易 | execution guide + 交易心理 | `SK-020_cognitive_bias_bank.md` | 只贴标签 -> 写信息扭曲环节 | 亏损不一定来自偏差 |
| SK-021 | 计算期望值 | execution guide | `SK-021_expectancy_bank.md` | 高胜率=正期望 -> 对比赔率题 | 正期望仍会回撤 |
| SK-022 | 区分仓位大小和风险金额 | execution guide | `SK-022_023_position_risk_bank.md` | 仓位=风险 -> 同仓位不同止损题 | 杠杆/滑点改变真实风险 |
| SK-023 | 用 1% 法则反推仓位 | execution guide | `SK-022_023_position_risk_bank.md` | 先想买多少 -> 失效点先行 | 强平边界会改变可用仓位 |
| SK-024 | 设置事前止损 | exit rules bank | `SK-024_025_exit_rules_bank.md` | 入场后改止损 -> 先写失效条件 | 止损太近会被噪音打掉 |
| SK-025 | 设置止盈和 R:R | exit rules bank | `SK-024_025_exit_rules_bank.md` | 感觉止盈 -> 固定/分批/追踪规则 | 低胜率需保护赔率 |
| SK-026 | 理解爆仓和强平边界 | derivatives guide | `SK-026_liquidation_mechanism_bank.md` | 止损/爆仓混淆 -> 主动/被动退出辨析 | 方向对也可能先爆仓 |
| SK-027 | 判断 CEX 托管风险 | FTX dossier | `SK-027_custody_risk_bank.md` | 余额=资产安全 -> 兑付链条 | 撮合正常不代表可提现 |
| SK-028 | 拆 DeFi 攻击面 | Mango dossier + DeFi guide | `SK-028_defi_protocol_risk_bank.md` | 全归代码 bug -> 攻击面分层 | 审计/TVL 高不等于安全 |
| SK-029 | 建立 OpSec 基础 | DeFi risk guide | `SK-029_030_opsec_journal_bank.md` | 自托管=安全 -> 攻击路径题 | 授权/前端/社工仍可致损 |
| SK-030 | 建交易日志并复盘 | execution guide | `SK-029_030_opsec_journal_bank.md` | 盈亏复盘 -> 字段化日志 | 盈利但违规则仍是坏执行 |
| SK-031 | 理解链上数据本质 | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 链上=全市场 -> 能测/不能测表 | CEX/OTC 不完整可见 |
| SK-032 | 解释 Realized Cap | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 当成 Market Cap 平滑版 -> UTXO 成本基础 | 丢失币/沉睡币影响解释 |
| SK-033 | 解读 Market vs Realized 差值 | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 差值=现金 -> 未实现盈亏压力 | 不能直接兑现 |
| SK-034 | 解释 MVRV | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 单指标交易 -> 联合确认 | regime 与宏观会改变含义 |
| SK-035 | 解读 MVRV-Z | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 极值=必然顶底 -> 统计边界 | 样本少、周期变化 |
| SK-036 | 解读 NUPL | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 背区间不懂盈亏分布 -> 公式重建 | 欣快区可继续上涨 |
| SK-037 | 定义 SOPR | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 混同日内涨跌 -> realized value/cost basis | raw SOPR 有噪音 |
| SK-038 | 分 regime 读 SOPR | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 机械读 1.0 -> 先判牛熊 | 同数值在不同 regime 含义相反 |
| SK-039 | 区分 LTH/STH | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 忘 155 天 -> 定义短练 | LTH 卖出不总是利空 |
| SK-040 | 三指标联合读法 | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 只挑一个指标 -> 三指标表 | 一致也不等于可直接交易 |
| SK-041 | 识别链上数据局限 | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 透明=无偏 -> 污染来源清单 | 洗盘/内部账/标签错误 |
| SK-042 | 用链上数据复盘周期 | Glassnode guide | `SK-031_042_onchain_metrics_bank.md` | 后见之明 -> 遮住后续路径 | 2020-2022 指标可能冲突 |
| SK-043 | 选择现货/永续/交割 | instrument dossier | `SK-043_instrument_choice_bank.md` | 工具只看收益放大 -> 风险结构比较 | 方向对但工具错 |
| SK-044 | 解读资金费率 | derivatives guide | `SK-044_051_execution_toolkit_bank.md` | 正费率=方向信号 -> 锚定/拥挤拆分 | 极端费率可延续 |
| SK-045 | 判断流动性与滑点 | microstructure guide | `SK-044_051_execution_toolkit_bank.md` | 滑点=手续费 -> 成本拆分 | 平静滑点不能外推极端行情 |
| SK-046 | 识别支撑阻力 | execution guide | `SK-044_051_execution_toolkit_bank.md` | 一条线=支撑 -> 证据清单 | 支撑破位后要改判断 |
| SK-047 | 分析成交量 | execution guide | `SK-044_051_execution_toolkit_bank.md` | 背四象限 -> 加位置/趋势 | 量减涨不总是看空 |
| SK-048 | 使用移动平均线 | execution guide | `SK-044_051_execution_toolkit_bank.md` | 金叉领先 -> 先说明滞后 | 震荡市假信号多 |
| SK-049 | 判断 K 线形态有效性 | execution guide | `SK-044_051_execution_toolkit_bank.md` | 单形态入场 -> 加量价/位置 | 形态需大周期确认 |
| SK-050 | 定义入场条件 | execution guide | `SK-044_051_execution_toolkit_bank.md` | 感觉入场 -> 外部可检验条件 | 条件未触发不能上车 |
| SK-051 | 定义出场条件 | execution guide | `SK-044_051_execution_toolkit_bank.md` | 只写目标价 -> 多种退出规则 | 趋势延续需追踪退出 |
| SK-052 | 三框架协同决策 | 2023-10 dossier | `SK-052_three_framework_synthesis_bank.md` | 三层混成结论 -> 三列表 | 三层不一致时降级动作 |
| SK-053 | 复盘 2020-03 崩盘 | 2020 crash dossier | `SK-053_056_case_synthesis_bank.md` | 事后抄底叙事 -> 当时信息集 | 流动性冲击不等于长期破产 |
| SK-054 | 复盘 2021 顶部 | 2021 top dossier | `SK-053_056_case_synthesis_bank.md` | 创新高=安全 -> 过热证据 | 顶部识别不是卖最高点 |
| SK-055 | 复盘 LUNA 崩盘 | UST/LUNA dossier | `SK-053_056_case_synthesis_bank.md` | 脱锚=普通波动 -> 机制链条 | 暂时回锚不等于结构安全 |
| SK-056 | 复盘 2025 闪崩 | flash crash dossier | `SK-053_056_case_synthesis_bank.md` | 只看跌幅 -> OI/费率/盘口/强平链 | 基本面未变也会闪崩 |
| SK-057 | 写个人策略文档 | SK-057 strategy template | `SK-057_personal_strategy_template.md` | 口号策略 -> 五段式补齐 | 盈利样例不能证明策略有效 |

---

## 剩余人工审阅建议

- 后续每完成一个新 SK 的概念课，应把真实错题回填到对应题库的错因表。
- 对 SK-005 ~ SK-018，可先用新增题库跑一轮，观察是否需要拆成更细的子题库。
- 对 SK-031 ~ SK-042 和 SK-044 ~ SK-051，共享题库已经覆盖全段，但真实训练时仍应按当前 SK 只抽相关题。
