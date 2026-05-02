# 内容质量标准

这是当前 crypto-learning 系统的 Markdown 内容标准，不是 schema，也不是引擎迁移。

---

## 每个技能点的最低要求

每个技能点至少需要：

1. `teacher/skill_graph.md` 中有清楚学习目标。
2. 有可观察的掌握标准，不能只靠自信程度判断。
3. 至少一个 source/case anchor：
   - 仓库内 guide、case dossier、question bank 或 template；或
   - 只用标题/来源名标记的 local-only source，不引用被忽略的 raw-import 路径。
4. 有练习入口：
   - 技能专属题库、共享区间题库，或明确记录的复习题组。
5. 有能把错题归类到错因和补救方向的 rubric。

---

## 题库覆盖要求

可用题库至少覆盖：

- 核心理解：定义、公式或第一性原理解释。
- 概念辨析：说明这个概念为什么不是相邻概念。
- 场景应用：把概念用于真实加密货币/交易场景。
- 边界或反例：说明规则何时失效、变弱，或需要另一个框架。

计算型技能必须有计算题，但计算题不够；至少再补一个场景题或边界题。

---

## Rubric 要求

每个 rubric 应该能把错误标记到以下一类或多类：

- `概念混淆`
- `应用偏差`
- `边界遗漏`
- `推导断链`
- `结果倒推`
- `计算错误`
- `基础记忆缺失`
- `批判不足`

rubric 还要能指向下一步补救动作，例如：

- 概念辨析短练
- 场景变体练习
- 边界/反例练习
- 分步推导练习
- 计算短练
- research dossier 修订

---

## Case / Source Anchor 标准

案例课或 source-guided 概念课应记录：

- case dossier 路径或 source 标题
- 使用的资源段落
- evidence packet 条目
- 决策当时的已知信息
- 决策当时的未知信息
- 学习者第一判断
- 结果揭示
- 偏差复盘
- 后续练习或复习结果

---

## 调研任务标准

调研任务必须使用 `resources/research_dossier_template.md` 或等价结构。

学习者必须输出：

- research question
- core claim
- evidence table
- source anchor
- uncertainty
- counterexample 或 disconfirming evidence
- conclusion boundary
- 它如何影响交易判断，但不能变成直接交易建议

调研输出是证据训练，不是信号服务，也不是金融建议。

---

## 当前关键技能检查结果

| 技能 | 练习入口 | Anchor | 当前缺口 / 修复 |
|------|----------------|--------|-------------------|
| SK-001 | `resources/question_banks/SK-001_003_money_foundations_bank.md` | POW cigarette, Rai stones, Nixon shock | Added repeatable review entry for due review debt. |
| SK-002 | `resources/question_banks/SK-001_003_money_foundations_bank.md` | POW cigarette, 1933 gold, Rai stones | Added boundary/remediation notes for durability/fungibility/scarcity misses. |
| SK-003 | `resources/question_banks/SK-001_003_money_foundations_bank.md` | Nixon shock, Rai stones | Added framework-discipline and sound-money remediation notes. |
| SK-004 | `resources/question_banks/SK-004_inflation_mechanism_bank.md` | 2020-2022 monetary expansion dossier | Has full entry; added wrong-cause/remediation focus. |
| SK-019 | `resources/question_banks/SK-019_probability_vs_result_bank.md` | decision-quality dossier | Has full entry; added result-bias remediation focus. |
| SK-021 | `resources/question_banks/SK-021_expectancy_bank.md` | execution decision guide | Has calculation entry; added formula/sample-size remediation focus. |
| SK-023 | `resources/question_banks/SK-022_023_position_risk_bank.md` | execution decision guide | Has shared entry; added risk-amount vs position-size remediation focus. |
| SK-027 | `resources/question_banks/SK-027_custody_risk_bank.md` | FTX dossier | Has full entry; added custody/liquidity remediation focus. |
| SK-034 | `resources/question_banks/SK-031_042_onchain_metrics_bank.md` | Glassnode guide | Has shared entry; added single-indicator and MVRV-boundary remediation focus. |
| SK-044 | `resources/question_banks/SK-044_051_execution_toolkit_bank.md` | derivatives and funding guide | Has shared entry; added funding-rate crowding remediation focus. |
| SK-052 | `resources/question_banks/SK-052_three_framework_synthesis_bank.md` | 2023-10 three-framework dossier | Has full entry; added synthesis/remediation focus. |
| SK-057 | `resources/04_trading/SK-057_personal_strategy_template.md` | execution decision guide | Has strategy template; added common failure/remediation notes. |
