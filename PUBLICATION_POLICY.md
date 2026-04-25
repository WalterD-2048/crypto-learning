# Publication Policy

This repository is intended to publish the learning-system code, teacher state, generated teaching views, self-authored case dossiers, guides, templates, and question banks.

It should not publish raw third-party books, articles, reports, or large imported source texts by default.

---

## Track By Default

- `tools/` and `tests/`
- `teacher/` system files and generated state files
- `resources/cases/` self-authored case dossiers
- `resources/question_banks/` self-authored question banks and rubrics
- Self-authored resource guides, indexes, and templates
- `AGENTS.md`, `CLAUDE.md`, `.gitignore`, and publication docs

---

## Keep Local Only

Raw third-party source material should remain local-only unless explicit rights and redistribution terms are confirmed.

Examples:

- Full or near-full book imports
- Article copies from third-party sites
- Research report copies
- Large markdown conversions from copyrighted books or reports

These files are ignored in `.gitignore`. The teaching system may still mention the corresponding title as a recommended reference, but public materials should not depend on the local raw copy being present.

---

## Reference Style

Use these forms in public docs:

- Good: `《Broken Money》（local-only source material；见法币稀释与购买力传导章节）`
- Good: `Binance Academy: A Beginner's Guide to Risk Management（local-only source material）`
- Avoid: direct public links to local raw imports that are ignored by Git.

Self-authored guides, dossiers, and question banks can be referenced by repository path.

---

## Before Publishing

Run:

```bash
python3 tools/learning_state.py sync
python3 tools/learning_state.py check
python3 -m unittest discover -s tests -v
git status --short --ignored
```

Confirm that ignored third-party source files appear under ignored output, and that public teaching artifacts remain tracked.
