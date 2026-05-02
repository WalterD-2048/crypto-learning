# 加密货币学习系统轻量审计

> 日期：2026-05-02
> 范围：只审计当前 Markdown 驱动的 crypto-learning 系统；不迁移到 `learning-system-template` 的大型运行时。

---

## 当前最强的 5 个点

1. `teacher/skill_graph.md` 已经能作为状态权威使用：每个技能都有状态、前置技能、掌握标准、练习历史、复习日期和生成调度区块。
2. 系统不是单纯笔记，而是已有闭环：概念课、练习日志、会话归档、进度视图、学习者画像、复习队列和下一课 briefing 都通过 `tools/learning_state.py` 串联。
3. 教师角色清楚：盛言、Root、Shaw 分别承担概念讲解、假设追问、错因解释、练习和复习。
4. 案例优先的教学结构已经存在：`resources/cases/`、信息切片模板和 briefing 指引会区分当时已知、当时未知、结果揭示和偏差复盘。
5. 发布边界明确：`.gitignore`、`PUBLICATION_POLICY.md`、`resources/source_materials_manifest.md` 把第三方 raw import 限定为本地材料。

---

## 最影响学习闭环的 5 个短板

1. SK-001 到 SK-003 是当前复习债技能，但此前没有专门的可复用题库入口，复习容易依赖历史记录或临场出题。
2. 内容追踪字段已经存在，但 session briefing 没有在使用现场明确提醒记录要求，导致资源和题库效果追踪容易为空。
3. 全局错因能被统计，但部分关键题库没有写明本技能的常见错因和补救方向。
4. 调研能力属于学习目标，但此前没有接入教学流程的轻量 research dossier 模板。
5. 生成状态校验较完整，但没有检查配置中的 case dossier、题库和模板引用是否真的指向仓库内文件。

---

## 现在修 vs 以后再修

现在修：

- 为 SK-001 到 SK-003 增加小型题库，支撑当前复习债。
- 增加简单内容标准，并给关键技能补常见错因和补救方向。
- 让 session briefing 在下一课现场提醒记录 case dossier、资源段落、证据/图示、题库题号和错因标签。
- 增加轻量 research dossier 模板和使用规则。
- 增加仓库内资源引用的存在性校验。

暂时不修：

- 不迁移到 JSON 状态、事件日志、数据库、前端 dashboard 或大型 adaptive runtime。
- 不增加复杂 agent 评审矩阵。
- 不重写 57 个技能或全部题库。
- 不改变 `teacher/skill_graph.md` 作为状态权威的定位。
- 不把实盘盈利或交易绩效作为掌握标准。

---

## 当前闭环

目标闭环是：

```text
concept lesson -> practice -> error cause -> review/remediation -> generated progress -> next lesson briefing
```

当前实现：

- 概念课：`teacher/session_briefing.md` 给出案例切片、已知/未知信息、第一问、结果揭示方式和偏差复盘重点。
- 练习：Shaw 优先使用技能题库，并把作答结果写入 `teacher/homework_log.md`。
- 错因：作业记录保留弱题型和错误模式；`tools/learning_state.py` 把它们映射为弱点簇和教学动作。
- 复习/补救：`teacher/skill_graph.md` 计算复习日期；`session_briefing.md` 按复习债、错误模式和延迟验证安排下一节课。
- 进度更新：`tools/learning_state.py sync` 生成 `skill_graph.md`、`progress.md`、`learner_profile.md`、`session_briefing.md` 和归档草稿。
- 下一课：下一次会话先读生成的 briefing 和 learner profile 控制面板。

---

## 闭环中断点

- 复习债冻结规则已经能阻止继续开新课，但 SK-001 到 SK-003 需要稳定题库来支持可重复复习。
- 内容效果追踪字段已经存在，但真实 session log 若缺少 trace 字段，`资源使用后续跟踪` 和 `题库题号效果` 会继续为空。
- 补救闭环在全局弱点层面较强，但若关键技能文件缺少本地错因/补救说明，练习后的修复动作仍不够具体。
- 调研任务可以口头布置，但没有 dossier 模板时，学习者容易跳过 source、uncertainty 和 counterexample。
