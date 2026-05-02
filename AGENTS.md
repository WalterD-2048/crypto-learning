# Agent 操作规则

这是一个 Markdown 驱动的加密货币学习系统。保持轻量，不要迁移到数据库、前端、复杂 agent 矩阵或大型 JSON 引擎。

## 启动时先读

1. `teacher/README_FOR_CLAUDE.md`
2. `teacher/skill_graph.md`
3. `teacher/progress.md`
4. `teacher/session_briefing.md`
5. `teacher/learner_profile.md`
6. `teacher/session_archive.md` 底部最近 3 条

## 状态权威与生成视图

- 状态权威：`teacher/skill_graph.md` 的技能明细。
- 练习证据：`teacher/homework_log.md`。
- 跨会话摘要：`teacher/session_archive.md` 和 `teacher/session_archive_drafts.md`。
- 自动生成视图：`teacher/progress.md`、`teacher/session_briefing.md`、`teacher/learner_profile.md` 的自动区块、`teacher/skill_graph.md` 的概览 / 当前可学 / 掌握记录 / 复习队列 / 复习时间表。

## 修改规则

- 不删除历史学习记录。
- 修改 `tools/learning_state.py` 后必须运行：
  - `python3 tools/learning_state.py check`
  - `python3 -m unittest discover -s tests -v`
- 修改题库或案例后检查：
  - 是否有明确技能点、题型、评分要点、常见错因 / 补救方向。
  - 是否引用了 case dossier、资源段落、题库题号或 source anchor。
  - 是否避免把结果倒推成当时判断。
- 不公开提交第三方书籍、文章、报告 raw import；遵守 `.gitignore`、`PUBLICATION_POLICY.md`、`resources/source_materials_manifest.md`。
- 本系统只用于教育和研究，不提供金融建议，不以实盘盈利作为掌握标准。

## 会话结束前

运行：

```bash
python3 tools/learning_state.py sync --diff
python3 tools/learning_state.py check
python3 -m unittest discover -s tests -v
git status --short --ignored
```
