from __future__ import annotations

import importlib.util
import sys
import textwrap
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "learning_state.py"
SPEC = importlib.util.spec_from_file_location("learning_state", MODULE_PATH)
learning_state = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = learning_state
SPEC.loader.exec_module(learning_state)


def sample_skill_graph() -> str:
    return textwrap.dedent(
        """\
        # 技能图谱（skill_graph.md）

        > 测试夹具

        ---

        ## 概览

        | 项目 | 数值 |
        |------|------|
        | 总技能点数 | 2 |
        | 已掌握 | 1 |
        | 学习中 | 0 |
        | 未解锁 | 0 |
        | 今日复习到期 | 0 |

        ---

        ## 当前可学习的技能点

        （前置技能已掌握，或无前置依赖）

        - SK-002：示例技能二

        ---

        ## 技能点目录

        ### SK-001：示例技能一

        - **描述**：描述一
        - **前置技能**：无
        - **掌握标准**：10题答对8题
        - **状态**：✅ 已掌握
        - **概念课完成**：2026-03-12
        - **首次掌握日期**：2026-03-12
        - **最近达标日期**：2026-03-12
        - **延迟验证到期**：—
        - **延迟验证通过日期**：2026-03-12
        - **最后练习**：2026-03-12
        - **历史准确率**：[8/10]
        - **复习到期**：2026-03-19
        - **复习轮次**：0

        ---

        ### SK-002：示例技能二

        - **描述**：描述二
        - **前置技能**：SK-001
        - **掌握标准**：10题答对8题
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

        ## 掌握记录（按时间）

        > 测试夹具

        | 技能点 | 首次掌握日期 | 通过方式 | 最终准确率 | 首次达标耗费次数 | 主要失败类型 | 延迟验证 |
        |-------|---------|---------|-----------|----------------|-------------|---------|
        | SK-001 | 2026-03-12 | 首练通过 | 8/10 | 1 | 无 | 未记录 |

        ---

        ## 今日延迟验证

        *（空）*

        ---

        ## 今日复习队列

        *（空）*

        ---

        ## 间隔复习时间表

        | 技能点 | 第1次复习到期 | 第2次到期 | 第3次到期 | 第4次到期 |
        |-------|------------|---------|---------|---------|
        | SK-001 | 2026-03-19 | 2026-04-09 | 2026-06-08 | 2026-09-06 |

        ---

        ## 状态图例

        | 图标 | 状态 | 含义 |
        |------|------|------|
        | ✅ | 已掌握 | 达到掌握标准 |
        """
    )


def sample_learner_profile() -> str:
    return textwrap.dedent(
        """\
        # 学习者档案（learner_profile.md）

        > 测试夹具

        ---

        ## 基本信息

        - 占位

        ---

        ## 学习风格观察

        手工内容

        ---

        ## 概念课表现记录

        手工内容

        ---

        ## 教学控制面板

        *（待系统生成）*

        ---

        ## 练习课准确率趋势

        *（待系统生成）*

        ---

        ## 盛言的当前评价

        手工内容
        """
    )


class LearningStateTests(unittest.TestCase):
    maxDiff = None

    def test_sync_skill_graph_concept_fields_keeps_skill_headings_intact(self) -> None:
        text = sample_skill_graph()
        skills = learning_state.parse_skill_graph(text)
        concept_events = {
            "SK-001": [
                learning_state.ConceptEvent(date(2026, 3, 12), None, "skill_graph"),
                learning_state.ConceptEvent(date(2026, 4, 7), "重修", "homework_log"),
                learning_state.ConceptEvent(date(2026, 4, 8), "重修2", "session_archive"),
            ],
            "SK-002": [],
        }

        synced = learning_state.sync_skill_graph_concept_fields(
            text, skills, concept_events
        )

        self.assertIn("### SK-001：示例技能一", synced)
        self.assertIn("### SK-002：示例技能二", synced)
        self.assertIn(
            "- **概念课完成**：2026-03-12（重修 2026-04-07，重修2 2026-04-08）",
            synced,
        )
        self.assertNotIn("P26-", synced)

    def test_case_template_for_skill_uses_specialized_resource_entry_for_luna_case(self) -> None:
        template = learning_state.case_template_for_skill(
            learning_state.Skill(
                skill_id="SK-055",
                name="案例：2022年LUNA崩盘",
                description="desc",
                prereq_text="SK-027, SK-052",
                prereqs=("SK-027", "SK-052"),
                mastery_standard="10题答对8题",
                status="⬜ 未学",
                concept_completed="—",
                first_mastery_date=None,
                latest_mastery_date=None,
                delayed_validation_due=None,
                delayed_validation_passed_date=None,
                last_practice=None,
                history_accuracies=(),
                review_due=None,
                review_round=0,
            ),
            [],
        )

        self.assertEqual(template["theme"], "UST 脱锚前夜的稳定币信心断裂切片")
        self.assertIn("2022-05_ust_luna_depeg_dossier.md", template["source"])
        self.assertIn("stablecoin_liquidity_risk_guide.md", template["source"])
        self.assertIn("ethereum_defi_risk_structure_guide.md", template["source"])
        self.assertEqual(template["recommended_level"], "入门切片")
        self.assertIn("2022-05-07 至 2022-05-12 UST 脱锚过程", template["entry_cases"])
        self.assertIn("LUNA 承接压力如何转成死亡螺旋", template["standard_cases"])
        self.assertIn("价格短暂回稳却已无法恢复结构信任的阶段", template["stress_cases"])

    def test_case_skill_resources_prefer_dossier_for_march_2020_case(self) -> None:
        references = learning_state.resource_references_for_skill(
            learning_state.Skill(
                skill_id="SK-053",
                name="案例：2020年3月崩盘",
                description="desc",
                prereq_text="SK-052",
                prereqs=("SK-052",),
                mastery_standard="10题答对8题",
                status="⬜ 未学",
                concept_completed="—",
                first_mastery_date=None,
                latest_mastery_date=None,
                delayed_validation_due=None,
                delayed_validation_passed_date=None,
                last_practice=None,
                history_accuracies=(),
                review_due=None,
                review_round=0,
            )
        )

        self.assertEqual(
            references[0], "`resources/cases/2020-03-12_btc_liquidity_crash_dossier.md`"
        )
        self.assertIn("SK-053_056_case_synthesis_bank.md", references[1])
        self.assertIn("glassnode_onchain_metrics_guide.md", references[2])

    def test_curated_skill_references_include_case_dossier_and_question_bank(self) -> None:
        skill = learning_state.Skill(
            skill_id="SK-052",
            name="三框架协同判断",
            description="desc",
            prereq_text="SK-040, SK-050",
            prereqs=("SK-040", "SK-050"),
            mastery_standard="10题答对8题",
            status="⬜ 未学",
            concept_completed="—",
            first_mastery_date=None,
            latest_mastery_date=None,
            delayed_validation_due=None,
            delayed_validation_passed_date=None,
            last_practice=None,
            history_accuracies=(),
            review_due=None,
            review_round=0,
        )

        self.assertEqual(
            learning_state.case_dossier_reference_for_skill(skill),
            "`resources/cases/2023-10_btc_three_framework_decision_dossier.md`",
        )
        self.assertEqual(
            learning_state.question_bank_reference_for_skill(skill),
            "`resources/question_banks/SK-052_three_framework_synthesis_bank.md`",
        )

    def test_foundation_skills_reference_shared_review_question_bank(self) -> None:
        skill = learning_state.Skill(
            skill_id="SK-001",
            name="货币的三个职能",
            description="desc",
            prereq_text="无",
            prereqs=(),
            mastery_standard="10题答对8题",
            status="✅ 已掌握",
            concept_completed="2026-03-12",
            first_mastery_date=date(2026, 3, 12),
            latest_mastery_date=date(2026, 3, 12),
            delayed_validation_due=None,
            delayed_validation_passed_date=date(2026, 3, 12),
            last_practice=date(2026, 3, 12),
            history_accuracies=("8/10",),
            review_due=date(2026, 3, 19),
            review_round=0,
        )

        self.assertEqual(
            learning_state.question_bank_reference_for_skill(skill),
            "`resources/question_banks/SK-001_003_money_foundations_bank.md`",
        )
        self.assertIn(
            "`resources/question_banks/SK-001_003_money_foundations_bank.md`",
            learning_state.resource_references_for_skill(skill),
        )

    def test_execution_skill_references_point_to_section_level_materials(self) -> None:
        funding_skill = learning_state.Skill(
            skill_id="SK-044",
            name="资金费率",
            description="desc",
            prereq_text="SK-043",
            prereqs=("SK-043",),
            mastery_standard="10题答对8题",
            status="⬜ 未学",
            concept_completed="—",
            first_mastery_date=None,
            latest_mastery_date=None,
            delayed_validation_due=None,
            delayed_validation_passed_date=None,
            last_practice=None,
            history_accuracies=(),
            review_due=None,
            review_round=0,
        )
        refs = learning_state.resource_references_for_skill(funding_skill)
        refs_text = "；".join(refs)

        self.assertIn("SK-044_051_execution_toolkit_bank.md", refs[0])
        self.assertIn("SK-044：资金费率", refs_text)
        self.assertIn("Trigger / Execution", refs_text)
        self.assertIn("理解盘口的第一原则", refs_text)

    def test_risk_track_question_bank_references_are_skill_specific(self) -> None:
        skill = learning_state.Skill(
            skill_id="SK-026",
            name="爆仓机制",
            description="desc",
            prereq_text="SK-023",
            prereqs=("SK-023",),
            mastery_standard="10题答对8题",
            status="⬜ 未学",
            concept_completed="—",
            first_mastery_date=None,
            latest_mastery_date=None,
            delayed_validation_due=None,
            delayed_validation_passed_date=None,
            last_practice=None,
            history_accuracies=(),
            review_due=None,
            review_round=0,
        )

        self.assertEqual(
            learning_state.question_bank_reference_for_skill(skill),
            "`resources/question_banks/SK-026_liquidation_mechanism_bank.md`",
        )
        self.assertIn(
            "`resources/question_banks/SK-026_liquidation_mechanism_bank.md`",
            learning_state.resource_references_for_skill(skill)[0],
        )

    def test_onchain_and_execution_ranges_use_merged_question_banks(self) -> None:
        template = learning_state.parse_skill_graph(sample_skill_graph())[1]
        onchain_skill = learning_state.replace(
            template,
            skill_id="SK-034",
            name="MVRV 比率",
            prereq_text="SK-033",
            prereqs=("SK-033",),
        )
        execution_skill = learning_state.replace(
            template,
            skill_id="SK-048",
            name="移动平均线",
            prereq_text="SK-046",
            prereqs=("SK-046",),
        )

        self.assertEqual(
            learning_state.question_bank_reference_for_skill(onchain_skill),
            "`resources/question_banks/SK-031_042_onchain_metrics_bank.md`",
        )
        self.assertIn(
            "`resources/question_banks/SK-031_042_onchain_metrics_bank.md`",
            learning_state.resource_references_for_skill(onchain_skill)[0],
        )
        self.assertEqual(
            learning_state.question_bank_reference_for_skill(execution_skill),
            "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
        )
        self.assertIn(
            "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
            learning_state.resource_references_for_skill(execution_skill)[0],
        )

    def test_graduation_resources_include_fillable_template(self) -> None:
        skill = learning_state.Skill(
            skill_id="SK-057",
            name="毕业综合：个人交易策略文档",
            description="desc",
            prereq_text="SK-030, SK-053, SK-054, SK-055, SK-056",
            prereqs=("SK-030", "SK-053", "SK-054", "SK-055", "SK-056"),
            mastery_standard="文档通过评审",
            status="⬜ 未学",
            concept_completed="—",
            first_mastery_date=None,
            latest_mastery_date=None,
            delayed_validation_due=None,
            delayed_validation_passed_date=None,
            last_practice=None,
            history_accuracies=(),
            review_due=None,
            review_round=0,
        )
        refs = learning_state.resource_references_for_skill(skill)

        self.assertEqual(
            refs[0],
            "`resources/04_trading/SK-057_personal_strategy_template.md`",
        )
        self.assertIn("SK-057：毕业策略文档评分表", refs[1])

    def test_generated_resource_references_do_not_use_local_only_raw_paths(self) -> None:
        raw_path_fragments = [
            "ARKInvest_090320_Bitcoin_PART_1",
            "Broken-Money_",
            "Emerging_Tech_Bitcoin_Crypto",
            "The-Bitcoin-Standard_",
            "A Beginner's Guide to Risk Management.md",
            "Five Risk Management Strategies.md",
            "What Are Stop-Loss and Take-Profit Levels and How to Calculate Them.md",
            "What Is a Trading Journal and How to Use One.md",
            "Trading-in-the-Zone_",
            "Cryptoassets_",
            "The-Art-and-Science-of-Technical-Analysis_",
            "The-Crypto-Trader",
        ]
        rendered_refs = []
        for number in range(1, 58):
            skill = learning_state.Skill(
                skill_id=f"SK-{number:03d}",
                name=f"测试技能{number}",
                description="desc",
                prereq_text="无",
                prereqs=(),
                mastery_standard="10题答对8题",
                status="⬜ 未学",
                concept_completed="—",
                first_mastery_date=None,
                latest_mastery_date=None,
                delayed_validation_due=None,
                delayed_validation_passed_date=None,
                last_practice=None,
                history_accuracies=(),
                review_due=None,
                review_round=0,
            )
            rendered_refs.extend(learning_state.resource_references_for_skill(skill))
            rendered_refs.append(learning_state.case_template_for_skill(skill, [])["source"])

        rendered_text = "\n".join(rendered_refs)

        for fragment in raw_path_fragments:
            self.assertNotIn(fragment, rendered_text)
        self.assertIn("local-only source material", rendered_text)

    def test_validate_configured_resource_references_detects_missing_file(self) -> None:
        original_reference = learning_state.QUESTION_BANK_REFERENCES["SK-001"]
        try:
            learning_state.QUESTION_BANK_REFERENCES["SK-001"] = (
                "`resources/question_banks/DOES_NOT_EXIST.md`"
            )
            errors = learning_state.validate_configured_resource_references()
        finally:
            learning_state.QUESTION_BANK_REFERENCES["SK-001"] = original_reference

        self.assertTrue(
            any("resources/question_banks/DOES_NOT_EXIST.md" in error for error in errors)
        )

    def test_session_briefing_lists_case_dossier_for_case_skill(self) -> None:
        skills = [
            learning_state.Skill(
                skill_id="SK-052",
                name="三框架协同决策",
                description="desc",
                prereq_text="SK-040, SK-050",
                prereqs=("SK-040", "SK-050"),
                mastery_standard="10题答对8题",
                status="✅ 已掌握",
                concept_completed="2026-03-18",
                first_mastery_date=date(2026, 3, 18),
                latest_mastery_date=date(2026, 3, 18),
                delayed_validation_due=None,
                delayed_validation_passed_date=date(2026, 3, 20),
                last_practice=date(2026, 3, 20),
                history_accuracies=("8/10",),
                review_due=None,
                review_round=0,
            ),
            learning_state.Skill(
                skill_id="SK-053",
                name="案例：2020年3月崩盘",
                description="desc",
                prereq_text="SK-052",
                prereqs=("SK-052",),
                mastery_standard="10题答对8题",
                status="⬜ 未学",
                concept_completed="—",
                first_mastery_date=None,
                latest_mastery_date=None,
                delayed_validation_due=None,
                delayed_validation_passed_date=None,
                last_practice=None,
                history_accuracies=(),
                review_due=None,
                review_round=0,
            ),
        ]

        briefing = learning_state.render_session_briefing(
            skills,
            [],
            [],
            date(2026, 3, 20),
        )

        self.assertIn("#### SK-053：案例：2020年3月崩盘", briefing)
        self.assertIn(
            "- **案例 dossier**：`resources/cases/2020-03-12_btc_liquidity_crash_dossier.md`",
            briefing,
        )

    def test_session_briefing_lists_question_bank_for_curated_new_skills(self) -> None:
        template_skills = learning_state.parse_skill_graph(sample_skill_graph())
        skills = [
            learning_state.replace(
                template_skills[0],
                skill_id="SK-003",
                name="宏观前置",
                prereq_text="无",
                prereqs=(),
                review_due=None,
            ),
            learning_state.replace(
                template_skills[1],
                skill_id="SK-004",
                name="通货膨胀的机制",
                prereq_text="SK-003",
                prereqs=("SK-003",),
            ),
            learning_state.replace(
                template_skills[1],
                skill_id="SK-019",
                name="概率思维 vs 结果导向",
                prereq_text="无",
                prereqs=(),
            ),
        ]

        briefing = learning_state.render_session_briefing(
            skills,
            [],
            [],
            date(2026, 4, 24),
        )

        self.assertIn("#### SK-004：通货膨胀的机制", briefing)
        self.assertIn(
            "- **案例 dossier**：`resources/cases/2020-2022_monetary_expansion_inflation_dossier.md`",
            briefing,
        )
        self.assertIn(
            "- **题库 / 评分 rubric**：`resources/question_banks/SK-004_inflation_mechanism_bank.md`",
            briefing,
        )
        self.assertIn("#### SK-019：概率思维 vs 结果导向", briefing)
        self.assertIn(
            "- **案例 dossier**：`resources/cases/decision_quality_vs_result_quality_dossier.md`",
            briefing,
        )
        self.assertIn(
            "- **题库 / 评分 rubric**：`resources/question_banks/SK-019_probability_vs_result_bank.md`",
            briefing,
        )
        self.assertIn("## 本节记录要求", briefing)
        self.assertIn("`题库题号`", briefing)
        self.assertIn("resources/research_dossier_template.md", briefing)

    def test_normalize_homework_log_orders_retry_between_attempts(self) -> None:
        raw = textwrap.dedent(
            """\
            # 学习记录（homework_log.md）

            ## 练习记录

            ### 2026-04-09 练习课（第3次）：SK-003《测试技能》

            **本次准确率**：8/10（80%）
            **掌握判定**：✅ 掌握

            ---

            ### 2026-04-09 练习课（第1次）：SK-003《测试技能》

            **本次准确率**：6/10（60%）
            **掌握判定**：❌ 未掌握

            ---

            ### 2026-04-09 概念重修课：SK-003《测试技能》

            **盛言开场案例**：示例

            ---

            ### 2026-04-09 练习课（第2次）：SK-003《测试技能》

            **本次准确率**：7/10（70%）
            **掌握判定**：❌ 未掌握
            """
        )

        normalized = learning_state.normalize_homework_log(raw)
        headings = [
            match.group(1)
            for match in learning_state.re.finditer(r"^### (.+)$", normalized, learning_state.re.M)
        ]

        self.assertEqual(
            headings,
            [
                "2026-04-09 练习课（第1次）：SK-003《测试技能》",
                "2026-04-09 练习课（第2次）：SK-003《测试技能》",
                "2026-04-09 概念重修课：SK-003《测试技能》",
                "2026-04-09 练习课（第3次）：SK-003《测试技能》",
            ],
        )
        self.assertNotIn("---\n\n---", normalized)

    def test_collect_concept_events_combines_skill_graph_homework_and_archive(self) -> None:
        skill = learning_state.Skill(
            skill_id="SK-002",
            name="测试技能",
            description="描述",
            prereq_text="无",
            prereqs=(),
            mastery_standard="10题答对8题",
            status="✅ 已掌握",
            concept_completed="2026-03-12",
            first_mastery_date=date(2026, 3, 12),
            latest_mastery_date=date(2026, 4, 8),
            delayed_validation_due=None,
            delayed_validation_passed_date=date(2026, 4, 8),
            last_practice=date(2026, 4, 8),
            history_accuracies=("9/10",),
            review_due=date(2026, 4, 15),
            review_round=0,
        )
        homework_entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 7),
                session_title="概念课（重修）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="**盛言收尾评注**：示例",
                accuracy="—",
                judgment="概念课完成",
                weak_points="—",
            )
        ]
        archive_entries = [
            learning_state.ArchiveEntry(
                header_index=0,
                header="2026-04-08 概念课（重修2） + 练习课",
                entry_date=date(2026, 4, 8),
                skill_id="SK-002",
                fields={"技能点": "SK-002《测试技能》"},
            )
        ]

        concept_events = learning_state.collect_concept_events(
            [skill], homework_entries, archive_entries
        )
        rendered = learning_state.render_concept_completed_value(
            skill, concept_events["SK-002"]
        )

        self.assertEqual(
            rendered,
            "2026-03-12（重修 2026-04-07，重修2 2026-04-08）",
        )

    def test_render_session_archive_drafts_skips_archived_groups_and_extracts_core(self) -> None:
        homework_entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 3, 9),
                session_title="练习课：SK-001《旧技能》",
                skill_id="SK-001",
                skill_name="旧技能",
                body="",
                accuracy="10/10（100%）",
                judgment="✅ 已掌握",
                weak_points="无",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 8),
                session_title="概念课：SK-003《新技能》",
                skill_id="SK-003",
                skill_name="新技能",
                body=(
                    "**案例 dossier**：`resources/cases/2023-10_btc_three_framework_decision_dossier.md`\n"
                    "**案例切片**：2023-10 三框架共振窗口\n"
                    "**盛言开场案例**：示例案例\n"
                    "**当时已知信息**：只知道条件A和条件B\n"
                    "**当时未知信息**：不知道后续结果\n"
                    "**学习者当下判断**：先看边界，再下结论\n"
                    "**结果揭示**：结果后来验证了边界比直觉更重要\n"
                    "**偏差复盘**：别被表面叙事带走\n"
                    "**复述检验**：先看边界，再下结论"
                ),
                accuracy="—",
                judgment="概念课完成",
                weak_points="—",
            ),
            learning_state.HomeworkEntry(
                header_index=2,
                entry_date=date(2026, 4, 8),
                session_title="练习课（第1次）：SK-003《新技能》",
                skill_id="SK-003",
                skill_name="新技能",
                body=(
                    "**错误模式**：概念混淆（Q2 边界不清）、应用偏差（Q4 被表面现象带走）"
                ),
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="边界识别",
            ),
            learning_state.HomeworkEntry(
                header_index=3,
                entry_date=date(2026, 4, 8),
                session_title="练习课（第2次）：SK-003《新技能》",
                skill_id="SK-003",
                skill_name="新技能",
                body="**错误模式**：推导断链（Q8 直接跳到结论）",
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="最终薄弱点",
            ),
        ]
        archive_entries = [
            learning_state.ArchiveEntry(
                header_index=0,
                header="2026-03-09 练习课",
                entry_date=date(2026, 3, 9),
                skill_id="SK-001",
                fields={"技能点": "SK-001《旧技能》"},
            )
        ]

        drafts = learning_state.render_session_archive_drafts(
            homework_entries, archive_entries
        )

        self.assertNotIn("SK-001《旧技能》", drafts)
        self.assertIn("### 2026-04-08 概念课 + 练习课（自动草稿）", drafts)
        self.assertIn("**技能点**：SK-003《新技能》", drafts)
        self.assertIn(
            "**案例 dossier**：`resources/cases/2023-10_btc_three_framework_decision_dossier.md`",
            drafts,
        )
        self.assertIn("**案例切片**：2023-10 三框架共振窗口", drafts)
        self.assertIn("**本节核心**：先看边界，再下结论", drafts)
        self.assertIn("**遗留问题**：最终薄弱点", drafts)
        self.assertIn("**下次会话强制动作**：无", drafts)
        self.assertIn("**下次概念课建议追问**：概念边界辨析：概念课强制比较相邻概念", drafts)
        self.assertIn("**下次练习课建议题型**：概念边界辨析：上调 `辨析` 与 `直接应用` 占比", drafts)

    def test_session_archive_drafts_do_not_leak_future_hard_rules(self) -> None:
        homework_entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 8),
                session_title="概念课：SK-003《新技能》",
                skill_id="SK-003",
                skill_name="新技能",
                body=(
                    "**盛言开场案例**：示例案例\n"
                    "**当时已知信息**：条件A\n"
                    "**当时未知信息**：后续结果\n"
                    "**学习者当下判断**：先看边界\n"
                    "**结果揭示**：后续验证边界重要\n"
                    "**偏差复盘**：别被表面现象带走\n"
                    "**复述检验**：先看边界"
                ),
                accuracy="—",
                judgment="概念课完成",
                weak_points="—",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 9),
                session_title="练习课（第1次）：SK-003《新技能》",
                skill_id="SK-003",
                skill_name="新技能",
                body="**错误模式**：概念混淆（Q2）",
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="辨析",
            ),
            learning_state.HomeworkEntry(
                header_index=2,
                entry_date=date(2026, 4, 10),
                session_title="练习课（第2次）：SK-003《新技能》",
                skill_id="SK-003",
                skill_name="新技能",
                body="**错误模式**：概念混淆（Q5）",
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="辨析",
            ),
        ]

        drafts = learning_state.render_session_archive_drafts(homework_entries, [])
        concept_block = drafts.split("### 2026-04-08 概念课（自动草稿）", 1)[1].split("---", 1)[0]

        self.assertIn("**下次会话强制动作**：无", concept_block)

    def test_validate_homework_log_warns_when_concept_entry_is_not_structured(self) -> None:
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 8),
                session_title="概念课：SK-003《新技能》",
                skill_id="SK-003",
                skill_name="新技能",
                body="**盛言开场案例**：只有开场案例，没有其他字段",
                accuracy="—",
                judgment="概念课完成",
                weak_points="—",
            )
        ]

        warnings = learning_state.validate_homework_log(entries)

        self.assertEqual(len(warnings), 1)
        self.assertIn("missing structured fields", warnings[0])

    def test_build_mastery_records_tracks_method_failures_and_delayed_validation(self) -> None:
        skill = learning_state.Skill(
            skill_id="SK-002",
            name="测试技能",
            description="描述",
            prereq_text="无",
            prereqs=(),
            mastery_standard="10题答对8题",
            status="✅ 已掌握",
            concept_completed="2026-04-07（重修 2026-04-08）",
            first_mastery_date=date(2026, 4, 8),
            latest_mastery_date=date(2026, 4, 8),
            delayed_validation_due=None,
            delayed_validation_passed_date=date(2026, 4, 10),
            last_practice=date(2026, 4, 10),
            history_accuracies=("4/10", "6/10", "8/10"),
            review_due=date(2026, 4, 17),
            review_round=0,
        )
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 7),
                session_title="练习课（第1次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="**错误模式**：概念混淆（Q1）、边界遗漏（Q2）",
                accuracy="4/10（40%）",
                judgment="❌ 未掌握",
                weak_points="辨析、反例构造",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 8),
                session_title="概念课（重修）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="**盛言开场案例**：示例",
                accuracy="—",
                judgment="概念课完成",
                weak_points="—",
            ),
            learning_state.HomeworkEntry(
                header_index=2,
                entry_date=date(2026, 4, 8),
                session_title="练习课（第2次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="**错误模式**：概念混淆（Q3）、应用偏差（Q4）",
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="辨析、场景判断",
            ),
            learning_state.HomeworkEntry(
                header_index=3,
                entry_date=date(2026, 4, 8),
                session_title="练习课（第3次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="",
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="无",
            ),
            learning_state.HomeworkEntry(
                header_index=4,
                entry_date=date(2026, 4, 10),
                session_title="延迟验证：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="",
                accuracy="4/5（80%）",
                judgment="✅ 延迟验证通过",
                weak_points="无",
            ),
        ]

        records = learning_state.build_mastery_records([skill], entries)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].mastery_method, "概念重修后通过")
        self.assertEqual(records[0].attempt_count, 3)
        self.assertEqual(
            records[0].primary_failure_types,
            "概念混淆×2；应用偏差；边界遗漏",
        )
        self.assertEqual(records[0].delayed_validation, "是（2026-04-10）")

    def test_triggered_teaching_actions_map_repeated_errors_to_hard_actions(self) -> None:
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 7),
                session_title="练习课（第1次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="**错误模式**：概念混淆（Q1）、应用偏差（Q4）",
                accuracy="5/10（50%）",
                judgment="❌ 未掌握",
                weak_points="辨析、场景判断",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 8),
                session_title="练习课（第2次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="**错误模式**：概念混淆（Q2）、应用偏差（Q6）",
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="辨析、变形应用",
            ),
        ]

        triggers = learning_state.triggered_teaching_actions_for_skill(entries, "SK-002")
        summary = learning_state.summarize_mandatory_action_for_skill(entries, "SK-002")
        panel = learning_state.render_teaching_control_panel(entries, date(2026, 4, 8))

        self.assertEqual([trigger.error_mode for trigger in triggers], ["概念混淆", "应用偏差"])
        self.assertEqual(triggers[0].next_session, "概念重修")
        self.assertIn("连续2次概念混淆 → 概念重修", summary)
        self.assertIn("连续2次应用偏差 → 变式练习", summary)
        self.assertIn("### 已触发的硬规则", panel)
        self.assertIn("| SK-002：测试技能 | 概念混淆（连续2次） | 概念重修：先回概念课", panel)

    def test_hard_rule_streak_resets_after_mastery(self) -> None:
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 7),
                session_title="练习课（第1次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="**错误模式**：概念混淆（Q1）",
                accuracy="5/10（50%）",
                judgment="❌ 未掌握",
                weak_points="辨析",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 8),
                session_title="练习课（第2次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="**错误模式**：概念混淆（Q2）",
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="辨析",
            ),
            learning_state.HomeworkEntry(
                header_index=2,
                entry_date=date(2026, 4, 9),
                session_title="练习课（第3次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="",
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="无",
            ),
        ]

        triggers = learning_state.triggered_teaching_actions_for_skill(entries, "SK-002")

        self.assertEqual(triggers, [])

    def test_recent_error_modes_fall_back_to_latest_scored_entries_when_window_is_empty(self) -> None:
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 8),
                session_title="练习课（第1次）：SK-003《测试技能》",
                skill_id="SK-003",
                skill_name="测试技能",
                body="**错误模式**：概念混淆（Q1）、应用偏差（Q4）",
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="辨析、场景判断",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 9),
                session_title="练习课（第2次）：SK-003《测试技能》",
                skill_id="SK-003",
                skill_name="测试技能",
                body="**错误模式**：概念混淆（Q2）",
                accuracy="7/10（70%）",
                judgment="❌ 未掌握",
                weak_points="辨析",
            ),
        ]

        panel = learning_state.render_teaching_control_panel(entries, date(2026, 4, 23))

        self.assertIn("当前使用：最近2条有结果记录（回退）", panel)
        self.assertIn("| 概念混淆 | 2 |", panel)
        self.assertIn("| 应用偏差 | 1 |", panel)

    def test_render_operating_metrics_summarizes_weekly_progress_and_error_repeat_rate(self) -> None:
        skill = learning_state.Skill(
            skill_id="SK-002",
            name="测试技能",
            description="描述",
            prereq_text="无",
            prereqs=(),
            mastery_standard="10题答对8题",
            status="✅ 已掌握",
            concept_completed="2026-04-20",
            first_mastery_date=date(2026, 4, 21),
            latest_mastery_date=date(2026, 4, 21),
            delayed_validation_due=None,
            delayed_validation_passed_date=date(2026, 4, 22),
            last_practice=date(2026, 4, 22),
            history_accuracies=("5/10", "8/10"),
            review_due=date(2026, 4, 29),
            review_round=0,
        )
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 20),
                session_title="练习课（第1次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="**错误模式**：概念混淆（Q1）、应用偏差（Q4）",
                accuracy="5/10（50%）",
                judgment="❌ 未掌握",
                weak_points="辨析、场景判断",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 21),
                session_title="练习课（第2次）：SK-002《测试技能》",
                skill_id="SK-002",
                skill_name="测试技能",
                body="",
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="无",
            ),
            learning_state.HomeworkEntry(
                header_index=2,
                entry_date=date(2026, 4, 22),
                session_title="间隔复习（第1次）：SK-001《旧技能》",
                skill_id="SK-001",
                skill_name="旧技能",
                body="**错误模式**：概念混淆（Q2）",
                accuracy="8/10（80%）",
                judgment="🔄 复习完成",
                weak_points="无",
            ),
        ]

        metrics = learning_state.render_operating_metrics([skill], entries, date(2026, 4, 23))

        self.assertIn("| 每周新增稳定掌握 | 1 |", metrics)
        self.assertIn("| 每周消化复习债 | 1 |", metrics)
        self.assertIn("| 单技能平均首次达标次数 | 2.0 次 |", metrics)
        self.assertIn("| 高频错误重复率 | 2/3（67%） |", metrics)

    def test_render_content_effectiveness_metrics_tracks_case_follow_up_and_question_types(self) -> None:
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 20),
                session_title="练习课（第1次）：SK-004《通货膨胀的机制》",
                skill_id="SK-004",
                skill_name="通货膨胀的机制",
                body=(
                    "**Shaw 出题清单：**\n"
                    "| 编号 | 题目简述 | 题型 | 来源技能点 | 结果 |\n"
                    "|------|---------|------|-----------|------|\n"
                    "| 1 | 解释资产先涨 | 变形应用 | SK-004 | ✗ 只答 CPI |\n"
                    "| 2 | 区分货币通胀和价格通胀 | 辨析 | SK-004 | ⚠️ 还差一步。 |\n"
                    "**错误模式**：概念混淆（Q2）、应用偏差（Q1）"
                ),
                accuracy="5/10（50%）",
                judgment="❌ 未掌握",
                weak_points="辨析、变形应用",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 21),
                session_title="概念课：SK-004《通货膨胀的机制》",
                skill_id="SK-004",
                skill_name="通货膨胀的机制",
                body=(
                    "**案例 dossier**：`resources/cases/2020-2022_monetary_expansion_inflation_dossier.md`\n"
                    "**案例切片**：2020-2022 宽松扩张到 CPI 上行\n"
                    "**盛言开场案例**：2020-2022 宽松扩张到 CPI 上行\n"
                    "**当时已知信息**：流动性改善\n"
                    "**当时未知信息**：消费价格何时上行\n"
                    "**学习者当下判断**：先看资产与信用传导\n"
                    "**结果揭示**：后续 CPI 才反应\n"
                    "**偏差复盘**：不要把没涨 CPI 等同于没通胀\n"
                    "**复述检验**：通胀是带时滞的传导链"
                ),
                accuracy="—",
                judgment="概念课完成",
                weak_points="—",
            ),
            learning_state.HomeworkEntry(
                header_index=2,
                entry_date=date(2026, 4, 22),
                session_title="练习课（第2次）：SK-004《通货膨胀的机制》",
                skill_id="SK-004",
                skill_name="通货膨胀的机制",
                body=(
                    "**Shaw 出题清单：**\n"
                    "| 编号 | 题目简述 | 题型 | 来源技能点 | 结果 |\n"
                    "|------|---------|------|-----------|------|\n"
                    "| 1 | 解释资产先涨 | 变形应用 | SK-004 | ✓ |\n"
                    "| 2 | 区分货币通胀和价格通胀 | 辨析 | SK-004 | ✓ |\n"
                ),
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="无",
            ),
        ]

        metrics = learning_state.render_content_effectiveness_metrics(entries)

        self.assertIn("### 案例切片后续跟踪", metrics)
        self.assertIn("2020-2022 宽松扩张到 CPI 上行", metrics)
        self.assertIn("8/10 ✅ 掌握；主要重复错误已清零", metrics)
        self.assertIn("### 题型失误热度", metrics)
        self.assertIn("| 变形应用 | 1 | 2 | 50% |", metrics)
        self.assertIn("| 辨析 | 1 | 2 | 50% |", metrics)

    def test_sync_skill_graph_renders_full_document_and_mastery_records(self) -> None:
        skills = learning_state.parse_skill_graph(sample_skill_graph())
        homework_entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 3, 12),
                session_title="练习课（第1次）：SK-001《示例技能一》",
                skill_id="SK-001",
                skill_name="示例技能一",
                body="",
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="无",
            )
        ]
        concept_events = {
            "SK-001": [
                learning_state.ConceptEvent(date(2026, 3, 12), None, "skill_graph"),
                learning_state.ConceptEvent(date(2026, 4, 7), "重修", "homework_log"),
            ],
            "SK-002": [],
        }

        rendered = learning_state.sync_skill_graph(
            skills,
            homework_entries,
            date(2026, 3, 20),
            concept_events,
        )
        reparsed = learning_state.parse_skill_graph(rendered)

        self.assertEqual([skill.skill_id for skill in reparsed], ["SK-001", "SK-002"])
        self.assertIn("## 第一阶段：宏观框架（SK-001 ~ SK-018）", rendered)
        self.assertIn("### 主线A：货币 / 宏观 / 周期", rendered)
        self.assertIn("### SK-001：示例技能一", rendered)
        self.assertIn("- **主要参考资源**：", rendered)
        self.assertIn(
            "- **概念课完成**：2026-03-12（重修 2026-04-07）",
            rendered,
        )
        self.assertIn("## 掌握记录（按时间）", rendered)
        self.assertIn(
            "| SK-001 | 2026-03-12 | 首练通过 | 8/10 | 1 | 无 | 未记录 |",
            rendered,
        )
        self.assertIn("- **首次掌握日期**：2026-03-12", rendered)
        self.assertIn("- **最近达标日期**：2026-03-12", rendered)
        self.assertIn("- **延迟验证通过日期**：2026-03-12", rendered)
        self.assertIn("## 今日延迟验证", rendered)
        self.assertIn("## 今日复习队列", rendered)

    def test_pending_delayed_validation_blocks_unlock_and_review_due(self) -> None:
        skills = learning_state.parse_skill_graph(sample_skill_graph())
        pending_skills = [
            learning_state.replace(
                skills[0],
                status="✅ 已掌握",
                first_mastery_date=date(2026, 3, 12),
                latest_mastery_date=date(2026, 3, 12),
                delayed_validation_due=date(2026, 3, 14),
                delayed_validation_passed_date=None,
                review_due=None,
            ),
            skills[1],
        ]

        rendered = learning_state.render_skill_graph(
            pending_skills,
            [],
            date(2026, 3, 14),
        )

        self.assertIn("- **状态**：✅ 待延迟验证", rendered)
        self.assertIn("- **延迟验证到期**：2026-03-14", rendered)
        self.assertIn("- **复习到期**：—", rendered)
        current_section = rendered.split("## 当前可学习的技能点", 1)[1].split("## 技能点目录", 1)[0]
        self.assertNotIn("SK-002：示例技能二", current_section)
        delayed_section = rendered.split("## 今日延迟验证", 1)[1].split("## 今日复习队列", 1)[0]
        self.assertIn("SK-001：示例技能一（延迟验证到期 2026-03-14，今日到期）", delayed_section)

    def test_scheduling_policy_freezes_new_lessons_when_review_debt_hits_threshold(self) -> None:
        skills = learning_state.parse_skill_graph(sample_skill_graph())
        expanded_skills = [
            learning_state.replace(
                skills[0],
                skill_id="SK-001",
                name="示例技能一",
                prereq_text="无",
                prereqs=(),
                status="✅ 已掌握",
                first_mastery_date=date(2026, 3, 1),
                latest_mastery_date=date(2026, 3, 1),
                delayed_validation_due=None,
                delayed_validation_passed_date=date(2026, 3, 1),
                review_due=date(2026, 3, 8),
            ),
            learning_state.replace(
                skills[0],
                skill_id="SK-002",
                name="示例技能二",
                prereq_text="无",
                prereqs=(),
                status="✅ 已掌握",
                first_mastery_date=date(2026, 3, 2),
                latest_mastery_date=date(2026, 3, 2),
                delayed_validation_due=None,
                delayed_validation_passed_date=date(2026, 3, 2),
                review_due=date(2026, 3, 9),
            ),
            learning_state.replace(
                skills[0],
                skill_id="SK-003",
                name="示例技能三",
                prereq_text="无",
                prereqs=(),
                status="✅ 已掌握",
                first_mastery_date=date(2026, 3, 3),
                latest_mastery_date=date(2026, 3, 3),
                delayed_validation_due=None,
                delayed_validation_passed_date=date(2026, 3, 3),
                review_due=date(2026, 3, 10),
            ),
            learning_state.replace(
                skills[1],
                skill_id="SK-004",
                name="示例技能四",
                prereq_text="无",
                prereqs=(),
            ),
        ]

        policy = learning_state.scheduling_policy(expanded_skills, date(2026, 3, 20))
        learnable_section = learning_state.render_learnable_section(
            expanded_skills,
            {skill.skill_id: skill for skill in expanded_skills},
            date(2026, 3, 20),
        )

        self.assertEqual(policy.code, "freeze_new_lessons")
        self.assertIn("### 主线A：货币 / 宏观 / 周期", learnable_section)
        self.assertIn("*（空）*", learnable_section)
        self.assertIn("今日调度策略：默认冻结新课", learnable_section)
        self.assertIn("当前有 3 个技能点复习到期", learnable_section)

    def test_scheduling_policy_switches_to_review_only_at_five_due_reviews(self) -> None:
        skills = []
        template = learning_state.parse_skill_graph(sample_skill_graph())[0]
        for number in range(1, 6):
            skills.append(
                learning_state.replace(
                    template,
                    skill_id=f"SK-{number:03d}",
                    name=f"示例技能{number}",
                    prereq_text="无",
                    prereqs=(),
                    first_mastery_date=date(2026, 3, number),
                    latest_mastery_date=date(2026, 3, number),
                    delayed_validation_due=None,
                    delayed_validation_passed_date=date(2026, 3, number),
                    review_due=date(2026, 3, 10 + number),
                )
            )

        policy = learning_state.scheduling_policy(skills, date(2026, 3, 20))

        self.assertEqual(policy.code, "review_only")
        self.assertIn("只允许清理复习债", policy.detail)

    def test_review_due_queue_prioritizes_fragile_review_before_older_due(self) -> None:
        template = learning_state.parse_skill_graph(sample_skill_graph())[0]
        skills = [
            learning_state.replace(
                template,
                skill_id="SK-001",
                name="技能一",
                prereq_text="无",
                prereqs=(),
                first_mastery_date=date(2026, 3, 1),
                latest_mastery_date=date(2026, 3, 1),
                delayed_validation_due=None,
                delayed_validation_passed_date=date(2026, 3, 1),
                review_due=date(2026, 3, 10),
            ),
            learning_state.replace(
                template,
                skill_id="SK-002",
                name="技能二",
                prereq_text="无",
                prereqs=(),
                first_mastery_date=date(2026, 3, 2),
                latest_mastery_date=date(2026, 3, 2),
                delayed_validation_due=None,
                delayed_validation_passed_date=date(2026, 3, 2),
                review_due=date(2026, 3, 12),
            ),
        ]
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 3, 16),
                session_title="间隔复习：SK-002《技能二》（第1次复习）",
                skill_id="SK-002",
                skill_name="技能二",
                body="**错误模式**：概念混淆（Q1）、应用偏差（Q4）",
                accuracy="7/10（70%）",
                judgment="🔄 复习完成，掌握状态维持（未达8/10，但首次复习可维持）",
                weak_points="辨析、场景判断",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 3, 17),
                session_title="练习课：SK-001《技能一》",
                skill_id="SK-001",
                skill_name="技能一",
                body="**错误模式**：概念混淆（Q2）",
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="无",
            ),
        ]

        due_skills = learning_state.review_due_skills(skills, date(2026, 3, 20), entries)
        due_queue = learning_state.render_due_queue(skills, date(2026, 3, 20), entries)

        self.assertEqual([skill.skill_id for skill in due_skills], ["SK-002", "SK-001"])
        self.assertIn("SK-002：技能二（第1次复习到期 2026-03-12，已逾期 8 天；优先原因：上次复习仅维持", due_queue)

    def test_review_priority_ignores_old_failed_review_after_retraining(self) -> None:
        skill = learning_state.replace(
            learning_state.parse_skill_graph(sample_skill_graph())[0],
            skill_id="SK-001",
            name="技能一",
            prereq_text="无",
            prereqs=(),
            first_mastery_date=date(2026, 3, 1),
            latest_mastery_date=date(2026, 4, 7),
            delayed_validation_due=None,
            delayed_validation_passed_date=date(2026, 4, 7),
            review_due=date(2026, 4, 14),
        )
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 7),
                session_title="间隔复习：SK-001《技能一》（第2次复习）",
                skill_id="SK-001",
                skill_name="技能一",
                body="**错误模式**：概念混淆（Q1）",
                accuracy="4/6（67%）",
                judgment="❌ 未通过，状态回退至 🟡 学习中",
                weak_points="辨析",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 7),
                session_title="练习课：SK-001《技能一》",
                skill_id="SK-001",
                skill_name="技能一",
                body="**错误模式**：概念混淆（Q2）",
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="无",
            ),
        ]

        snapshot = learning_state.review_priority_snapshot(skill, entries, date(2026, 4, 23))

        self.assertNotIn("上次复习未通过", snapshot.reason)

    def test_dual_track_outputs_group_macro_and_risk_entry_points(self) -> None:
        template_skills = learning_state.parse_skill_graph(sample_skill_graph())
        skills = [
            learning_state.replace(
                template_skills[0],
                skill_id="SK-003",
                name="宏观前置",
                prereq_text="无",
                prereqs=(),
                review_due=None,
            ),
            learning_state.replace(
                template_skills[1],
                skill_id="SK-004",
                name="宏观新课",
                prereq_text="SK-003",
                prereqs=("SK-003",),
            ),
            learning_state.replace(
                template_skills[1],
                skill_id="SK-019",
                name="风险新课",
                prereq_text="无",
                prereqs=(),
            ),
        ]
        skills_by_id = {skill.skill_id: skill for skill in skills}

        learnable_section = learning_state.render_learnable_section(
            skills,
            skills_by_id,
            date(2026, 3, 20),
        )
        dual_track_progress = learning_state.render_dual_track_progress(
            skills,
            skills_by_id,
        )

        self.assertIn("### 主线A：货币 / 宏观 / 周期", learnable_section)
        self.assertIn("- SK-004：宏观新课", learnable_section)
        self.assertIn("### 主线B：风险 / 执行 / 交易结构", learnable_section)
        self.assertIn("- SK-019：风险新课", learnable_section)
        self.assertIn("| 主线A：货币 / 宏观 / 周期 |", dual_track_progress)
        self.assertIn("SK-004：宏观新课", dual_track_progress)
        self.assertIn("| 主线B：风险 / 执行 / 交易结构 |", dual_track_progress)
        self.assertIn("SK-019：风险新课", dual_track_progress)

    def test_sync_learner_profile_renders_teaching_control_panel_from_errors(self) -> None:
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 14),
                session_title="概念课：SK-003《示例技能三》",
                skill_id="SK-003",
                skill_name="示例技能三",
                body=(
                    "**盛言开场案例**：1971年政策切换\n"
                    "**当时已知信息**：制度刚变化\n"
                    "**当时未知信息**：后续价格与接受度\n"
                    "**学习者当下判断**：先看保障机制怎么变\n"
                    "**结果揭示**：结果证明先看保障机制是对的\n"
                    "**偏差复盘**：容易把社会共识当成第七条属性\n"
                    "**复述检验**：判断健全货币要先看底层保障机制。"
                ),
                accuracy="—",
                judgment="概念课完成",
                weak_points="—",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 15),
                session_title="练习课（第1次）：SK-001《示例技能一》",
                skill_id="SK-001",
                skill_name="示例技能一",
                body=(
                    "**薄弱题型**：辨析、场景判断\n"
                    "**错误模式**：概念混淆（Q1 边界不清）、应用偏差（Q4 被表面现象带走）"
                ),
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="辨析、场景判断",
            ),
            learning_state.HomeworkEntry(
                header_index=2,
                entry_date=date(2026, 4, 18),
                session_title="练习课（第2次）：SK-002《示例技能二》",
                skill_id="SK-002",
                skill_name="示例技能二",
                body=(
                    "**薄弱题型**：反例构造、批判性判断\n"
                    "**错误模式**：边界遗漏（Q6 未考虑极端条件）、推导断链（Q8 直接跳结论）"
                ),
                accuracy="7/10（70%）",
                judgment="❌ 未掌握",
                weak_points="反例构造、批判性判断",
            ),
            learning_state.HomeworkEntry(
                header_index=3,
                entry_date=date(2026, 4, 20),
                session_title="练习课（第3次）：SK-003《示例技能三》",
                skill_id="SK-003",
                skill_name="示例技能三",
                body=(
                    "**薄弱题型**：辨析、批判性判断\n"
                    "**错误模式**：概念混用（Q3 术语放错位置）、批判不足（Q9 缺少中间判断）"
                ),
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="辨析、批判性判断",
            ),
        ]

        synced = learning_state.sync_learner_profile(
            sample_learner_profile(),
            entries,
            date(2026, 4, 22),
        )

        self.assertIn("## 教学控制面板", synced)
        self.assertIn("## 概念课表现记录", synced)
        self.assertIn("| 2026-04-14 | SK-003：示例技能三 | 1971年政策切换 | 判断健全货币要先看底层保障机制。 | 容易把社会共识当成第七条属性 |", synced)
        self.assertIn("| 概念边界辨析 | 2 | SK-003, SK-001 |", synced)
        self.assertIn("| 框架纪律与中间判断 | 2 | SK-003, SK-002 |", synced)
        self.assertIn("| 概念混淆 | 2 |", synced)
        self.assertIn("| 推导断链 | 1 |", synced)
        self.assertIn("`概念边界辨析`：概念课强制比较相邻概念", synced)
        self.assertIn("`框架纪律与中间判断`：增加 `批判性判断` 与分步作答题", synced)
        self.assertIn("| 2026-04-20 | SK-003：示例技能三 | 8/10（80%） | ✅ 掌握 | 辨析、批判性判断 |", synced)

    def test_render_session_briefing_uses_archive_guidance_and_groups_priority_skills(self) -> None:
        skills = learning_state.parse_skill_graph(sample_skill_graph())
        homework_entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 3, 12),
                session_title="练习课（第1次）：SK-001《示例技能一》",
                skill_id="SK-001",
                skill_name="示例技能一",
                body="**错误模式**：概念混淆（Q1 边界不清）",
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="辨析",
            )
        ]
        archive_entries = [
            learning_state.ArchiveEntry(
                header_index=0,
                header="2026-03-12 练习课",
                entry_date=date(2026, 3, 12),
                skill_id="SK-001",
                fields={
                    "技能点": "SK-001《示例技能一》",
                    "状态变化": "8/10 ✅ 掌握",
                    "本节核心": "核心",
                    "盛言的评注": "评注",
                    "遗留问题": "继续盯住概念边界。",
                    "下次概念课建议追问": "概念边界辨析：先回答为什么不是另一个概念。",
                    "下次练习课建议题型": "概念边界辨析：先打辨析题。",
                },
            )
        ]

        briefing = learning_state.render_session_briefing(
            skills,
            homework_entries,
            archive_entries,
            date(2026, 3, 20),
        )

        self.assertIn("## 今日开场结论", briefing)
        self.assertIn("- **今日调度策略**：复习优先", briefing)
        self.assertIn("### SK-001：示例技能一", briefing)
        self.assertIn("- **建议模式**：复习课", briefing)
        self.assertIn("- **参考资源**：", briefing)
        self.assertIn("- **遗留问题**：继续盯住概念边界。", briefing)
        self.assertIn("- **强制教学动作**：无", briefing)
        self.assertIn("- **概念课建议追问**：概念边界辨析：先回答为什么不是另一个概念。", briefing)
        self.assertIn("- **练习课建议题型**：概念边界辨析：先打辨析题。", briefing)
        self.assertIn("- **Shaw 起手模板**：", briefing)
        self.assertIn("  - 前3题：辨析 → 直接应用 → 案例判断。", briefing)
        self.assertIn("## 双主线新课入口", briefing)
        self.assertIn("- **主线A：货币 / 宏观 / 周期**：SK-002：示例技能二", briefing)
        self.assertIn("## 如明确打破冻结，可开的新技能点", briefing)
        self.assertIn("### 主线A：货币 / 宏观 / 周期", briefing)
        self.assertIn("#### SK-002：示例技能二", briefing)
        self.assertIn("- **强制教学动作**：无", briefing)
        self.assertIn("- **首次练习时的 Shaw 起手模板**：", briefing)
        self.assertIn("- **信息切片案例模板**：", briefing)
        self.assertIn("- **建议案例强度**：入门切片（首次进入该技能点，先用低背景负担事件暴露原始框架。）", briefing)
        self.assertIn("- **入门切片**：1971-08 尼克松冲击与美元脱锚；塞浦路斯银行危机与资本管制", briefing)
        self.assertIn("- **标准切片**：2020-2022 宽松扩张到 CPI 上行；法币购买力被稀释时资产先涨后传导到消费品", briefing)
        self.assertIn("- **高压反例切片**：名义价格稳定但购买力持续走弱的阶段；制度未立刻崩溃却已开始侵蚀货币职能的阶段", briefing)
        self.assertIn("- **案例材料入口**：优先从 `resources/01_macro/` 里选一个历史货币制度或购买力变化事件切片", briefing)
        self.assertIn("- **案例母题**：第一阶段历史货币事件切片", briefing)
        self.assertIn("- **当时已知信息**：制度变化、货币媒介特征、当时参与者约束。", briefing)

    def test_session_briefing_promotes_concept_retry_when_hard_rule_hits(self) -> None:
        skills = learning_state.parse_skill_graph(sample_skill_graph())
        updated_skills = [
            skills[0],
            learning_state.replace(
                skills[1],
                status="🟡 学习中",
                concept_completed="2026-03-12",
            ),
        ]
        homework_entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 3, 18),
                session_title="练习课（第1次）：SK-002《示例技能二》",
                skill_id="SK-002",
                skill_name="示例技能二",
                body="**错误模式**：概念混淆（Q1）",
                accuracy="5/10（50%）",
                judgment="❌ 未掌握",
                weak_points="辨析",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 3, 19),
                session_title="练习课（第2次）：SK-002《示例技能二》",
                skill_id="SK-002",
                skill_name="示例技能二",
                body="**错误模式**：概念混淆（Q3）",
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="辨析",
            ),
        ]

        briefing = learning_state.render_session_briefing(
            updated_skills,
            homework_entries,
            [],
            date(2026, 3, 20),
        )

        self.assertIn("### SK-002：示例技能二", briefing)
        self.assertIn("- **建议模式**：概念重修", briefing)
        self.assertIn("- **强制教学动作**：连续2次概念混淆 → 概念重修", briefing)
        self.assertIn("  - 暂停练习。先安排概念重修，不进入 Shaw 出题。", briefing)

    def test_promote_archive_drafts_moves_new_draft_into_archive(self) -> None:
        archive_text = textwrap.dedent(
            """\
            # 历史会话存档（session_archive.md）

            > 测试夹具

            ---

            ## 存档记录

            ### 2026-03-12 练习课

            **技能点**：SK-001《示例技能一》
            **状态变化**：8/10 ✅ 掌握
            **本节核心**：核心一
            **盛言的评注**：评注一
            **遗留问题**：遗留一
            """
        )
        draft_text = textwrap.dedent(
            """\
            # 会话存档草稿（session_archive_drafts.md）

            > 测试夹具

            ---

            ### 2026-03-18 练习课（自动草稿）

            **技能点**：SK-002《示例技能二》
            **状态变化**：6/10 ❌ 未掌握
            **本节核心**：核心二
            **盛言的评注**：评注二
            **遗留问题**：遗留二
            **下次会话强制动作**：无
            """
        )
        homework_entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 3, 18),
                session_title="练习课（第1次）：SK-002《示例技能二》",
                skill_id="SK-002",
                skill_name="示例技能二",
                body="**错误模式**：概念混淆（Q1）",
                accuracy="6/10（60%）",
                judgment="❌ 未掌握",
                weak_points="辨析",
            )
        ]

        promoted_archive, promoted_headers = learning_state.promote_archive_drafts(
            archive_text,
            draft_text,
        )
        promoted_entries = learning_state.parse_session_archive_entries(promoted_archive)
        rendered_drafts = learning_state.render_session_archive_drafts(
            homework_entries,
            promoted_entries,
        )

        self.assertEqual(promoted_headers, ["2026-03-18 练习课"])
        self.assertIn("### 2026-03-18 练习课", promoted_archive)
        self.assertNotIn("自动草稿", promoted_archive)
        self.assertIn("**下次会话强制动作**：无", promoted_archive)
        self.assertIn("*（空）*", rendered_drafts)

    def test_validate_session_archive_entries_accepts_case_trace_fields(self) -> None:
        errors, warnings = learning_state.validate_session_archive_entries(
            [
                learning_state.ArchiveEntry(
                    header_index=0,
                    header="2026-04-24 概念课",
                    entry_date=date(2026, 4, 24),
                    skill_id="SK-004",
                    fields={
                        "技能点": "SK-004《通货膨胀的机制》",
                        "案例 dossier": "`resources/cases/2020-2022_monetary_expansion_inflation_dossier.md`",
                        "案例切片": "2020-2022 宽松扩张到 CPI 上行",
                        "状态变化": "⬜ 未学 → 🔵 概念已完成",
                        "本节核心": "通胀是带时滞的传导链。",
                        "盛言的评注": "先看传导，不要只看 CPI。",
                        "遗留问题": "需尽快进入练习课。",
                    },
                )
            ]
        )

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_promote_archive_drafts_skips_existing_coverage(self) -> None:
        archive_text = textwrap.dedent(
            """\
            # 历史会话存档（session_archive.md）

            > 测试夹具

            ---

            ### 2026-03-18 练习课

            **技能点**：SK-002《示例技能二》
            **状态变化**：6/10 ❌ 未掌握
            **本节核心**：核心二
            **盛言的评注**：评注二
            **遗留问题**：遗留二
            """
        )
        draft_text = textwrap.dedent(
            """\
            # 会话存档草稿（session_archive_drafts.md）

            > 测试夹具

            ---

            ### 2026-03-18 练习课（自动草稿）

            **技能点**：SK-002《示例技能二》
            **状态变化**：6/10 ❌ 未掌握
            **本节核心**：核心二
            **盛言的评注**：评注二
            **遗留问题**：遗留二
            """
        )

        promoted_archive, promoted_headers = learning_state.promote_archive_drafts(
            archive_text,
            draft_text,
        )

        self.assertEqual(promoted_headers, [])
        self.assertEqual(
            promoted_archive,
            learning_state.normalize_session_archive(archive_text),
        )

    def test_build_unified_diff_mentions_target_file(self) -> None:
        path = ROOT / "teacher" / "progress.md"

        diff = learning_state.build_unified_diff(
            path,
            "old line\n",
            "new line\n",
        )

        self.assertIn("a/teacher/progress.md", diff)
        self.assertIn("b/teacher/progress.md", diff)
        self.assertIn("-old line", diff)
        self.assertIn("+new line", diff)

    def test_write_backup_snapshot_copies_existing_file_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_file = temp_root / "teacher" / "progress.md"
            source_file.parent.mkdir(parents=True, exist_ok=True)
            source_file.write_text("before\n")
            backup_root = temp_root / "snapshots"

            backup_dir = learning_state.write_backup_snapshot(
                {source_file: "after\n"},
                backup_root=backup_root,
            )

            self.assertIsNotNone(backup_dir)
            assert backup_dir is not None
            backup_file = backup_dir / "progress.md"
            self.assertTrue(backup_file.exists())
            self.assertEqual(backup_file.read_text(), "before\n")

    def test_validate_generated_freshness_flags_stale_current_system_date(self) -> None:
        errors = learning_state.validate_generated_freshness(
            {
                ROOT / "teacher" / "session_briefing.md": (
                    "- **当前系统日期**：2026-04-24\n"
                )
            },
            date(2026, 4, 26),
        )

        self.assertEqual(len(errors), 1)
        self.assertIn("stale 当前系统日期 2026-04-24", errors[0])
        self.assertIn("expected 2026-04-26", errors[0])

    def test_content_metrics_track_resource_trace_and_question_bank_ids(self) -> None:
        entries = [
            learning_state.HomeworkEntry(
                header_index=0,
                entry_date=date(2026, 4, 21),
                session_title="概念课：SK-004《通货膨胀的机制》",
                skill_id="SK-004",
                skill_name="通货膨胀的机制",
                body=(
                    "**案例 dossier**：`resources/cases/2020-2022_monetary_expansion_inflation_dossier.md`\n"
                    "**案例切片**：2020-2022 宽松扩张到 CPI 上行\n"
                    "**资源段落**：`execution_decision_framework_guide.md#流动性传导`\n"
                    "**证据包条目**：CPI 时间线 + 资产价格截面\n"
                    "**图示编号**：稳定币传导链图\n"
                    "**盛言开场案例**：2020-2022 宽松扩张\n"
                    "**当时已知信息**：流动性改善\n"
                    "**当时未知信息**：消费价格何时上行\n"
                    "**学习者当下判断**：先看资产与信用传导\n"
                    "**结果揭示**：后续 CPI 才反应\n"
                    "**偏差复盘**：不要把没涨 CPI 等同于没通胀\n"
                    "**复述检验**：通胀是带时滞的传导链"
                ),
                accuracy="—",
                judgment="概念课完成",
                weak_points="—",
            ),
            learning_state.HomeworkEntry(
                header_index=1,
                entry_date=date(2026, 4, 22),
                session_title="练习课（第1次）：SK-004《通货膨胀的机制》",
                skill_id="SK-004",
                skill_name="通货膨胀的机制",
                body=(
                    "**Shaw 出题清单：**\n"
                    "| 编号 | 题库题号 | 题目简述 | 题型 | 来源技能点 | 结果 |\n"
                    "|------|---------|---------|------|-----------|------|\n"
                    "| 1 | QB-SK-004-01 | 区分货币通胀和价格通胀 | 辨析 | SK-004 | ✓ |\n"
                    "| 2 | QB-SK-004-02 | 解释资产先涨 | 变形应用 | SK-004 | ✗ 只答 CPI |\n"
                    "**题库来源**：`resources/question_banks/SK-004_inflation_mechanism_bank.md`\n"
                    "**使用资源段落**：`resources/cases/2020-2022_monetary_expansion_inflation_dossier.md#评分点`\n"
                    "**使用图示**：货币扩张传导链\n"
                    "**错误模式**：应用偏差（Q2）"
                ),
                accuracy="8/10（80%）",
                judgment="✅ 掌握",
                weak_points="变形应用",
            ),
        ]

        metrics = learning_state.render_content_effectiveness_metrics(entries)

        self.assertIn("### 资源使用后续跟踪", metrics)
        self.assertIn("资源：`execution_decision_framework_guide.md#流动性传导`", metrics)
        self.assertIn("证据包条目：CPI 时间线 + 资产价格截面", metrics)
        self.assertIn("图示编号：稳定币传导链图", metrics)
        self.assertIn("资源：`resources/cases/2020-2022_monetary_expansion_inflation_dossier.md#评分点`", metrics)
        self.assertIn("图示编号：货币扩张传导链", metrics)
        self.assertIn("### 题库题号效果", metrics)
        self.assertIn("| QB-SK-004-02 | 1 | 1 | 100% |", metrics)
        self.assertIn("| QB-SK-004-01 | 0 | 1 | 0% |", metrics)


if __name__ == "__main__":
    unittest.main()
