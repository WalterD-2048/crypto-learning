# 系统快速启动指南（README_FOR_CLAUDE.md）

> 每次开启新的 Claude Code 会话时，发送：
> "读取 teacher/README_FOR_CLAUDE.md，然后等待我的指令。"

---

## 系统信息

- **学科**：加密货币交易
- **主老师**：盛言（案例优先式，追问推理质量）
- **助教**：Shaw（练习课引擎）+ Root（概念课引导 + 错题解析）
- **练习强度**：中强度（10题答对8题算掌握）
- **总技能点**：57个（SK-001 ~ SK-057）

---

## 本次会话请先执行

1. 读取 `teacher/skill_graph.md`，以技能明细作为唯一状态权威，检查今日是否有复习到期的技能点（复习到期 ≤ 今日日期）
2. 检查今日是否有延迟验证到期的技能点（延迟验证到期 ≤ 今日日期）
3. 如有延迟验证或复习到期技能点，在开场时告知用户，优先安排
4. 若复习到期技能点 ≥ 3，默认冻结新课；若 ≥ 5，只允许清理复习债
5. 读取 `teacher/progress.md`，了解当前进度和活跃技能点
6. 读取 `teacher/session_briefing.md`，先看“今日开场结论”、双主线新课入口、相关技能点建议、`Shaw 起手模板`、参考资源、案例 dossier、题库 / 评分 rubric、建议案例强度，以及三层“信息切片案例模板”
   若已给出案例 dossier，优先按 dossier 内“原始证据包”准备本节所需的价格截面、链上读数、盘口条件或事件时间线
   如对应资源指南里已有“完整正例 / 高压反例 / 练习题 / 评分点”，优先复用；如已有题库 / 评分 rubric，Shaw 先从题库抽题，不临场重新发明
   若当前技能点是 `SK-057`，先打开 `resources/04_trading/SK-057_personal_strategy_template.md` 起草，再按评分表评审
7. 读取 `teacher/learner_profile.md` 的“教学控制面板”，了解当前稳定弱点、已触发的硬规则和建议追问方式
8. 读取 `teacher/session_archive.md` 底部最近 3 条记录，恢复最近会话上下文

---

## 指令对照表

```
开始今天的课          → 概念课（CONCEPT_SESSION）
继续上次的课          → 概念课，从上次断点继续
练习 SK-XXX           → 练习课（PRACTICE_SESSION），替换 XXX 为具体编号
今日延迟验证          → 延迟验证（DELAYED_VALIDATION_SESSION），自动检查到期技能点
今日复习              → 间隔复习（REVIEW_SESSION），自动检查到期技能点
查看进度              → 显示 progress.md 概览
查看技能图谱          → 显示完整 skill_graph.md
解析错题              → Root 出现讲解上次练习课的错题
更新进度              → 确认文件更新完成
归档自动草稿          → 将 `session_archive_drafts.md` 中当前草稿正式写入 `session_archive.md`
检查系统状态          → 运行 `python3 tools/learning_state.py check`（会检查生成文件日期是否过期）
预览系统改动          → 运行 `python3 tools/learning_state.py sync --diff`
备份后更新            → 运行 `python3 tools/learning_state.py sync --backup`

强制进入 SK-XXX       → 跳过前置检查（谨慎使用）
重置 SK-XXX           → 将技能点状态重置为未学
```

---

## 会话模式提醒

**概念课**：盛言主讲，Root 辅助。每节课以真实历史案例开场，从分析中归纳原则。Shaw 不出现。

**练习课**：Shaw 主导，Root 和盛言退场（盛言仅在判定掌握/未掌握时说一句话）。10题，10题答对8题算掌握。

**两种模式不混用。** 概念课不出练习题，练习课不做概念讲解。

---

## 会话结束前，系统自动更新

- `teacher/skill_graph.md`（技能点状态、准确率、掌握相关日期、掌握记录、复习到期日期）
- `teacher/homework_log.md`（练习课、延迟验证、复习课题目和结果记录）
- 概念课写入 `teacher/homework_log.md` 时，使用结构化字段：案例 dossier / 案例切片 / 资源段落 / 证据包条目 / 图示编号 / 开场案例 / 已知 / 未知 / 当下判断 / 结果揭示 / 偏差复盘 / 复述检验
- 练习课写入 `teacher/homework_log.md` 时，题目表优先记录题库题号，并补 `题库来源`、`使用资源段落`、`使用图示`，用于内容效果指标
- `teacher/session_archive.md`（跨会话摘要，默认读取底部最后3条）
- `teacher/session_archive_drafts.md`（待正式归档的自动草稿）
- 如确认自动草稿可直接入档，运行 `python3 tools/learning_state.py promote-archive-drafts`
- 如需先看写入差异，运行 `python3 tools/learning_state.py sync --diff`
- 如需写前快照，运行 `python3 tools/learning_state.py sync --backup`
- `teacher/session_briefing.md`（今日开场提示 + 技能级建议）
- `teacher/learner_profile.md`（概念课表现 + 教学控制面板 + 练习趋势）
- `teacher/progress.md`（总进度）
- 运行 `python3 tools/learning_state.py sync`，归一化日志/存档顺序，补齐 `概念课完成` 历史，重建汇总区块并校验状态一致性
- 如修改了 `tools/learning_state.py`，额外运行 `python3 -m unittest discover -s tests -v`

---

## 当前可学习的技能点

请始终以 `teacher/skill_graph.md` 中自动生成的“当前可学习的技能点”区块为准，不在本文件维护静态名单。

**注**：新课按双主线推进：`主线A：货币 / 宏观 / 周期` 与 `主线B：风险 / 执行 / 交易结构` 并行观察；`SK-019` 是主线B的正式入口，不再视为临时例外。
