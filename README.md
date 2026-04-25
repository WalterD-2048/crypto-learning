# Crypto Learning System

这是一个加密货币学习系统，用于组织宏观、风险、链上、交易执行四条学习能力线，并通过技能图谱、案例 dossier、题库和复习队列驱动学习。

## 结构

- `teacher/`：教师角色、系统规则、学习状态、技能图谱和会话简报。
- `resources/`：自有教学指南、案例 dossier、题库、索引和资源说明。
- `tools/learning_state.py`：学习状态同步、校验、差异查看和备份工具。
- `tests/`：学习状态工具的回归测试。

## 常用命令

```bash
python3 tools/learning_state.py sync
python3 tools/learning_state.py check
python3 -m unittest discover -s tests -v
```

## 发布边界

本仓库默认只发布自有教学材料、生成状态、案例、题库和工具代码。第三方书籍、文章、报告的本地转写文件属于 local-only source material，默认由 `.gitignore` 排除。

发布前请参考：

- `PUBLICATION_POLICY.md`
- `resources/source_materials_manifest.md`

## Disclaimer

This project is for education and research only. It is not financial advice.
