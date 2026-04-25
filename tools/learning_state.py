#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import difflib
import re
import sys
from dataclasses import dataclass, replace
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEACHER_DIR = ROOT / "teacher"
SKILL_GRAPH_PATH = TEACHER_DIR / "skill_graph.md"
PROGRESS_PATH = TEACHER_DIR / "progress.md"
HOMEWORK_LOG_PATH = TEACHER_DIR / "homework_log.md"
SESSION_ARCHIVE_PATH = TEACHER_DIR / "session_archive.md"
SESSION_ARCHIVE_DRAFTS_PATH = TEACHER_DIR / "session_archive_drafts.md"
LEARNER_PROFILE_PATH = TEACHER_DIR / "learner_profile.md"
SESSION_BRIEFING_PATH = TEACHER_DIR / "session_briefing.md"
BACKUP_ROOT = TEACHER_DIR / ".state_backups"

MASTERED_PREFIXES = ("✅", "🔄", "💚")
ACTIVE_PREFIXES = ("🔵", "🟡")
ALLOWED_STATUS_PREFIXES = {"🔒", "⬜", "🔵", "🟡", "✅", "🔄", "💚"}
STAGE_DEFINITIONS = (
    (1, 18, "第一阶段：宏观框架"),
    (19, 30, "第二阶段：风险管理"),
    (31, 42, "第三阶段：链上数据"),
    (43, 57, "第四阶段：交易实操"),
)
TRACK_DEFINITIONS = (
    (
        "macro_cycle",
        "主线A：货币 / 宏观 / 周期",
        ((1, 18), (31, 42)),
        "先建立货币与宏观框架，再用链上数据强化周期判断。",
    ),
    (
        "risk_execution",
        "主线B：风险 / 执行 / 交易结构",
        ((19, 30), (43, 57)),
        "尽早训练风险纪律，并逐步进入交易执行与结构判断。",
    ),
)
ERROR_MODE_PATTERNS = (
    ("概念混淆", ("概念混淆", "概念混用", "轻微概念混淆")),
    ("推导断链", ("推导断链",)),
    ("应用偏差", ("应用偏差",)),
    ("叙事替代推理", ("叙事替代推理",)),
    ("结果倒推", ("结果倒推",)),
    ("边界遗漏", ("边界遗漏",)),
    ("计算错误", ("计算错误",)),
    ("基础记忆缺失", ("基础记忆缺失",)),
    ("批判不足", ("批判不足",)),
)
WEAKNESS_PATTERNS = (
    ("概念边界辨析", ("概念混淆", "概念混用", "轻微概念混淆", "辨析", "边界识别", "属性混淆", "记账单位", "可替换", "便携", "稀缺", "耐久")),
    ("场景应用迁移", ("应用偏差", "直接应用", "场景判断", "变形应用", "案例判断", "场景应用", "健全性判定")),
    ("边界条件与反例构造", ("边界遗漏", "反例构造", "极端条件", "反驳")),
    ("框架纪律与中间判断", ("推导断链", "批判性判断", "框架纪律", "中间判断", "批判不足")),
    ("基础记忆提取", ("基础记忆缺失", "列举", "记忆缺失")),
)
WEAKNESS_RECOMMENDATIONS = {
    "概念边界辨析": {
        "meaning": "相邻概念边界不稳，容易把正确术语放到错误位置。",
        "concept": "概念课强制比较相邻概念，要求回答“为什么不是另一个”。",
        "practice": "上调 `辨析` 与 `直接应用` 占比，连续追打最易混的两组概念。",
    },
    "场景应用迁移": {
        "meaning": "概念能背出，但迁移到真实场景时容易被表面现象带走。",
        "concept": "概念课必须从历史场景回推原则，并显式说明关键判断依据。",
        "practice": "上调 `场景判断`、`变形应用`、`案例判断` 占比。",
    },
    "边界条件与反例构造": {
        "meaning": "知道原则，但对失效边界和反例不敏感。",
        "concept": "每节概念课至少构造一个失败场景，要求学习者说出原则何时不成立。",
        "practice": "增加 `反例构造` 与边界条件题，不接受只给结论。",
    },
    "框架纪律与中间判断": {
        "meaning": "容易直接跳结论，缺中间判断步骤和框架纪律。",
        "concept": "盛言必须追问“你中间哪一步做了什么判断”，不接受跳步。",
        "practice": "增加 `批判性判断` 与分步作答题，要求显式列出推理链。",
    },
    "基础记忆提取": {
        "meaning": "基础清单提取不稳，会拖慢后续应用和辨析。",
        "concept": "概念课收尾前增加压缩复述，要求完整列出最小要点清单。",
        "practice": "增加 `直接应用` 和快速口头提取题，先稳住基本枚举能力。",
    },
}
ERROR_ACTION_RULES = {
    "概念混淆": {
        "bucket": "concept_rebuild",
        "next_session": "概念重修",
        "detail": "先回概念课，强制比较相邻概念并回答“为什么不是另一个”。",
    },
    "叙事替代推理": {
        "bucket": "concept_rebuild",
        "next_session": "概念重修",
        "detail": "先回案例切片，禁止用叙事代替因果链。",
    },
    "结果倒推": {
        "bucket": "concept_rebuild",
        "next_session": "概念重修",
        "detail": "先回案例切片，只给当时信息，不允许先看结果。",
    },
    "推导断链": {
        "bucket": "structured_practice",
        "next_session": "分步练习",
        "detail": "下次作答必须显式写出中间判断，不接受直接结论。",
    },
    "批判不足": {
        "bucket": "structured_practice",
        "next_session": "分步练习",
        "detail": "下次先列判断依据再给结论，必须补齐批判步骤。",
    },
    "应用偏差": {
        "bucket": "variant_practice",
        "next_session": "变式练习",
        "detail": "下次练习前4题强制做场景变形，不出纯记忆题起手。",
    },
    "边界遗漏": {
        "bucket": "variant_practice",
        "next_session": "反例/边界练习",
        "detail": "下次先做边界条件与反例题，要求说明命题何时失效。",
    },
    "计算错误": {
        "bucket": "targeted_drill",
        "next_session": "计算短打",
        "detail": "下次先做3题计算短打，再进入综合题。",
    },
    "基础记忆缺失": {
        "bucket": "targeted_drill",
        "next_session": "基础提取短打",
        "detail": "下次先做最小要点提取，再进入场景题。",
    },
}
ACTION_BUCKET_ORDER = {
    "concept_rebuild": 0,
    "structured_practice": 1,
    "variant_practice": 2,
    "targeted_drill": 3,
}
CATEGORY_STARTER_TYPES = {
    "概念边界辨析": ("辨析", "直接应用"),
    "场景应用迁移": ("案例判断", "变形应用"),
    "边界条件与反例构造": ("反例构造", "案例判断"),
    "框架纪律与中间判断": ("案例判断", "变形应用"),
    "基础记忆提取": ("直接应用", "辨析"),
}
CASE_DIFFICULTY_LEVELS = ("入门切片", "标准切片", "高压反例切片")
CASE_TEMPLATE_STAGE_DEFAULTS = {
    1: {
        "theme": "第一阶段历史货币事件切片",
        "source": "优先从 `resources/01_macro/` 里选一个历史货币制度或购买力变化事件切片，必要时补 `resources/01_macro/bitcoin_whitepaper_guide.md` 的机制段落。",
        "known": "制度变化、货币媒介特征、当时参与者约束。",
        "unknown": "后续购买力、货币地位和使用行为会如何变化。",
        "question": "这个场景里，最先变化的货币机制是什么？它会怎么传导到职能或购买力？",
        "reveal": "先让学习者给出因果链，再揭示后续购买力或货币地位如何变化。",
        "retro": "重点复盘有没有把属性、职能和结果混在一起解释。",
    },
    2: {
        "theme": "第二阶段交易决策节点切片",
        "source": "优先从 `resources/04_trading/execution_decision_framework_guide.md` 里抽一个执行决策节点，再用 `resources/02_risk/` 中的风险材料补充偏差或结构性风险。",
        "known": "入场理由、风险预算、仓位约束、当时能看到的市场信息。",
        "unknown": "这笔交易最后赚还是亏，市场后面怎么走。",
        "question": "只看当时信息集，这个决策值不值得做？风险报酬比在哪里？",
        "reveal": "先记录学习者的决策与依据，再揭示最终盈亏和后续走势。",
        "retro": "重点复盘有没有把结果质量误当成决策质量。",
    },
    3: {
        "theme": "第三阶段链上数据截面切片",
        "source": "优先从 `resources/03_onchain/glassnode_onchain_metrics_guide.md` 里选一个具体指标读数截面，再回到原始宏观背景解释它为什么重要。",
        "known": "指定日期的链上指标读数、价格位置和筹码行为。",
        "unknown": "后续市场如何演化，指标是否被后验验证。",
        "question": "这组链上数据当下最支持什么判断？证据链缺哪一环？",
        "reveal": "先要求给出周期判断和证据，再揭示后续行情与指标延续/失效。",
        "retro": "重点复盘有没有把单一指标当成完整结论。",
    },
    4: {
        "theme": "第四阶段交易执行快照",
        "source": "优先从 `resources/04_trading/` 中选一个真实执行场景，必要时联合 `resources/03_onchain/` 的周期读数做三框架判断。",
        "known": "入场位、止损位、结构位置、流动性和执行约束。",
        "unknown": "成交后价格如何运行，计划是否被破坏。",
        "question": "这笔单子该不该做；如果做，仓位、止损和失效条件是什么？",
        "reveal": "先锁定执行计划，再揭示成交后的走势和执行结果。",
        "retro": "重点复盘有没有先有结论再补风险管理。",
    },
}
CASE_LIBRARY_STAGE_DEFAULTS = {
    1: {
        "入门切片": (
            "1971-08 尼克松冲击与美元脱锚",
            "塞浦路斯银行危机与资本管制",
        ),
        "标准切片": (
            "2020-2022 宽松扩张到 CPI 上行",
            "法币购买力被稀释时资产先涨后传导到消费品",
        ),
        "高压反例切片": (
            "名义价格稳定但购买力持续走弱的阶段",
            "制度未立刻崩溃却已开始侵蚀货币职能的阶段",
        ),
    },
    2: {
        "入门切片": (
            "守纪律亏损 vs 违纪律盈利的对照交易",
            "一次止损后反弹 vs 一次不止损深亏",
        ),
        "标准切片": (
            "2022-11 FTX 挤兑与账户资产不可得",
            "高杠杆环境下仓位计算失真导致的被动退出",
        ),
        "高压反例切片": (
            "结果赚钱但决策结构明显错误的交易",
            "平台表面稳定但底层可得性已恶化的情景",
        ),
    },
    3: {
        "入门切片": (
            "2020-03-12 恐慌底部的链上盈利切片",
            "2021-11-08 顶部区间的 MVRV / NUPL 截面",
        ),
        "标准切片": (
            "2022-11 FTX 后的去杠杆与链上重定价",
            "SOPR 反复跌破 1.0 又被压回的熊市阶段",
        ),
        "高压反例切片": (
            "单一指标指向乐观、但其他指标并未确认的错配场景",
            "价格短反弹但链上盈利结构未改善的诱多阶段",
        ),
    },
    4: {
        "入门切片": (
            "2020-03 流动性危机中的盘口抽空",
            "2021-11 顶部区间的高资金费率与高 OI",
        ),
        "标准切片": (
            "2025-10 闪崩中的清算链条",
            "同方向判断下，现货 vs 永续 vs 交割合约的执行差异",
        ),
        "高压反例切片": (
            "方向判断正确但工具选择错误导致先被强平的情景",
            "盘口短暂恢复却不足以承接连锁清算的二次冲击场景",
        ),
    },
}
CASE_LIBRARY_SKILL_OVERRIDES = {
    "SK-004": {
        "入门切片": (
            "2020-03 疫情宽松启动",
            "央行扩表后资产先涨的早期阶段",
        ),
        "标准切片": (
            "2021-2022 资产先涨、商品后涨",
            "购买力稀释如何跨阶段传导到生活成本",
        ),
        "高压反例切片": (
            "1970s 美国通胀螺旋",
            "货币扩张后价格未同步上行的时滞误判场景",
        ),
    },
    "SK-019": {
        "入门切片": (
            "守纪律亏损 vs 违纪律盈利",
            "计划完整但结果不佳的交易",
        ),
        "标准切片": (
            "突破追单被止损但计划正确",
            "侥幸扛单盈利但决策结构很差",
        ),
        "高压反例切片": (
            "连续两笔好决策亏损后是否开始改规则",
            "结果漂亮却完全违背计划的高诱惑样本",
        ),
    },
    "SK-027": {
        "入门切片": (
            "2022-11 FTX 挤兑与提现冻结",
            "用户先看到信用折价、后感知资产不可得",
        ),
        "标准切片": (
            "平台信用折价扩散到用户资产可得性",
            "稳定币挤兑需求如何放大托管风险",
        ),
        "高压反例切片": (
            "平台界面余额正常但提现通道恶化的情景",
            "价格暂稳却应优先撤离托管风险的时点",
        ),
    },
    "SK-028": {
        "入门切片": (
            "Mango Markets 预言机操纵",
            "单一价格源失真如何触发系统性损失",
        ),
        "标准切片": (
            "Euler Finance 攻击后的多层扩散",
            "桥接或多签失效引发的协议信任坍塌",
        ),
        "高压反例切片": (
            "审计通过但权限层过度集中导致的失效",
            "不是代码 bug 而是授权 / 前端 / 外部依赖先出问题的场景",
        ),
    },
    "SK-043": {
        "入门切片": (
            "现货持仓 vs 永续持仓在同一波动路径下的差异",
            "季度合约临近到期时的基差变化",
        ),
        "标准切片": (
            "高资金费率环境下为什么工具选择先于方向判断",
            "同样判断下，交割合约和永续的成本结构差异",
        ),
        "高压反例切片": (
            "方向判断正确但永续仓位先被强平的情景",
            "选择错误工具导致风险结构先失控的案例",
        ),
    },
    "SK-052": {
        "入门切片": (
            "宏观环境改善但链上与技术结构尚未完全同步的过渡阶段",
            "单一框架看多、其余两层仍在确认的等待场景",
        ),
        "标准切片": (
            "2023-10 BTC 三框架同时转强的决策窗口",
            "宏观、链上、结构出现共振时如何定义入场与风险",
        ),
        "高压反例切片": (
            "三框架只有一层成立却强行重仓的误判",
            "只因价格突破就忽略宏观与链上不确认的假共振场景",
        ),
    },
    "SK-055": {
        "入门切片": (
            "2022-05-07 至 2022-05-12 UST 脱锚过程",
            "Curve 池失衡与赎回压力放大",
        ),
        "标准切片": (
            "LUNA 承接压力如何转成死亡螺旋",
            "轻微脱锚如何演化成信心坍塌",
        ),
        "高压反例切片": (
            "价格短暂回稳却已无法恢复结构信任的阶段",
            "把“暂时稳住”误判成“机制仍然可靠”的反例",
        ),
    },
    "SK-056": {
        "入门切片": (
            "2025-10 闪崩前的高 OI / 极端资金费率组合",
            "宏观冲击触发的去杠杆链条",
        ),
        "标准切片": (
            "盘口抽空如何放大小幅外部冲击",
            "强平单如何连续吃穿盘口",
        ),
        "高压反例切片": (
            "消息不算大但杠杆结构极脆弱时的闪崩放大",
            "价格短反弹却因流动性不足再度触发二次踩踏",
        ),
    },
    "SK-053": {
        "入门切片": (
            "2020-03-12 BTC 单日从 7900 跌至 3800",
            "恐慌去杠杆下的链上盈利切片",
        ),
        "标准切片": (
            "全球流动性危机如何传导到 BTC",
            "极端抛压后为什么仍要区分流动性冲击与基本面失效",
        ),
        "高压反例切片": (
            "把恐慌暴跌直接误判成长期逻辑破产",
            "只看价格跌幅，不看执行条件与链上筹码重定价",
        ),
    },
    "SK-054": {
        "入门切片": (
            "2021-11-08 BTC 顶部区间与高盈利状态",
            "LTH 分发与链上过热信号",
        ),
        "标准切片": (
            "顶部附近为什么价格创新高不代表风险下降",
            "离场信号往往先出现在结构，而不是新闻",
        ),
        "高压反例切片": (
            "价格还在涨就继续加仓，忽略过热和分发信号",
            "把高情绪阶段误判成趋势最安全的阶段",
        ),
    },
}
CASE_TEMPLATE_SKILL_OVERRIDES = {
    "SK-004": {
        "theme": "2020-2022 货币扩张与物价传导切片",
        "source": "优先读 `resources/cases/2020-2022_monetary_expansion_inflation_dossier.md`，再补《Broken Money》里法币稀释与购买力传导的章节与 ARK Invest Bitcoin research report 的宏观流动性框架（local-only source material）。",
        "known": "宽松政策启动、货币供给显著扩张、居民和资产负债表先被推高。",
        "unknown": "消费价格何时明显反应，先涨资产还是先涨生活成本，购买力稀释如何传导。",
        "question": "如果货币供给先扩张、超市价格却没立刻跳涨，你会先追哪条传导链？",
        "reveal": "先要求画出“货币供给→信用/资产→商品与工资→购买力”的链条，再揭示后续物价上行与时滞。",
        "retro": "重点复盘有没有把“货币通胀”直接等同于“所有价格当天上涨”。",
    },
    "SK-019": {
        "theme": "两笔交易：守纪律亏损 vs 违纪律盈利",
        "source": "优先读 `resources/cases/decision_quality_vs_result_quality_dossier.md`，再补 `resources/04_trading/execution_decision_framework_guide.md` 的“决策质量 vs 结果质量”段落与《Trading in the Zone》的概率思维视角。",
        "known": "两笔交易在入场前的逻辑、仓位风险、止损计划和执行纪律。",
        "unknown": "最终哪笔赚钱、哪笔亏钱，以及市场后续如何运行。",
        "question": "不看结果，只看决策前信息集，哪一笔决策质量更高？为什么？",
        "reveal": "先锁定学习者对决策质量的判断，再揭示“好决策亏钱、坏决策赚钱”的结果反差。",
        "retro": "重点复盘有没有因为结果好坏而倒推决策本身的质量。",
    },
    "SK-027": {
        "theme": "FTX 流动性挤兑与用户资产不可得切片",
        "source": "优先读 `resources/cases/2022-11_ftx_bank_run_dossier.md`，再补 `resources/02_risk/stablecoin_liquidity_risk_guide.md` 的风险传导链与 `resources/04_trading/exchange_microstructure_guide.md` 的提现/流动性视角。",
        "known": "平台资产负债表开始被质疑，稳定币和主流币提现需求上升，二级市场对平台信用折价扩大。",
        "unknown": "平台还能否正常兑付，挤兑会不会从个别资产扩散到整体账户体系。",
        "question": "当你发现平台信用开始被质疑时，第一优先判断应该是什么：价格、余额，还是可提现性？",
        "reveal": "先要求学习者画出“信用受损→挤兑→流动性不足→资产不可得”的链条，再揭示平台冻结或破产如何影响用户。",
        "retro": "重点复盘有没有把屏幕上的余额错当成已经隔离托管的资产。",
    },
    "SK-028": {
        "theme": "DeFi 协议被攻击后的多层失效切片",
        "source": "优先读 `resources/cases/mango_markets_oracle_manipulation_dossier.md`，再补 `resources/02_risk/ethereum_defi_risk_structure_guide.md` 的六类攻击面与 `resources/02_risk/stablecoin_liquidity_risk_guide.md` 的流动性池失衡视角。",
        "known": "协议依赖预言机、可升级合约和流动性池，异常交易开始出现，链上授权与价格波动同步放大。",
        "unknown": "问题是单点代码漏洞、预言机操纵，还是治理/桥接层失效；损失会扩散到哪一层。",
        "question": "只看当时信息，你会先怀疑代码、预言机、权限，还是用户授权层？为什么？",
        "reveal": "先要求学习者按风险层次排序怀疑对象，再揭示真实攻击面和损失如何扩散。",
        "retro": "重点复盘有没有把所有 DeFi 风险都粗暴归结成“智能合约有 bug”。",
    },
    "SK-043": {
        "theme": "同一方向判断下，现货 vs 永续 vs 交割合约的执行切片",
        "source": "优先读 `resources/cases/spot_perpetual_delivery_execution_dossier.md`，再补 `resources/04_trading/derivatives_and_funding_rate_guide.md` 的三种工具比较与 `resources/04_trading/exchange_microstructure_guide.md` 的成交/流动性约束。",
        "known": "同一交易判断下，三种工具的保证金占用、到期机制、资金费率和流动性条件不同。",
        "unknown": "哪种工具最匹配当前场景，风险会先从方向暴露、资金费率还是清算机制显形。",
        "question": "如果你判断方向对，但不确定路径和时间，三种工具里哪一种最不容易把你先送出场？",
        "reveal": "先让学习者比较成本和风险结构，再揭示不同工具在同一行情路径下的结果差异。",
        "retro": "重点复盘有没有把“看对方向”误当成“任何工具都一样好”。",
    },
    "SK-052": {
        "theme": "三框架协同判断：宏观 + 链上 + 结构共振切片",
        "source": "优先读 `resources/cases/2023-10_btc_three_framework_decision_dossier.md`，再补 `resources/03_onchain/glassnode_onchain_metrics_guide.md` 与 `resources/04_trading/execution_decision_framework_guide.md`。",
        "known": "宏观流动性边际改善信号开始出现，链上盈利与筹码结构转强，价格重返关键结构位。",
        "unknown": "三层共振是否足以支撑入场，还是只是局部框架先行、其余两层尚未确认。",
        "question": "如果宏观、链上、技术结构三层里只有两层偏多，你会直接入场，还是继续等待？差的那一层决定什么？",
        "reveal": "先要求学习者给出三层各自结论和权重，再揭示后续走势与哪些信号真正起了确认作用。",
        "retro": "重点复盘有没有把三框架协同偷换成“任意一层看多就上”。",
    },
    "SK-055": {
        "theme": "UST 脱锚前夜的稳定币信心断裂切片",
        "source": "优先读 `resources/cases/2022-05_ust_luna_depeg_dossier.md`，再补 `resources/02_risk/stablecoin_liquidity_risk_guide.md` 的 LUNA / UST 结构与 `resources/02_risk/ethereum_defi_risk_structure_guide.md` 的机制/外部依赖层。",
        "known": "UST 锚定开始波动，套利与赎回压力升高，相关池子失衡，LUNA 承接压力同步变大。",
        "unknown": "系统还能否靠机制自愈，还是已经进入正反馈死亡螺旋。",
        "question": "如果稳定币开始轻微脱锚，你会先看哪几个环节来判断这是暂时波动还是结构性失败？",
        "reveal": "先要求学习者画出“脱锚→赎回/铸销→LUNA 抛压→信心进一步坍塌”的链条，再揭示崩盘如何加速。",
        "retro": "重点复盘有没有把价格暂时稳定误当成机制稳健。",
    },
    "SK-056": {
        "theme": "高 OI + 极端资金费率 + 薄盘口下的闪崩切片",
        "source": "优先读 `resources/cases/2025-10_crypto_flash_crash_dossier.md`，再补 `resources/04_trading/derivatives_and_funding_rate_guide.md` 的清算螺旋、`resources/04_trading/exchange_microstructure_guide.md` 的流动性抽离与 `resources/03_onchain/glassnode_onchain_metrics_guide.md` 的持仓盈利背景。",
        "known": "OI 处在高位，资金费率极端，链上显示大部分筹码处于盈利状态，外部宏观冲击开始出现。",
        "unknown": "冲击会不会只是短暂波动，还是会触发连锁去杠杆并放大成闪崩。",
        "question": "只看当时信息，你会先担心方向错，还是担心杠杆结构和盘口深度先崩？为什么？",
        "reveal": "先要求学习者说明哪一层最脆弱，再揭示强平单如何吃穿盘口并放大价格下跌。",
        "retro": "重点复盘有没有把闪崩仅仅解释成“消息面太差”，却忽略了杠杆和流动性的放大作用。",
    },
    "SK-053": {
        "theme": "2020-03-12 流动性危机与恐慌底部切片",
        "source": "优先读 `resources/cases/2020-03-12_btc_liquidity_crash_dossier.md`，再补 `resources/03_onchain/glassnode_onchain_metrics_guide.md` 的恐慌底部指标视角。",
        "known": "全球风险资产同步去杠杆，BTC 单日暴跌，市场流动性抽离，链上和衍生品结构都处在压力中。",
        "unknown": "这是结构性崩坏还是流动性冲击后的极端错杀；何时能重新定义风险收益。",
        "question": "如果你身处 2020-03-12 当天，第一优先会区分什么：基本面坏掉了，还是流动性危机先压垮了价格？",
        "reveal": "先要求学习者分层拆出宏观流动性、链上盈利结构和执行条件，再揭示后续恢复路径。",
        "retro": "重点复盘有没有把极端流动性冲击直接等同于长期基本面失效。",
    },
    "SK-054": {
        "theme": "2021-11-08 周期顶部与离场信号切片",
        "source": "优先读 `resources/cases/2021-11-08_btc_cycle_top_dossier.md`，再补 `resources/03_onchain/glassnode_onchain_metrics_guide.md` 的顶部指标与技术结构对照。",
        "known": "BTC 位于历史高位附近，MVRV-Z / NUPL 等指标高企，LTH 开始分发，情绪仍偏乐观。",
        "unknown": "这只是强趋势中的正常过热，还是接近顶部的离场窗口；结构信号能否先于价格确认风险。",
        "question": "只看当时信息，哪些信号已经足够让你把“继续追涨”降级为“考虑分批离场”？",
        "reveal": "先锁定学习者对顶部信号和离场节奏的判断，再揭示后续顶部确认与回撤路径。",
        "retro": "重点复盘有没有因为价格还在涨，就压制了对分发和过热结构的判断。",
    },
}
CASE_DOSSIER_REFERENCES = {
    "SK-004": "`resources/cases/2020-2022_monetary_expansion_inflation_dossier.md`",
    "SK-019": "`resources/cases/decision_quality_vs_result_quality_dossier.md`",
    "SK-043": "`resources/cases/spot_perpetual_delivery_execution_dossier.md`",
    "SK-052": "`resources/cases/2023-10_btc_three_framework_decision_dossier.md`",
    "SK-027": "`resources/cases/2022-11_ftx_bank_run_dossier.md`",
    "SK-028": "`resources/cases/mango_markets_oracle_manipulation_dossier.md`",
    "SK-053": "`resources/cases/2020-03-12_btc_liquidity_crash_dossier.md`",
    "SK-054": "`resources/cases/2021-11-08_btc_cycle_top_dossier.md`",
    "SK-055": "`resources/cases/2022-05_ust_luna_depeg_dossier.md`",
    "SK-056": "`resources/cases/2025-10_crypto_flash_crash_dossier.md`",
}
QUESTION_BANK_REFERENCES = {
    "SK-004": "`resources/question_banks/SK-004_inflation_mechanism_bank.md`",
    "SK-019": "`resources/question_banks/SK-019_probability_vs_result_bank.md`",
    "SK-020": "`resources/question_banks/SK-020_cognitive_bias_bank.md`",
    "SK-021": "`resources/question_banks/SK-021_expectancy_bank.md`",
    "SK-022": "`resources/question_banks/SK-022_023_position_risk_bank.md`",
    "SK-023": "`resources/question_banks/SK-022_023_position_risk_bank.md`",
    "SK-024": "`resources/question_banks/SK-024_025_exit_rules_bank.md`",
    "SK-025": "`resources/question_banks/SK-024_025_exit_rules_bank.md`",
    "SK-026": "`resources/question_banks/SK-026_liquidation_mechanism_bank.md`",
    "SK-027": "`resources/question_banks/SK-027_custody_risk_bank.md`",
    "SK-028": "`resources/question_banks/SK-028_defi_protocol_risk_bank.md`",
    "SK-029": "`resources/question_banks/SK-029_030_opsec_journal_bank.md`",
    "SK-030": "`resources/question_banks/SK-029_030_opsec_journal_bank.md`",
    "SK-043": "`resources/question_banks/SK-043_instrument_choice_bank.md`",
    "SK-044": "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "SK-045": "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "SK-046": "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "SK-047": "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "SK-048": "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "SK-049": "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "SK-050": "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "SK-051": "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "SK-052": "`resources/question_banks/SK-052_three_framework_synthesis_bank.md`",
    "SK-053": "`resources/question_banks/SK-053_056_case_synthesis_bank.md`",
    "SK-054": "`resources/question_banks/SK-053_056_case_synthesis_bank.md`",
    "SK-055": "`resources/question_banks/SK-053_056_case_synthesis_bank.md`",
    "SK-056": "`resources/question_banks/SK-053_056_case_synthesis_bank.md`",
}
CASE_RETRO_FOCUS = {
    "概念边界辨析": "复盘时强制回答“为什么不是另一个相邻概念”。",
    "场景应用迁移": "复盘时拆开“场景表象”和“底层原则”，确认有没有被表面现象带走。",
    "边界条件与反例构造": "复盘时补一个让当前判断失效的反例或边界条件。",
    "框架纪律与中间判断": "复盘时显式补齐中间判断步骤，不接受跳结论。",
    "基础记忆提取": "复盘时先做最小要点清单，再回到场景判断。",
}
MACRO_FOUNDATION_RESOURCES = (
    "`resources/cases/ww2_pow_cigarette_money_dossier.md`",
    "`resources/cases/1933_gold_confiscation_dossier.md`",
    "`resources/cases/1871_rai_stones_dossier.md`",
    "`resources/cases/1971-08_nixon_shock_dossier.md`",
    "《The Bitcoin Standard》",
    "《Broken Money》",
    "`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`",
)
MONETARY_EXPANSION_RESOURCES = (
    "《Broken Money》",
    "`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`",
    "ARK Invest Bitcoin research report（local-only source material）",
)
BITCOIN_MECHANICS_RESOURCES = (
    "`resources/01_macro/bitcoin_whitepaper_guide.md`",
    "Emerging Tech Bitcoin/Crypto research report（local-only source material）",
    "《The Bitcoin Standard》",
)
MACRO_CYCLE_RESOURCES = (
    "《Broken Money》",
    "ARK Invest Bitcoin research report（local-only source material）",
    "`resources/01_macro/lyn_alden_3_reasons_bitcoin.md`",
)
INFLATION_MECHANISM_RESOURCES = (
    "`resources/cases/2020-2022_monetary_expansion_inflation_dossier.md`",
    "`resources/question_banks/SK-004_inflation_mechanism_bank.md`",
    "《Broken Money》（见“法币稀释与购买力传导”相关章节）",
    "ARK Invest Bitcoin research report（local-only source material；见“流动性先推升资产、再传导到消费”相关段落）",
)
RISK_DECISION_RESOURCES = (
    "`resources/question_banks/SK-020_cognitive_bias_bank.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“SK-020：交易中的主要认知偏差”）",
    "《Trading in the Zone》（见“概率思维、情绪与偏差”相关章节）",
    "Binance Academy: A Beginner's Guide to Risk Management（local-only source material；见风险纪律与行为偏差部分）",
)
EXPECTANCY_RESOURCES = (
    "`resources/question_banks/SK-021_expectancy_bank.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“SK-021：期望值”）",
    "《Trading in the Zone》（见期望值、样本量与结果噪音相关章节）",
    "Binance Academy: A Beginner's Guide to Risk Management（local-only source material；见风险回报与长期生存部分）",
)
PROBABILITY_DECISION_RESOURCES = (
    "`resources/cases/decision_quality_vs_result_quality_dossier.md`",
    "`resources/question_banks/SK-019_probability_vs_result_bank.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“SK-019：概率思维 vs 结果导向”）",
    "《Trading in the Zone》（见“决策质量独立于结果质量”相关章节）",
)
POSITION_SIZING_RESOURCES = (
    "`resources/question_banks/SK-022_023_position_risk_bank.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“SK-021：期望值”“SK-022 / SK-023：风险金额与仓位”“SK-024 / SK-025：止损与止盈”）",
    "Binance Academy: Stop-Loss and Take-Profit Levels（local-only source material；见止损距离与风险收益比部分）",
    "Binance Academy: Five Risk Management Strategies（local-only source material；见单笔风险与账户保护部分）",
)
EXIT_RULE_RESOURCES = (
    "`resources/question_banks/SK-024_025_exit_rules_bank.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“SK-024 / SK-025：止损与止盈”）",
    "Binance Academy: Stop-Loss and Take-Profit Levels（local-only source material；见止损、止盈与风险收益比部分）",
    "Binance Academy: Five Risk Management Strategies（local-only source material；见退出纪律与风险控制部分）",
)
LIQUIDATION_RESOURCES = (
    "`resources/question_banks/SK-026_liquidation_mechanism_bank.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“SK-026：爆仓机制与生存边界”）",
    "`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“实战检查表”与爆仓机制相关段落）",
    "Binance Academy: Five Risk Management Strategies（local-only source material；见账户保护与连续亏损控制部分）",
)
CEX_RISK_RESOURCES = (
    "`resources/cases/2022-11_ftx_bank_run_dossier.md`",
    "`resources/question_banks/SK-027_custody_risk_bank.md`",
    "`resources/04_trading/exchange_microstructure_guide.md`（见“理解盘口的第一原则”和“CEX 余额不等于链上托管”相关段落）",
    "`resources/02_risk/stablecoin_liquidity_risk_guide.md`（见交易对手方与流动性断裂传导部分）",
)
DEFI_RISK_RESOURCES = (
    "`resources/cases/mango_markets_oracle_manipulation_dossier.md`",
    "`resources/question_banks/SK-028_defi_protocol_risk_bank.md`",
    "`resources/02_risk/ethereum_defi_risk_structure_guide.md`（见预言机、授权、桥与协议分层风险部分）",
    "`resources/02_risk/stablecoin_liquidity_risk_guide.md`（见机制失效如何向市场扩散部分）",
)
OPSEC_RESOURCES = (
    "`resources/question_banks/SK-029_030_opsec_journal_bank.md`",
    "`resources/02_risk/ethereum_defi_risk_structure_guide.md`（见授权、前端钓鱼、桥与钱包暴露面部分）",
    "`resources/02_risk/stablecoin_liquidity_risk_guide.md`（见交易对手方与链上转移风险部分）",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“复盘时必须问的四个问题”）",
)
TRADING_JOURNAL_RESOURCES = (
    "`resources/question_banks/SK-029_030_opsec_journal_bank.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“SK-030：交易日志”与“复盘时必须问的四个问题”）",
    "Binance Academy: What Is a Trading Journal and How to Use One（local-only source material；见日志字段与复盘用途部分）",
    "《Trading in the Zone》（见复盘纪律与情绪记录相关章节）",
)
ONCHAIN_CYCLE_RESOURCES = (
    "`resources/question_banks/SK-031_042_onchain_metrics_bank.md`",
    "`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“1. Realized Cap”“2. MVRV Ratio”“3. SOPR”“4. NUPL”）",
    "《Cryptoassets》（见链上估值与市场周期相关章节）",
    "ARK Invest Bitcoin research report（local-only source material；见周期与机构流动性框架部分）",
)
DERIVATIVES_RESOURCES = (
    "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“SK-044：资金费率”）",
    "`resources/04_trading/exchange_microstructure_guide.md`（见“SK-045：流动性与滑点”）",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“SK-026：爆仓机制与生存边界”）",
)
FUNDING_RATE_RESOURCES = (
    "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“SK-044：资金费率”）",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”中的 Trigger / Execution）",
    "`resources/04_trading/exchange_microstructure_guide.md`（见“理解盘口的第一原则”）",
)
LIQUIDITY_SLIPPAGE_RESOURCES = (
    "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "`resources/04_trading/exchange_microstructure_guide.md`（见“SK-045：流动性与滑点”）",
    "`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“实战检查表”）",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“最小下单模板”与 Execution）",
)
INSTRUMENT_CHOICE_RESOURCES = (
    "`resources/cases/spot_perpetual_delivery_execution_dossier.md`",
    "`resources/question_banks/SK-043_instrument_choice_bank.md`",
    "`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“SK-043：现货、永续、交割”）",
    "`resources/04_trading/exchange_microstructure_guide.md`（见“SK-043：现货、永续合约、交割合约”）",
)
TA_EXECUTION_RESOURCES = (
    "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”“最小下单模板”）",
    "《The Art and Science of Technical Analysis》（见结构、量价与形态相关章节）",
    "《The Crypto Trader》（见执行计划与案例复盘相关章节）",
)
SYNTHESIS_RESOURCES = (
    "`resources/question_banks/SK-044_051_execution_toolkit_bank.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”）",
    "`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“2. MVRV Ratio”“3. SOPR”“4. NUPL”）",
    "《The Art and Science of Technical Analysis》（见趋势确认与结构失效相关章节）",
)
THREE_FRAMEWORK_SYNTHESIS_RESOURCES = (
    "`resources/cases/2023-10_btc_three_framework_decision_dossier.md`",
    "`resources/question_banks/SK-052_three_framework_synthesis_bank.md`",
    "`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“2. MVRV Ratio”“3. SOPR”“4. NUPL”）",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“一笔交易的五段式结构”）",
)
MARCH_2020_CASE_RESOURCES = (
    "`resources/cases/2020-03-12_btc_liquidity_crash_dossier.md`",
    "`resources/question_banks/SK-053_056_case_synthesis_bank.md`",
    "`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“2. MVRV Ratio”“3. SOPR”）",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“复盘时必须问的四个问题”）",
)
NOV_2021_CASE_RESOURCES = (
    "`resources/cases/2021-11-08_btc_cycle_top_dossier.md`",
    "`resources/question_banks/SK-053_056_case_synthesis_bank.md`",
    "`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“2. MVRV Ratio”“4. NUPL”）",
    "《The Art and Science of Technical Analysis》（见顶部结构与离场确认相关章节）",
)
LUNA_CASE_RESOURCES = (
    "`resources/cases/2022-05_ust_luna_depeg_dossier.md`",
    "`resources/question_banks/SK-053_056_case_synthesis_bank.md`",
    "`resources/02_risk/stablecoin_liquidity_risk_guide.md`（见脱锚、赎回与信心断裂传导部分）",
    "`resources/02_risk/ethereum_defi_risk_structure_guide.md`（见机制风险与协议暴露面部分）",
)
FLASH_CRASH_RESOURCES = (
    "`resources/cases/2025-10_crypto_flash_crash_dossier.md`",
    "`resources/question_banks/SK-053_056_case_synthesis_bank.md`",
    "`resources/04_trading/derivatives_and_funding_rate_guide.md`（见“SK-056：闪崩案例”）",
    "`resources/03_onchain/glassnode_onchain_metrics_guide.md`（见“2. MVRV Ratio”“4. NUPL”）",
    "`resources/04_trading/exchange_microstructure_guide.md`（见“SK-056：2025年10月加密市场闪崩”）",
)
GRADUATION_RESOURCES = (
    "`resources/04_trading/SK-057_personal_strategy_template.md`",
    "`resources/04_trading/execution_decision_framework_guide.md`（见“SK-057：毕业策略文档评分表”“SK-057：可填写模板”）",
    "Binance Academy: What Is a Trading Journal and How to Use One（local-only source material；见日志字段与复盘样例部分）",
    "《The Crypto Trader》（见完整策略样例与交易复盘相关章节）",
)
CONCEPT_SLICE_FIELDS = (
    "案例 dossier",
    "案例切片",
    "盛言开场案例",
    "当时已知信息",
    "当时未知信息",
    "学习者当下判断",
    "结果揭示",
    "偏差复盘",
    "复述检验",
)
CONCEPT_RESOURCE_TRACE_FIELDS = (
    "资源段落",
    "证据包条目",
    "图示编号",
)
ALL_CONCEPT_TRACE_FIELDS = CONCEPT_SLICE_FIELDS + CONCEPT_RESOURCE_TRACE_FIELDS


@dataclass(frozen=True)
class Skill:
    skill_id: str
    name: str
    description: str
    prereq_text: str
    prereqs: tuple[str, ...]
    mastery_standard: str
    status: str
    concept_completed: str
    first_mastery_date: date | None
    latest_mastery_date: date | None
    delayed_validation_due: date | None
    delayed_validation_passed_date: date | None
    last_practice: date | None
    history_accuracies: tuple[str, ...]
    review_due: date | None
    review_round: int

    @property
    def number(self) -> int:
        return int(self.skill_id.split("-")[1])

    @property
    def status_icon(self) -> str:
        return self.status[:1]

    @property
    def is_mastered(self) -> bool:
        return self.status.startswith(MASTERED_PREFIXES) and self.is_delayed_validated

    @property
    def is_active(self) -> bool:
        return self.status.startswith(ACTIVE_PREFIXES)

    @property
    def is_delayed_validated(self) -> bool:
        return (
            self.delayed_validation_passed_date is not None
            or self.review_due is not None
            or self.review_round > 0
            or self.status.startswith(("🔄", "💚"))
        )

    @property
    def needs_delayed_validation(self) -> bool:
        return (
            self.status.startswith("✅")
            and self.latest_mastery_date is not None
            and not self.is_delayed_validated
        )

    @property
    def review_anchor_date(self) -> date | None:
        return self.delayed_validation_passed_date or self.latest_mastery_date

    @property
    def rendered_status(self) -> str:
        if self.needs_delayed_validation:
            return "✅ 待延迟验证"
        if self.status.startswith("✅"):
            return "✅ 已掌握"
        return self.status


@dataclass(frozen=True)
class HomeworkEntry:
    header_index: int
    entry_date: date | None
    session_title: str
    skill_id: str | None
    skill_name: str | None
    body: str
    accuracy: str
    judgment: str
    weak_points: str


@dataclass(frozen=True)
class ShawQuestionRecord:
    number: str
    question_bank_id: str
    summary: str
    question_type: str
    source_skill: str
    result: str


@dataclass(frozen=True)
class HomeworkSection:
    original_index: int
    header: str
    body: str


@dataclass(frozen=True)
class ArchiveSection:
    original_index: int
    header: str
    body: str


@dataclass(frozen=True)
class ArchiveEntry:
    header_index: int
    header: str
    entry_date: date | None
    skill_id: str | None
    fields: dict[str, str]


@dataclass(frozen=True)
class ConceptEvent:
    event_date: date
    label: str | None
    source: str


@dataclass(frozen=True)
class MasteryRecord:
    skill_id: str
    skill_name: str
    first_mastery_date: date
    mastery_method: str
    final_accuracy: str
    attempt_count: int
    primary_failure_types: str
    delayed_validation: str


@dataclass(frozen=True)
class MasterySnapshot:
    first_mastery_date: date | None
    latest_mastery_date: date | None


@dataclass(frozen=True)
class DelayedValidationSnapshot:
    passed_date: date | None


@dataclass(frozen=True)
class SchedulingPolicy:
    code: str
    headline: str
    detail: str


@dataclass(frozen=True)
class TeachingActionTrigger:
    skill_id: str
    skill_name: str
    error_mode: str
    streak: int
    bucket: str
    next_session: str
    detail: str


@dataclass(frozen=True)
class ReviewPriority:
    status_rank: int
    overdue_days: int
    error_mode_count: int
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync and validate the markdown-backed learning state."
    )
    parser.add_argument(
        "command",
        choices=("sync", "check", "promote-archive-drafts"),
        help="sync writes generated sections; check validates without writing; promote-archive-drafts promotes current draft archive entries before syncing",
    )
    parser.add_argument(
        "--today",
        help="Override the effective date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Print unified diffs for any files that would change.",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Before writing changed files, snapshot their current contents under teacher/.state_backups/.",
    )
    return parser.parse_args()


def parse_iso_date(value: str) -> date | None:
    match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", value)
    if not match:
        return None
    return date.fromisoformat(match.group(0))


def parse_all_iso_dates(value: str) -> tuple[date, ...]:
    return tuple(date.fromisoformat(match) for match in re.findall(r"\b\d{4}-\d{2}-\d{2}\b", value))


def format_date(value: date | None) -> str:
    return value.isoformat() if value else "—"


def parse_history(value: str) -> tuple[str, ...]:
    stripped = value.strip()
    if stripped == "[]":
        return ()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        return ()
    body = stripped[1:-1].strip()
    if not body:
        return ()
    return tuple(item.strip() for item in body.split(",") if item.strip())


def short_accuracy(value: str) -> str:
    match = re.search(r"\b\d+/\d+\b", value)
    return match.group(0) if match else value.strip()


def accuracy_fraction(value: str) -> float | None:
    short = short_accuracy(value)
    match = re.fullmatch(r"(\d+)/(\d+)", short)
    if not match:
        return None
    numerator = int(match.group(1))
    denominator = int(match.group(2))
    if denominator == 0:
        return None
    return numerator / denominator


def parse_skill_graph(text: str) -> list[Skill]:
    heading_matches = list(re.finditer(r"^### (SK-\d{3})：(.+)$", text, re.MULTILINE))
    if not heading_matches:
        raise ValueError("No skill headings found in skill_graph.md")

    review_queue_index = text.index("## 今日复习队列")
    skills: list[Skill] = []

    for index, match in enumerate(heading_matches):
        body_start = match.end()
        body_end = (
            heading_matches[index + 1].start()
            if index + 1 < len(heading_matches)
            else review_queue_index
        )
        block = text[body_start:body_end]
        fields = {
            field_match.group(1): field_match.group(2).strip()
            for field_match in re.finditer(
                r"^- \*\*(.+?)\*\*：(.*)$", block, re.MULTILINE
            )
        }

        prereq_text = fields["前置技能"]
        prereqs = tuple(re.findall(r"SK-\d{3}", prereq_text))
        legacy_mastery_value = fields.get("掌握日期", "—")
        first_mastery_value = fields.get("首次掌握日期", legacy_mastery_value)
        latest_mastery_value = fields.get("最近达标日期", legacy_mastery_value)
        delayed_validation_due = fields.get("延迟验证到期", "—")
        delayed_validation_passed_value = fields.get("延迟验证通过日期", "—")
        skills.append(
            Skill(
                skill_id=match.group(1),
                name=match.group(2).strip(),
                description=fields["描述"],
                prereq_text=prereq_text,
                prereqs=prereqs,
                mastery_standard=fields["掌握标准"],
                status=fields["状态"],
                concept_completed=fields["概念课完成"],
                first_mastery_date=parse_iso_date(first_mastery_value),
                latest_mastery_date=parse_iso_date(latest_mastery_value),
                delayed_validation_due=parse_iso_date(delayed_validation_due),
                delayed_validation_passed_date=parse_iso_date(delayed_validation_passed_value),
                last_practice=parse_iso_date(fields["最后练习"]),
                history_accuracies=parse_history(fields["历史准确率"]),
                review_due=parse_iso_date(fields["复习到期"]),
                review_round=int(fields["复习轮次"]),
            )
        )

    return skills


def parse_homework_log(text: str) -> list[HomeworkEntry]:
    header_matches = list(re.finditer(r"^### (.+)$", text, re.MULTILINE))
    entries: list[HomeworkEntry] = []
    for index, match in enumerate(header_matches):
        body_start = match.end()
        body_end = header_matches[index + 1].start() if index + 1 < len(header_matches) else len(text)
        header = match.group(1).strip()
        body = text[body_start:body_end]

        date_match = re.match(r"(\d{4}-\d{2}-\d{2})\s+(.*)", header)
        entry_date = date.fromisoformat(date_match.group(1)) if date_match else None
        session_title = date_match.group(2).strip() if date_match else header

        skill_match = re.search(r"(SK-\d{3})《(.+?)》", header)
        skill_id = skill_match.group(1) if skill_match else None
        skill_name = skill_match.group(2) if skill_match else None

        accuracy_match = re.search(r"^\*\*本次准确率\*\*：(.*)$", body, re.MULTILINE)
        accuracy = accuracy_match.group(1).strip() if accuracy_match else "—"

        judgment_match = re.search(r"^\*\*掌握判定\*\*：(.*)$", body, re.MULTILINE)
        if judgment_match:
            judgment = judgment_match.group(1).strip()
        elif "概念" in session_title:
            judgment = "概念课完成"
        else:
            judgment = "—"

        weak_points_match = re.search(r"^\*\*薄弱题型(?:（如有）)?\*\*：(.*)$", body, re.MULTILINE)
        weak_points = weak_points_match.group(1).strip() if weak_points_match else "—"

        entries.append(
            HomeworkEntry(
                header_index=index,
                entry_date=entry_date,
                session_title=session_title,
                skill_id=skill_id,
                skill_name=skill_name,
                body=body.strip(),
                accuracy=accuracy,
                judgment=judgment,
                weak_points=weak_points,
            )
        )
    return entries


def split_homework_sections(text: str) -> tuple[str, list[HomeworkSection]]:
    matches = list(re.finditer(r"^### (\d{4}-\d{2}-\d{2} .+)$", text, re.MULTILINE))
    if not matches:
        return text, []

    prefix = text[: matches[0].start()]
    sections: list[HomeworkSection] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        header, _, body = block.partition("\n")
        cleaned_body = re.sub(r"(?:\n\s*---\s*)+$", "", body.strip())
        sections.append(
            HomeworkSection(
                original_index=index,
                header=header.strip(),
                body=cleaned_body,
            )
        )
    return prefix.rstrip() + "\n\n", sections


def split_session_archive_sections(text: str) -> tuple[str, list[ArchiveSection]]:
    matches = list(re.finditer(r"^### (\d{4}-\d{2}-\d{2} .+)$", text, re.MULTILINE))
    if not matches:
        return text, []

    prefix = text[: matches[0].start()]
    sections: list[ArchiveSection] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        header, _, body = block.partition("\n")
        cleaned_body = re.sub(r"(?:\n\s*---\s*)+$", "", body.strip())
        sections.append(
            ArchiveSection(
                original_index=index,
                header=header.strip(),
                body=cleaned_body,
            )
        )
    return prefix.rstrip() + "\n\n", sections


def render_archive_sections(prefix: str, sections: list[ArchiveSection]) -> str:
    normalized_prefix = prefix.rstrip() + "\n\n"
    if not sections:
        return normalized_prefix.rstrip() + "\n"

    rendered_sections = [
        f"{section.header}\n\n{section.body}".rstrip()
        for section in sections
    ]
    return normalized_prefix + "\n\n---\n\n".join(rendered_sections) + "\n"


def parse_archive_fields(body: str) -> dict[str, str]:
    return {
        match.group(1): match.group(2).strip()
        for match in re.finditer(r"^\*\*(.+?)\*\*：(.*)$", body, re.MULTILINE)
    }


def archive_section_key(section: ArchiveSection) -> tuple[date | None, str | None]:
    header_text = section.header.removeprefix("### ").strip()
    fields = parse_archive_fields(section.body)
    skill_match = re.search(r"(SK-\d{3})《", fields.get("技能点", ""))
    skill_id = skill_match.group(1) if skill_match else None
    return parse_iso_date(header_text), skill_id


def strip_auto_draft_marker(header_text: str) -> str:
    return re.sub(r"\s*（自动草稿）$", "", header_text).strip()


def parse_attempt_number(text: str) -> int:
    match = re.search(r"第(\d+)次", text)
    return int(match.group(1)) if match else 1


def homework_session_order(header: str) -> int:
    if "间隔复习" in header or "复习课" in header:
        round_number = parse_attempt_number(header)
        return round_number

    if "概念重修" in header or "概念课（重修" in header:
        retry_match = re.search(r"重修(\d+)", header)
        retry_number = int(retry_match.group(1)) if retry_match else 1
        return 20 * (retry_number * 2) + 10

    if "概念课" in header:
        return 10

    if "练习课" in header:
        attempt_number = parse_attempt_number(header)
        return 20 * attempt_number

    return 10_000


def normalize_homework_log(text: str) -> str:
    prefix, sections = split_homework_sections(text)
    if not sections:
        return text.rstrip() + "\n"

    group_first_seen: dict[tuple[date | None, str | None], int] = {}
    section_meta: list[tuple[HomeworkSection, date | None, str | None, int]] = []
    for section in sections:
        header_text = section.header.removeprefix("### ").strip()
        entry_date = parse_iso_date(header_text)
        skill_match = re.search(r"(SK-\d{3})《", header_text)
        skill_id = skill_match.group(1) if skill_match else None
        group_key = (entry_date, skill_id)
        group_first_seen.setdefault(group_key, section.original_index)
        section_meta.append(
            (section, entry_date, skill_id, homework_session_order(header_text))
        )

    normalized_sections = sorted(
        section_meta,
        key=lambda item: (
            item[1] or date.min,
            group_first_seen[(item[1], item[2])],
            item[3],
            item[0].original_index,
        ),
    )

    rendered_sections = [
        f"{section.header}\n\n{section.body}".rstrip()
        for section, _, _, _ in normalized_sections
    ]
    return prefix + "\n\n---\n\n".join(rendered_sections) + "\n"


def normalize_session_archive(text: str) -> str:
    prefix, sections = split_session_archive_sections(text)
    if not sections:
        return text.rstrip() + "\n"

    normalized_sections = sorted(
        sections,
        key=lambda section: (
            parse_iso_date(section.header) or date.min,
            section.original_index,
        ),
    )
    rendered_sections = [
        f"{section.header}\n\n{section.body}".rstrip()
        for section in normalized_sections
    ]
    return render_archive_sections(prefix, normalized_sections)


def parse_session_archive_entries(text: str) -> list[ArchiveEntry]:
    _, sections = split_session_archive_sections(text)
    entries: list[ArchiveEntry] = []
    for index, section in enumerate(sections):
        header_text = section.header.removeprefix("### ").strip()
        fields = parse_archive_fields(section.body)
        skill_match = re.search(r"(SK-\d{3})《", fields.get("技能点", ""))
        entries.append(
            ArchiveEntry(
                header_index=index,
                header=header_text,
                entry_date=parse_iso_date(header_text),
                skill_id=skill_match.group(1) if skill_match else None,
                fields=fields,
            )
        )
    return entries


def concept_label_from_title(title: str) -> str | None:
    if "重修2" in title:
        return "重修2"
    if "重修" in title:
        return "重修"
    if "概念" in title:
        return None
    return None


def collect_concept_events(
    skills: list[Skill],
    homework_entries: list[HomeworkEntry],
    archive_entries: list[ArchiveEntry],
) -> dict[str, list[ConceptEvent]]:
    events_by_skill: dict[str, dict[date, ConceptEvent]] = {skill.skill_id: {} for skill in skills}

    for skill in skills:
        for index, event_date in enumerate(parse_all_iso_dates(skill.concept_completed)):
            events_by_skill[skill.skill_id].setdefault(
                event_date,
                ConceptEvent(
                    event_date=event_date,
                    label=None if index == 0 else ("重修" if index == 1 else f"重修{index}"),
                    source="skill_graph",
                ),
            )

    for entry in homework_entries:
        if not entry.skill_id or "概念" not in entry.session_title or not entry.entry_date:
            continue
        existing = events_by_skill[entry.skill_id].get(entry.entry_date)
        label = concept_label_from_title(entry.session_title)
        if not existing or (existing.label is None and label is not None):
            events_by_skill[entry.skill_id][entry.entry_date] = ConceptEvent(
                event_date=entry.entry_date,
                label=label,
                source="homework_log",
            )

    for entry in archive_entries:
        if not entry.skill_id or "概念" not in entry.header or not entry.entry_date:
            continue
        existing = events_by_skill[entry.skill_id].get(entry.entry_date)
        label = concept_label_from_title(entry.header)
        if not existing or (existing.label is None and label is not None):
            events_by_skill[entry.skill_id][entry.entry_date] = ConceptEvent(
                event_date=entry.entry_date,
                label=label,
                source="session_archive",
            )

    return {
        skill_id: sorted(events.values(), key=lambda event: event.event_date)
        for skill_id, events in events_by_skill.items()
    }


def render_concept_completed_value(skill: Skill, concept_events: list[ConceptEvent]) -> str:
    if not concept_events:
        return "—"

    base_date = concept_events[0].event_date
    extras: list[str] = []
    retry_counter = 1
    for event in concept_events[1:]:
        label = event.label
        if not label:
            label = "重修" if retry_counter == 1 else f"重修{retry_counter}"
        extras.append(f"{label} {event.event_date.isoformat()}")
        retry_counter += 1

    if not extras:
        return base_date.isoformat()
    return f"{base_date.isoformat()}（{'，'.join(extras)}）"


def sync_skill_graph_concept_fields(
    text: str,
    skills: list[Skill],
    concept_events_by_skill: dict[str, list[ConceptEvent]],
) -> str:
    synced = text
    for skill in skills:
        desired = render_concept_completed_value(
            skill,
            concept_events_by_skill.get(skill.skill_id, []),
        )
        pattern = re.compile(
            rf"(### {re.escape(skill.skill_id)}：.*?\n- \*\*概念课完成\*\*：)(.*?)(?=\n- \*\*)",
            re.DOTALL,
        )
        synced, count = pattern.subn(
            lambda match: f"{match.group(1)}{desired}",
            synced,
            count=1,
        )
        if count != 1:
            raise ValueError(f"Unable to sync 概念课完成 for {skill.skill_id}")
    return synced


def normalize_session_label(entries: list[HomeworkEntry]) -> str:
    labels: list[str] = []
    for entry in entries:
        if "间隔复习" in entry.session_title:
            label = "复习课"
        elif "概念" in entry.session_title:
            label = "概念重修" if "重修" in entry.session_title else "概念课"
        else:
            label = "练习课"
        if not labels or labels[-1] != label:
            labels.append(label)
    return " + ".join(labels)


def extract_named_value(body: str, label: str) -> str | None:
    match = re.search(rf"^\*\*{re.escape(label)}\*\*：(.*)$", body, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    return value or None


def parse_shaw_question_records(body: str) -> list[ShawQuestionRecord]:
    records: list[ShawQuestionRecord] = []
    in_table = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped == "**Shaw 出题清单：**":
            in_table = True
            continue
        if not in_table:
            continue
        if not stripped:
            if records:
                break
            continue
        if not stripped.startswith("|"):
            if records:
                break
            continue
        parts = [part.strip() for part in stripped.strip("|").split("|")]
        if len(parts) not in {5, 6}:
            continue
        if parts[0] == "编号":
            continue
        if all(part and set(part) <= {"-"} for part in parts):
            continue
        if len(parts) == 6:
            records.append(
                ShawQuestionRecord(
                    number=parts[0],
                    question_bank_id=parts[1],
                    summary=parts[2],
                    question_type=parts[3],
                    source_skill=parts[4],
                    result=parts[5],
                )
            )
        else:
            records.append(
                ShawQuestionRecord(
                    number=parts[0],
                    question_bank_id="—",
                    summary=parts[1],
                    question_type=parts[2],
                    source_skill=parts[3],
                    result=parts[4],
                )
            )
    return records


def parse_shaw_question_rows(body: str) -> list[tuple[str, str]]:
    return [
        (record.question_type, record.result)
        for record in parse_shaw_question_records(body)
    ]


def extract_concept_slice(entry: HomeworkEntry) -> dict[str, str]:
    return {
        label: value
        for label in ALL_CONCEPT_TRACE_FIELDS
        if (value := extract_named_value(entry.body, label))
    }


def extract_concept_core(entries: list[HomeworkEntry]) -> str | None:
    for entry in entries:
        if "概念" not in entry.session_title:
            continue
        concept_slice = extract_concept_slice(entry)
        recall = concept_slice.get("复述检验")
        if recall and recall not in {"通过", "未通过"}:
            return recall
        initial_judgment = concept_slice.get("学习者当下判断")
        if initial_judgment:
            return initial_judgment

    preferred_labels = (
        "学习者从案例中自行推导出全部六条属性",
        "学习者从案例中自行推导出全部六个属性",
        "关键辨析突破",
        "框架边界",
        "Root 延伸",
        "核心教学方法",
    )
    for entry in entries:
        if "概念" not in entry.session_title:
            continue
        for label in preferred_labels:
            value = extract_named_value(entry.body, label)
            if value:
                return value
    return None


def summarize_status_change(entries: list[HomeworkEntry]) -> str:
    parts: list[str] = []
    for entry in entries:
        if "概念" in entry.session_title:
            label = "概念重修完成" if "重修" in entry.session_title else "概念课完成"
        elif "间隔复习" in entry.session_title:
            label = f"{short_accuracy(entry.accuracy)} {entry.judgment}"
        else:
            label = f"{short_accuracy(entry.accuracy)} {entry.judgment}"
        parts.append(label)
    return " → ".join(parts)


def summarize_session_core(entries: list[HomeworkEntry]) -> str:
    concept_core = extract_concept_core(entries)
    if concept_core:
        return concept_core

    practice_entries = [entry for entry in entries if entry.accuracy != "—"]
    if not practice_entries:
        return "待补充"

    latest = practice_entries[-1]
    attempts = len(practice_entries)
    highest = max(practice_entries, key=lambda entry: int(short_accuracy(entry.accuracy).split("/")[0]))
    return (
        f"本日共 {attempts} 次练习/复习，最新结果 {latest.accuracy}；"
        f"最高结果 {highest.accuracy}。"
    )


def summarize_shengyan_comment(entries: list[HomeworkEntry]) -> str:
    for entry in entries:
        if "概念" not in entry.session_title:
            continue
        for label in ("盛言收尾评注", "盛言的评注"):
            value = extract_named_value(entry.body, label)
            if value:
                return value
    return "待补充"


def summarize_follow_up(entries: list[HomeworkEntry]) -> str:
    for entry in reversed(entries):
        if entry.weak_points not in {"—", "无"}:
            return entry.weak_points
        if "概念" in entry.session_title:
            concept_slice = extract_concept_slice(entry)
            review_note = concept_slice.get("偏差复盘")
            if review_note:
                return review_note
    return "待补充"


def summarize_concept_trace(entries: list[HomeworkEntry]) -> tuple[str | None, str | None]:
    for entry in reversed(entries):
        if "概念" not in entry.session_title:
            continue
        concept_slice = extract_concept_slice(entry)
        dossier = concept_slice.get("案例 dossier")
        slice_name = concept_slice.get("案例切片")
        if dossier or slice_name:
            return dossier, slice_name
    return None, None


def summarize_concept_resource_trace(entries: list[HomeworkEntry]) -> dict[str, str]:
    for entry in reversed(entries):
        if "概念" not in entry.session_title:
            continue
        concept_slice = extract_concept_slice(entry)
        trace = {
            field: concept_slice[field]
            for field in CONCEPT_RESOURCE_TRACE_FIELDS
            if concept_slice.get(field)
        }
        if trace:
            return trace
    return {}


def render_session_archive_drafts(
    homework_entries: list[HomeworkEntry],
    archive_entries: list[ArchiveEntry],
) -> str:
    archive_coverage = {
        (entry.entry_date, entry.skill_id)
        for entry in archive_entries
        if entry.entry_date and entry.skill_id
    }

    grouped_entries: dict[tuple[date, str], list[HomeworkEntry]] = {}
    for entry in homework_entries:
        if not entry.entry_date or not entry.skill_id or not entry.skill_name:
            continue
        grouped_entries.setdefault((entry.entry_date, entry.skill_id), []).append(entry)

    missing_groups = [
        (key, grouped_entries[key])
        for key in sorted(grouped_entries)
        if key not in archive_coverage
    ]

    lines = [
        "# 会话存档草稿（session_archive_drafts.md）",
        "",
        "> 本文件由 `python3 tools/learning_state.py sync` 自动生成。",
        "> 作用：为 `teacher/session_archive.md` 提供尚未正式归档的会话草稿。",
        "> 草稿只提取可安全结构化的信息；“本节核心”和“盛言的评注”仍建议人工复核后再正式入档。",
        "> 如确认草稿可直接入档，可运行 `python3 tools/learning_state.py promote-archive-drafts`。",
        "> “下次概念课建议追问 / 下次练习课建议题型”会复用 `learner_profile.md` 的弱点聚类逻辑自动生成。",
        "",
        "---",
        "",
    ]

    if not missing_groups:
        lines.extend(["*（空）*", ""])
        return "\n".join(lines)

    for (entry_date, skill_id), entries in missing_groups:
        skill_name = entries[0].skill_name or "待补充"
        cutoff_header_index = max(entry.header_index for entry in entries)
        historical_entries = [
            entry for entry in homework_entries if entry.header_index <= cutoff_header_index
        ]
        dossier, slice_name = summarize_concept_trace(entries)
        resource_trace = summarize_concept_resource_trace(entries)
        trace_lines: list[str] = []
        if dossier:
            trace_lines.append(f"**案例 dossier**：{dossier}")
        if slice_name:
            trace_lines.append(f"**案例切片**：{slice_name}")
        for field in CONCEPT_RESOURCE_TRACE_FIELDS:
            if field in resource_trace:
                trace_lines.append(f"**{field}**：{resource_trace[field]}")
        lines.extend(
            [
                f"### {entry_date.isoformat()} {normalize_session_label(entries)}（自动草稿）",
                "",
                f"**技能点**：{skill_id}《{skill_name}》",
                *trace_lines,
                f"**状态变化**：{summarize_status_change(entries)}",
                f"**本节核心**：{summarize_session_core(entries)}",
                f"**盛言的评注**：{summarize_shengyan_comment(entries)}",
                f"**遗留问题**：{summarize_follow_up(entries)}",
                f"**下次会话强制动作**：{summarize_mandatory_action_for_skill(historical_entries, skill_id)}",
                f"**下次概念课建议追问**：{summarize_next_concept_follow_up(entries, historical_entries, skill_id)}",
                f"**下次练习课建议题型**：{summarize_next_practice_bias(entries, historical_entries, skill_id)}",
                "",
                "---",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def latest_archive_entry_for_skill(
    archive_entries: list[ArchiveEntry],
    skill_id: str,
) -> ArchiveEntry | None:
    for entry in reversed(archive_entries):
        if entry.skill_id == skill_id:
            return entry
    return None


def promote_archive_drafts(
    session_archive_text: str,
    archive_drafts_text: str,
) -> tuple[str, list[str]]:
    normalized_archive = normalize_session_archive(session_archive_text)
    prefix, archive_sections = split_session_archive_sections(normalized_archive)
    _, draft_sections = split_session_archive_sections(archive_drafts_text)
    if not draft_sections:
        return normalized_archive, []

    covered_keys = {
        key
        for key in (archive_section_key(section) for section in archive_sections)
        if key[0] and key[1]
    }
    merged_sections = list(archive_sections)
    promoted_headers: list[str] = []

    for draft_section in draft_sections:
        key = archive_section_key(draft_section)
        if key[0] and key[1] and key in covered_keys:
            continue

        header_text = draft_section.header.removeprefix("### ").strip()
        promoted_header = strip_auto_draft_marker(header_text)
        merged_sections.append(
            ArchiveSection(
                original_index=len(merged_sections),
                header=f"### {promoted_header}",
                body=draft_section.body,
            )
        )
        if key[0] and key[1]:
            covered_keys.add(key)
        promoted_headers.append(promoted_header)

    return normalize_session_archive(render_archive_sections(prefix, merged_sections)), promoted_headers


def latest_homework_entry_for_skill(
    homework_entries: list[HomeworkEntry],
    skill_id: str,
) -> HomeworkEntry | None:
    for entry in reversed(homework_entries):
        if entry.skill_id == skill_id:
            return entry
    return None


def latest_review_entry_for_skill(
    homework_entries: list[HomeworkEntry],
    skill_id: str,
) -> HomeworkEntry | None:
    for entry in reversed(homework_entries):
        if entry.skill_id == skill_id and "间隔复习" in entry.session_title:
            return entry
    return None


def latest_non_review_scored_entry_for_skill(
    homework_entries: list[HomeworkEntry],
    skill_id: str,
) -> HomeworkEntry | None:
    for entry in reversed(homework_entries):
        if (
            entry.skill_id == skill_id
            and entry.accuracy != "—"
            and "间隔复习" not in entry.session_title
        ):
            return entry
    return None


def review_priority_snapshot(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
    today: date,
) -> ReviewPriority:
    overdue_days = max((today - skill.review_due).days, 0) if skill.review_due else 0
    latest_review_entry = latest_review_entry_for_skill(homework_entries, skill.skill_id)
    latest_non_review_scored_entry = latest_non_review_scored_entry_for_skill(
        homework_entries, skill.skill_id
    )
    latest_scored_entry = latest_homework_entry_for_skill(homework_entries, skill.skill_id)
    status_rank = 0
    reasons: list[str] = []
    error_mode_count = 0

    if latest_review_entry and (
        not latest_non_review_scored_entry
        or latest_review_entry.header_index > latest_non_review_scored_entry.header_index
    ):
        if "未通过" in latest_review_entry.judgment:
            status_rank = 2
            reasons.append("上次复习未通过")
        elif (
            "维持" in latest_review_entry.judgment
            or (accuracy_fraction(latest_review_entry.accuracy) or 1.0) < 0.8
        ):
            status_rank = 1
            reasons.append("上次复习仅维持")

    if latest_scored_entry and latest_scored_entry.accuracy != "—":
        error_mode_count = len(error_modes_for_entry(latest_scored_entry))
        if error_mode_count:
            reasons.append(f"最近错误模式 {error_mode_count} 类")

    if skill.review_due == today:
        reasons.append("今日到期")
    elif overdue_days > 0:
        reasons.append(f"已逾期 {overdue_days} 天")

    return ReviewPriority(
        status_rank=status_rank,
        overdue_days=overdue_days,
        error_mode_count=error_mode_count,
        reason="；".join(reasons) if reasons else "正常到期",
    )


def latest_follow_up_for_skill(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
    archive_entries: list[ArchiveEntry],
) -> str:
    archive_entry = latest_archive_entry_for_skill(archive_entries, skill.skill_id)
    if archive_entry:
        follow_up = archive_entry.fields.get("遗留问题")
        if follow_up and follow_up not in {"待补充", "—", "无"}:
            return follow_up

    for entry in reversed(homework_entries):
        if entry.skill_id == skill.skill_id and entry.weak_points not in {"—", "无"}:
            return entry.weak_points

    if skill.status.startswith("⬜"):
        return "新技能，暂无历史遗留问题。"
    return "待补充"


def concept_guidance_for_skill(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
    archive_entries: list[ArchiveEntry],
) -> str:
    archive_entry = latest_archive_entry_for_skill(archive_entries, skill.skill_id)
    if archive_entry:
        guidance = archive_entry.fields.get("下次概念课建议追问")
        if guidance and guidance not in {"待补充", "—", "无"}:
            return guidance
    skill_entries = [entry for entry in homework_entries if entry.skill_id == skill.skill_id]
    return summarize_next_concept_follow_up(skill_entries, homework_entries, skill.skill_id)


def practice_guidance_for_skill(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
    archive_entries: list[ArchiveEntry],
) -> str:
    archive_entry = latest_archive_entry_for_skill(archive_entries, skill.skill_id)
    if archive_entry:
        guidance = archive_entry.fields.get("下次练习课建议题型")
        if guidance and guidance not in {"待补充", "—", "无"}:
            return guidance
    skill_entries = [entry for entry in homework_entries if entry.skill_id == skill.skill_id]
    return summarize_next_practice_bias(skill_entries, homework_entries, skill.skill_id)


def mandatory_action_for_skill(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
    archive_entries: list[ArchiveEntry],
) -> str:
    current_action = summarize_mandatory_action_for_skill(homework_entries, skill.skill_id)
    if current_action != "无":
        return current_action

    archive_entry = latest_archive_entry_for_skill(archive_entries, skill.skill_id)
    if archive_entry:
        action = archive_entry.fields.get("下次会话强制动作")
        if action and action not in {"待补充", "—", "无"}:
            return action
    return "无"


def primary_trigger_for_skill(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
) -> TeachingActionTrigger | None:
    triggers = triggered_teaching_actions_for_skill(homework_entries, skill.skill_id)
    return triggers[0] if triggers else None


def practice_starter_types_for_skill(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
) -> list[str]:
    categories = dominant_teaching_categories(
        [entry for entry in homework_entries if entry.skill_id == skill.skill_id],
        homework_entries,
        skill.skill_id,
        limit=3,
    )
    starter_types: list[str] = []
    for category in categories:
        for question_type in CATEGORY_STARTER_TYPES.get(category, ()):
            if question_type not in starter_types:
                starter_types.append(question_type)
            if len(starter_types) == 3:
                return starter_types
    for fallback_type in ("案例判断", "辨析", "直接应用"):
        if fallback_type not in starter_types:
            starter_types.append(fallback_type)
        if len(starter_types) == 3:
            break
    return starter_types


def render_shaw_starter_template(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
) -> list[str]:
    trigger = primary_trigger_for_skill(skill, homework_entries)
    starter_types = practice_starter_types_for_skill(skill, homework_entries)

    if trigger and trigger.bucket == "concept_rebuild":
        return [
            "暂停练习。先安排概念重修，不进入 Shaw 出题。",
            f"概念重修后恢复练习时，前3题：{' → '.join(starter_types)}。",
        ]

    lines = [f"前3题：{' → '.join(starter_types)}。"]
    if trigger and trigger.bucket == "structured_practice":
        lines.append("执行约束：每题先写中间判断，再给结论，不接受跳步。")
    elif trigger and trigger.bucket == "variant_practice":
        lines.append("执行约束：前2题不出纯记忆题，必须覆盖场景变形或边界条件。")
    elif trigger and trigger.bucket == "targeted_drill":
        lines.append("执行约束：前2题先做短打矫正，再进入综合题。")
    else:
        lines.append("执行约束：优先覆盖建议题型，但不打破 70/20/10 比例。")
    return lines


def recommended_session_mode(
    skill: Skill,
    today: date,
    homework_entries: list[HomeworkEntry] | None = None,
) -> tuple[str, str]:
    if (
        skill.needs_delayed_validation
        and skill.delayed_validation_due
        and skill.delayed_validation_due <= today
    ):
        overdue_days = (today - skill.delayed_validation_due).days
        detail = f"延迟验证到期 {skill.delayed_validation_due.isoformat()}"
        if overdue_days > 0:
            detail += f"，已逾期 {overdue_days} 天"
        return ("延迟验证", detail)

    if skill.review_due and skill.is_mastered and skill.review_due <= today:
        overdue_days = (today - skill.review_due).days
        detail = f"第{skill.review_round + 1}次复习到期 {skill.review_due.isoformat()}"
        if overdue_days > 0:
            detail += f"，已逾期 {overdue_days} 天"
        if homework_entries:
            detail += f"；优先原因：{review_priority_snapshot(skill, homework_entries, today).reason}"
        return ("复习课", detail)

    if homework_entries and skill.status.startswith(("🔵", "🟡")):
        for trigger in triggered_teaching_actions_for_skill(homework_entries, skill.skill_id):
            if trigger.bucket == "concept_rebuild":
                return ("概念重修", render_teaching_action_trigger(trigger))

    if skill.status.startswith("🔵"):
        return ("练习课", "概念课已完成，等待首次练习。")
    if skill.status.startswith("🟡"):
        return ("练习课", "仍处学习中，优先继续练习；连续卡住再回概念重修。")
    if skill.status.startswith("⬜"):
        return ("概念课", "前置已满足，可进入新概念。")
    return ("观察", "当前不需要立即开新会话。")


def stage_number_for_skill(skill: Skill) -> int:
    for index, (stage_start, stage_end, _) in enumerate(STAGE_DEFINITIONS, start=1):
        if stage_start <= skill.number <= stage_end:
            return index
    raise ValueError(f"No stage number found for {skill.skill_id}.")


def case_library_tiers_for_skill(skill: Skill) -> dict[str, tuple[str, ...]]:
    tiers = CASE_LIBRARY_SKILL_OVERRIDES.get(skill.skill_id)
    if tiers:
        return tiers
    return CASE_LIBRARY_STAGE_DEFAULTS[stage_number_for_skill(skill)]


def case_dossier_reference_for_skill(skill: Skill) -> str:
    return CASE_DOSSIER_REFERENCES.get(skill.skill_id, "")


def question_bank_reference_for_skill(skill: Skill) -> str:
    if 31 <= skill.number <= 42:
        return "`resources/question_banks/SK-031_042_onchain_metrics_bank.md`"
    return QUESTION_BANK_REFERENCES.get(skill.skill_id, "")


def recommended_case_difficulty_for_skill(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
) -> tuple[str, str]:
    triggers = (
        triggered_teaching_actions_for_skill(homework_entries, skill.skill_id)
        if skill.status.startswith(("🔵", "🟡"))
        else []
    )
    if skill.status.startswith("⬜"):
        return ("入门切片", "首次进入该技能点，先用低背景负担事件暴露原始框架。")
    if any(trigger.bucket == "concept_rebuild" for trigger in triggers):
        return ("标准切片", "已触发概念回退，先用标准事件重建主干判断。")
    if any(trigger.bucket in {"variant_practice", "structured_practice"} for trigger in triggers):
        return ("高压反例切片", "当前更需要边界、反例或高压场景来检验原则。")
    return ("标准切片", "默认用标准事件做迁移判断，再按表现升级到高压反例。")


def case_template_for_skill(
    skill: Skill,
    homework_entries: list[HomeworkEntry],
) -> dict[str, str]:
    template = CASE_TEMPLATE_SKILL_OVERRIDES.get(skill.skill_id)
    if not template:
        stage_number = stage_number_for_skill(skill)
        template = CASE_TEMPLATE_STAGE_DEFAULTS[stage_number]

    top_categories = dominant_teaching_categories([], homework_entries, None, limit=2)
    retro_focus_items = [
        CASE_RETRO_FOCUS[category].rstrip("。；")
        for category in top_categories
        if category in CASE_RETRO_FOCUS
    ]
    retro = template["retro"].rstrip("。；")
    if retro_focus_items:
        retro = f"{retro}；{'；'.join(retro_focus_items)}"
    retro += "。"
    recommended_level, recommended_reason = recommended_case_difficulty_for_skill(
        skill,
        homework_entries,
    )
    tier_lines = {
        level: "；".join(case_library_tiers_for_skill(skill)[level])
        for level in CASE_DIFFICULTY_LEVELS
    }

    return {
        "theme": template["theme"],
        "source": template["source"],
        "dossier": case_dossier_reference_for_skill(skill),
        "recommended_level": recommended_level,
        "recommended_reason": recommended_reason,
        "entry_cases": tier_lines["入门切片"],
        "standard_cases": tier_lines["标准切片"],
        "stress_cases": tier_lines["高压反例切片"],
        "known": template["known"],
        "unknown": template["unknown"],
        "question": template["question"],
        "reveal": template["reveal"],
        "retro": retro,
    }


def render_session_briefing(
    skills: list[Skill],
    homework_entries: list[HomeworkEntry],
    archive_entries: list[ArchiveEntry],
    today: date,
) -> str:
    skills_by_id = {skill.skill_id: skill for skill in skills}
    delayed_due = delayed_validation_due_skills(skills, today)
    review_due = review_due_skills(skills, today, homework_entries)
    active_skills = [skill for skill in skills if skill.status.startswith(("🔵", "🟡"))]
    learnable_skills = currently_learnable_skills(skills, skills_by_id)
    available_new_skills = [skill for skill in learnable_skills if skill.status.startswith("⬜")]
    policy = scheduling_policy(skills, today)
    top_categories = dominant_teaching_categories([], homework_entries, None, limit=3)

    priority_skills: list[Skill] = []
    seen_skill_ids: set[str] = set()
    for bucket in (delayed_due, review_due, active_skills):
        for skill in bucket:
            if skill.skill_id in seen_skill_ids:
                continue
            seen_skill_ids.add(skill.skill_id)
            priority_skills.append(skill)

    lines = [
        "# 会话开场提示（session_briefing.md）",
        "",
        "> 本文件由 `python3 tools/learning_state.py sync` 自动生成。",
        "> 作用：把今日排程、学习者稳定弱点、技能级建议追问 / 题型偏置汇总成开场 briefing。",
        "> 每次新会话开场先读本文件，再进入概念课 / 练习课 / 延迟验证 / 复习课。",
        "",
        "---",
        "",
        "## 今日开场结论",
        "",
        f"- **当前系统日期**：{today.isoformat()}",
        f"- **今日调度策略**：{policy.headline}",
        f"- **执行说明**：{policy.detail}",
    ]

    if delayed_due:
        delayed_labels = "；".join(
            f"{skill.skill_id}（到期 {format_date(skill.delayed_validation_due)}）"
            for skill in delayed_due
        )
        lines.append(f"- **今日延迟验证**：{delayed_labels}")
    else:
        lines.append("- **今日延迟验证**：无")

    if review_due:
        review_labels = "；".join(
            f"{skill.skill_id}（第{skill.review_round + 1}次复习到期 {format_date(skill.review_due)}）"
            for skill in review_due
        )
        lines.append(f"- **今日复习**：{review_labels}")
    else:
        lines.append("- **今日复习**：无")

    if available_new_skills:
        learnable_labels = "、".join(
            f"{skill.skill_id}：{skill.name}" for skill in available_new_skills
        )
        lines.append(f"- **当前可学新技能**：{learnable_labels}")
    else:
        lines.append("- **当前可学新技能**：无")

    lines.extend(["", "## 双主线新课入口", ""])
    for track_code, title, _, summary in TRACK_DEFINITIONS:
        track_learnable = [
            skill
            for skill in available_new_skills
            if track_definition_for_skill(skill.number)[0] == track_code
        ]
        track_labels = (
            "、".join(f"{skill.skill_id}：{skill.name}" for skill in track_learnable)
            if track_learnable
            else "无"
        )
        lines.append(f"- **{title}**：{track_labels}")
        lines.append(f"  {summary}")

    lines.extend(["", "## 概念课开场模板", ""])
    lines.append("1. 只给当时可见信息，不先揭示结果，严格用信息切片开场。")
    lines.append("2. 盛言先问“你怎么解释这个”，不提前铺定义。")
    if top_categories:
        for category in top_categories:
            lines.append(
                f"- `{category}`：{WEAKNESS_RECOMMENDATIONS[category]['concept']}"
            )
    else:
        lines.append("3. 暂无稳定弱点数据，按标准案例流程推进。")
    lines.append("3. Root 只追问隐含假设、边界条件和因果方向，不替学习者补答案。")

    lines.extend(["", "## 练习课 / 复习课开场模板", ""])
    lines.append("1. Shaw 维持标准开场格式：技能点、10题、独立作答、不看笔记。")
    if top_categories:
        for category in top_categories:
            lines.append(
                f"- `{category}`：{WEAKNESS_RECOMMENDATIONS[category]['practice']}"
            )
    else:
        lines.append("2. 暂无稳定弱点数据，按默认题型比例执行。")
    lines.append("2. 复习 / 延迟验证时不做概念讲解，只按到期技能点短测或复习。")

    lines.extend(["", "## 今日优先技能点", ""])
    if not priority_skills:
        lines.append("*（空）*")
    else:
        for skill in priority_skills:
            mode, reason = recommended_session_mode(skill, today, homework_entries)
            dossier_reference = case_dossier_reference_for_skill(skill)
            question_bank_reference = question_bank_reference_for_skill(skill)
            latest_entry = latest_homework_entry_for_skill(homework_entries, skill.skill_id)
            latest_result = "尚无练习/复习记录。"
            if latest_entry and latest_entry.entry_date:
                if latest_entry.accuracy != "—":
                    latest_result = (
                        f"{latest_entry.entry_date.isoformat()} {latest_entry.accuracy} {latest_entry.judgment}"
                    )
                else:
                    latest_result = (
                        f"{latest_entry.entry_date.isoformat()} {latest_entry.judgment}"
                    )

            skill_lines = [
                f"### {skill.skill_id}：{skill.name}",
                "",
                f"- **建议模式**：{mode}",
                f"- **当前原因**：{reason}",
                f"- **参考资源**：{render_resource_references(skill)}",
            ]
            if dossier_reference:
                skill_lines.append(f"- **案例 dossier**：{dossier_reference}")
            if question_bank_reference:
                skill_lines.append(f"- **题库 / 评分 rubric**：{question_bank_reference}")
            skill_lines.extend(
                [
                    f"- **最近结果**：{latest_result}",
                    f"- **遗留问题**：{latest_follow_up_for_skill(skill, homework_entries, archive_entries)}",
                    f"- **强制教学动作**：{mandatory_action_for_skill(skill, homework_entries, archive_entries)}",
                    f"- **概念课建议追问**：{concept_guidance_for_skill(skill, homework_entries, archive_entries)}",
                    f"- **练习课建议题型**：{practice_guidance_for_skill(skill, homework_entries, archive_entries)}",
                    "- **Shaw 起手模板**：",
                    *[f"  - {line}" for line in render_shaw_starter_template(skill, homework_entries)],
                    "",
                ]
            )
            lines.extend(skill_lines)

    lines.extend(["---", "", "## 如明确打破冻结，可开的新技能点", ""])
    if not available_new_skills:
        lines.append("*（空）*")
    else:
        for track_code, title, _, summary in TRACK_DEFINITIONS:
            track_new_skills = [
                skill
                for skill in available_new_skills
                if track_definition_for_skill(skill.number)[0] == track_code
            ]
            lines.extend([f"### {title}", "", f"> {summary}", ""])
            if not track_new_skills:
                lines.extend(["*（空）*", ""])
                continue
            for skill in track_new_skills:
                case_template = case_template_for_skill(skill, homework_entries)
                question_bank_reference = question_bank_reference_for_skill(skill)
                skill_lines = [
                    f"#### {skill.skill_id}：{skill.name}",
                    "",
                    "- **建议模式**：概念课",
                    f"- **当前原因**：{recommended_session_mode(skill, today, homework_entries)[1]}",
                    f"- **参考资源**：{render_resource_references(skill)}",
                ]
                if case_template["dossier"]:
                    skill_lines.append(f"- **案例 dossier**：{case_template['dossier']}")
                if question_bank_reference:
                    skill_lines.append(f"- **题库 / 评分 rubric**：{question_bank_reference}")
                skill_lines.extend(
                    [
                        f"- **强制教学动作**：{mandatory_action_for_skill(skill, homework_entries, archive_entries)}",
                        f"- **概念课建议追问**：{concept_guidance_for_skill(skill, homework_entries, archive_entries)}",
                        f"- **练习课建议题型**：{practice_guidance_for_skill(skill, homework_entries, archive_entries)}",
                        "- **首次练习时的 Shaw 起手模板**：",
                        *[f"  - {line}" for line in render_shaw_starter_template(skill, homework_entries)],
                        "- **信息切片案例模板**：按以下 6 项开场。",
                        f"- **建议案例强度**：{case_template['recommended_level']}（{case_template['recommended_reason']}）",
                        f"- **入门切片**：{case_template['entry_cases']}",
                        f"- **标准切片**：{case_template['standard_cases']}",
                        f"- **高压反例切片**：{case_template['stress_cases']}",
                        f"- **案例材料入口**：{case_template['source']}",
                        f"- **案例母题**：{case_template['theme']}",
                        f"- **当时已知信息**：{case_template['known']}",
                        f"- **当时未知信息**：{case_template['unknown']}",
                        f"- **当下第一问**：{case_template['question']}",
                        f"- **结果揭示方式**：{case_template['reveal']}",
                        f"- **偏差复盘重点**：{case_template['retro']}",
                        "",
                    ]
                )
                lines.extend(skill_lines)

    return "\n".join(lines).rstrip() + "\n"


def replace_section(text: str, heading: str, next_heading: str, body: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(heading)}\n\n)(.*?)(?=\n---\n\n## {re.escape(next_heading)}\n)",
        re.MULTILINE | re.DOTALL,
    )
    replacement = rf"\1{body.rstrip()}\n"
    new_text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise ValueError(f"Unable to replace section: {heading}")
    return new_text


def apply_concept_events(
    skills: list[Skill],
    concept_events_by_skill: dict[str, list[ConceptEvent]],
) -> list[Skill]:
    synced_skills: list[Skill] = []
    for skill in skills:
        synced_skills.append(
            replace(
                skill,
                concept_completed=render_concept_completed_value(
                    skill,
                    concept_events_by_skill.get(skill.skill_id, []),
                ),
            )
        )
    return synced_skills


def collect_mastery_snapshots(entries: list[HomeworkEntry]) -> dict[str, MasterySnapshot]:
    first_mastery_dates: dict[str, date] = {}
    latest_mastery_dates: dict[str, date] = {}

    for entry in entries:
        if not entry.skill_id or not entry.entry_date:
            continue
        if "间隔复习" in entry.session_title or "复习课" in entry.session_title:
            continue
        if "✅" not in entry.judgment or "掌握" not in entry.judgment:
            continue

        first_mastery_dates.setdefault(entry.skill_id, entry.entry_date)
        latest_mastery_dates[entry.skill_id] = entry.entry_date

    snapshots: dict[str, MasterySnapshot] = {}
    for skill_id in sorted({*first_mastery_dates, *latest_mastery_dates}):
        snapshots[skill_id] = MasterySnapshot(
            first_mastery_date=first_mastery_dates.get(skill_id),
            latest_mastery_date=latest_mastery_dates.get(skill_id),
        )
    return snapshots


def apply_mastery_snapshots(
    skills: list[Skill],
    snapshots: dict[str, MasterySnapshot],
) -> list[Skill]:
    synced_skills: list[Skill] = []
    for skill in skills:
        snapshot = snapshots.get(skill.skill_id)
        first_mastery_date = (
            snapshot.first_mastery_date
            if snapshot and snapshot.first_mastery_date
            else skill.first_mastery_date
        )
        latest_mastery_date = (
            snapshot.latest_mastery_date
            if snapshot and snapshot.latest_mastery_date
            else skill.latest_mastery_date
        )
        if not latest_mastery_date and first_mastery_date:
            latest_mastery_date = first_mastery_date
        synced_skills.append(
            replace(
                skill,
                first_mastery_date=first_mastery_date,
                latest_mastery_date=latest_mastery_date,
            )
        )
    return synced_skills


def collect_delayed_validation_snapshots(
    entries: list[HomeworkEntry],
) -> dict[str, DelayedValidationSnapshot]:
    latest_pass_by_skill: dict[str, date] = {}

    for entry in entries:
        if not entry.skill_id or not entry.entry_date:
            continue
        if "延迟验证" not in entry.session_title:
            continue
        if "✅" in entry.judgment:
            latest_pass_by_skill[entry.skill_id] = entry.entry_date

    return {
        skill_id: DelayedValidationSnapshot(passed_date=passed_date)
        for skill_id, passed_date in latest_pass_by_skill.items()
    }


def apply_delayed_validation_snapshots(
    skills: list[Skill],
    snapshots: dict[str, DelayedValidationSnapshot],
) -> list[Skill]:
    synced_skills: list[Skill] = []
    for skill in skills:
        snapshot = snapshots.get(skill.skill_id)
        passed_date = None
        if snapshot and snapshot.passed_date and (
            not skill.latest_mastery_date or snapshot.passed_date >= skill.latest_mastery_date
        ):
            passed_date = snapshot.passed_date
        elif skill.delayed_validation_passed_date and (
            not skill.latest_mastery_date or skill.delayed_validation_passed_date >= skill.latest_mastery_date
        ):
            passed_date = skill.delayed_validation_passed_date
        elif skill.latest_mastery_date and skill.review_due:
            # Legacy data predates delayed validation; preserve stable-mastery semantics.
            passed_date = skill.latest_mastery_date

        delayed_due = None
        review_due = skill.review_due
        if skill.latest_mastery_date and not passed_date:
            delayed_due = skill.latest_mastery_date + timedelta(days=2)
            review_due = None
        elif skill.review_round == 0 and passed_date and not review_due:
            review_due = passed_date + timedelta(days=7)

        synced_skills.append(
            replace(
                skill,
                delayed_validation_due=delayed_due,
                delayed_validation_passed_date=passed_date,
                review_due=review_due,
            )
        )
    return synced_skills


def review_due_skills(
    skills: list[Skill],
    today: date,
    homework_entries: list[HomeworkEntry] | None = None,
) -> list[Skill]:
    due = [
        skill
        for skill in skills
        if skill.review_due and skill.is_mastered and skill.review_due <= today
    ]
    if not homework_entries:
        return sorted(due, key=lambda skill: (skill.review_due, skill.number))
    return sorted(
        due,
        key=lambda skill: (
            -review_priority_snapshot(skill, homework_entries, today).status_rank,
            -review_priority_snapshot(skill, homework_entries, today).overdue_days,
            -review_priority_snapshot(skill, homework_entries, today).error_mode_count,
            skill.review_due,
            skill.number,
        ),
    )


def delayed_validation_due_skills(skills: list[Skill], today: date) -> list[Skill]:
    due = [
        skill
        for skill in skills
        if skill.needs_delayed_validation
        and skill.delayed_validation_due
        and skill.delayed_validation_due <= today
    ]
    return sorted(due, key=lambda skill: (skill.delayed_validation_due, skill.number))


def scheduling_policy(skills: list[Skill], today: date) -> SchedulingPolicy:
    delayed_due = len(delayed_validation_due_skills(skills, today))
    review_due = len(review_due_skills(skills, today))

    if delayed_due > 0:
        return SchedulingPolicy(
            code="delay_validation_first",
            headline="延迟验证优先",
            detail=f"当前有 {delayed_due} 个技能点延迟验证到期。先完成延迟验证，不安排新课。",
        )
    if review_due >= 5:
        return SchedulingPolicy(
            code="review_only",
            headline="复习债过高",
            detail=f"当前有 {review_due} 个技能点复习到期。只允许清理复习债，不安排新概念课或新练习课。",
        )
    if review_due >= 3:
        return SchedulingPolicy(
            code="freeze_new_lessons",
            headline="默认冻结新课",
            detail=f"当前有 {review_due} 个技能点复习到期。默认冻结新课，先清理复习债；只有用户明确要求时才打破。",
        )
    if review_due > 0:
        return SchedulingPolicy(
            code="review_first",
            headline="复习优先",
            detail=f"当前有 {review_due} 个技能点复习到期。建议先做复习，再决定是否开新课。",
        )
    return SchedulingPolicy(
        code="open",
        headline="可开新课",
        detail="当前没有延迟验证或复习债阻塞，可以按技能前置正常推进。",
    )


def currently_learnable_skills(skills: list[Skill], skills_by_id: dict[str, Skill]) -> list[Skill]:
    learnable: list[Skill] = []
    for skill in skills:
        if skill.status.startswith("🔒") or skill.is_mastered:
            continue
        if all(skills_by_id[prereq].is_mastered for prereq in skill.prereqs):
            learnable.append(skill)
    return learnable


def stage_title_for_skill(number: int) -> str:
    for start, end, title in STAGE_DEFINITIONS:
        if start <= number <= end:
            return title
    raise ValueError(f"No stage definition found for skill number {number}.")


def track_definition_for_skill(number: int) -> tuple[str, str, tuple[tuple[int, int], ...], str]:
    for definition in TRACK_DEFINITIONS:
        _, _, ranges, _ = definition
        if any(start <= number <= end for start, end in ranges):
            return definition
    raise ValueError(f"No track definition found for skill number {number}.")


def skills_in_track(skills: list[Skill], track_code: str) -> list[Skill]:
    return [
        skill
        for skill in skills
        if track_definition_for_skill(skill.number)[0] == track_code
    ]


def render_track_new_skill_labels(skills: list[Skill]) -> str:
    new_skills = [skill for skill in skills if skill.status.startswith("⬜")]
    if not new_skills:
        return "无"
    return "、".join(f"{skill.skill_id}：{skill.name}" for skill in new_skills)


def render_dual_track_progress(
    skills: list[Skill],
    skills_by_id: dict[str, Skill],
) -> str:
    learnable_skills = currently_learnable_skills(skills, skills_by_id)
    lines = [
        "> 技能明细仍按阶段维护；新课排程按双主线观察。",
        "",
        "| 主线 | 覆盖技能 | 稳定掌握 | 进行中 | 当前可开新技能 |",
        "|------|---------|---------|--------|---------------|",
    ]
    for track_code, title, ranges, _ in TRACK_DEFINITIONS:
        track_skills = skills_in_track(skills, track_code)
        track_learnable = [
            skill
            for skill in learnable_skills
            if track_definition_for_skill(skill.number)[0] == track_code
        ]
        lines.append(
            f"| {title} | {' + '.join(f'SK-{start:03d}~SK-{end:03d}' for start, end in ranges)} | {sum(skill.is_mastered for skill in track_skills)}/{len(track_skills)} | {sum(skill.is_active or skill.needs_delayed_validation for skill in track_skills)} | {render_track_new_skill_labels(track_learnable)} |"
        )
    return "\n".join(lines)


def render_track_learnable_blocks(learnable: list[Skill]) -> list[str]:
    blocks: list[str] = []
    for track_code, title, _, summary in TRACK_DEFINITIONS:
        track_skills = [
            skill
            for skill in learnable
            if track_definition_for_skill(skill.number)[0] == track_code
        ]
        blocks.extend(
            [
                f"### {title}",
                "",
                f"> {summary}",
                "",
            ]
        )
        if track_skills:
            blocks.extend(f"- {skill.skill_id}：{skill.name}" for skill in track_skills)
        else:
            blocks.append("*（空）*")
        blocks.append("")
    if blocks and blocks[-1] == "":
        blocks.pop()
    return blocks


def compute_review_schedule(mastery_date: date | None) -> tuple[str, str, str, str]:
    if not mastery_date:
        return ("—", "—", "—", "—")
    checkpoints = (7, 28, 88, 178)
    return tuple((mastery_date + timedelta(days=days)).isoformat() for days in checkpoints)


def render_history(history_accuracies: tuple[str, ...]) -> str:
    return "[" + ", ".join(history_accuracies) + "]" if history_accuracies else "[]"


def resource_references_for_skill(skill: Skill) -> tuple[str, ...]:
    number = skill.number
    if number <= 3:
        return MACRO_FOUNDATION_RESOURCES
    if skill.skill_id == "SK-004":
        return INFLATION_MECHANISM_RESOURCES
    if number <= 5:
        return MONETARY_EXPANSION_RESOURCES
    if number <= 10:
        return BITCOIN_MECHANICS_RESOURCES
    if number <= 18:
        return MACRO_CYCLE_RESOURCES
    if skill.skill_id == "SK-019":
        return PROBABILITY_DECISION_RESOURCES
    if skill.skill_id == "SK-020":
        return RISK_DECISION_RESOURCES
    if skill.skill_id == "SK-021":
        return EXPECTANCY_RESOURCES
    if skill.skill_id in {"SK-022", "SK-023"}:
        return POSITION_SIZING_RESOURCES
    if skill.skill_id in {"SK-024", "SK-025"}:
        return EXIT_RULE_RESOURCES
    if skill.skill_id == "SK-026":
        return LIQUIDATION_RESOURCES
    if skill.skill_id == "SK-027":
        return CEX_RISK_RESOURCES
    if skill.skill_id == "SK-028":
        return DEFI_RISK_RESOURCES
    if skill.skill_id == "SK-029":
        return OPSEC_RESOURCES
    if skill.skill_id == "SK-030":
        return TRADING_JOURNAL_RESOURCES
    if 31 <= number <= 42:
        return ONCHAIN_CYCLE_RESOURCES
    if skill.skill_id == "SK-043":
        return INSTRUMENT_CHOICE_RESOURCES
    if skill.skill_id == "SK-044":
        return FUNDING_RATE_RESOURCES
    if skill.skill_id == "SK-045":
        return LIQUIDITY_SLIPPAGE_RESOURCES
    if 43 <= number <= 45:
        return DERIVATIVES_RESOURCES
    if 46 <= number <= 51:
        return TA_EXECUTION_RESOURCES
    if skill.skill_id == "SK-052":
        return THREE_FRAMEWORK_SYNTHESIS_RESOURCES
    if skill.skill_id == "SK-053":
        return MARCH_2020_CASE_RESOURCES
    if skill.skill_id == "SK-054":
        return NOV_2021_CASE_RESOURCES
    if number == 52:
        return SYNTHESIS_RESOURCES
    if skill.skill_id == "SK-055":
        return LUNA_CASE_RESOURCES
    if skill.skill_id == "SK-056":
        return FLASH_CRASH_RESOURCES
    if skill.skill_id == "SK-057":
        return GRADUATION_RESOURCES
    return ()


def render_resource_references(skill: Skill) -> str:
    references = resource_references_for_skill(skill)
    return "；".join(references) if references else "待补充"


def render_skill_block(skill: Skill) -> str:
    return "\n".join(
        [
            f"### {skill.skill_id}：{skill.name}",
            "",
            f"- **描述**：{skill.description}",
            f"- **前置技能**：{skill.prereq_text}",
            f"- **掌握标准**：{skill.mastery_standard}",
            f"- **主要参考资源**：{render_resource_references(skill)}",
            f"- **状态**：{skill.rendered_status}",
            f"- **概念课完成**：{skill.concept_completed}",
            f"- **首次掌握日期**：{format_date(skill.first_mastery_date)}",
            f"- **最近达标日期**：{format_date(skill.latest_mastery_date)}",
            f"- **延迟验证到期**：{format_date(skill.delayed_validation_due)}",
            f"- **延迟验证通过日期**：{format_date(skill.delayed_validation_passed_date)}",
            f"- **最后练习**：{format_date(skill.last_practice)}",
            f"- **历史准确率**：{render_history(skill.history_accuracies)}",
            f"- **复习到期**：{format_date(skill.review_due)}",
            f"- **复习轮次**：{skill.review_round}",
        ]
    )


def build_mastery_records(skills: list[Skill], entries: list[HomeworkEntry]) -> list[MasteryRecord]:
    first_mastery_entry_by_skill: dict[str, HomeworkEntry] = {}

    for entry in entries:
        if not entry.skill_id or "间隔复习" in entry.session_title:
            continue
        if "✅" not in entry.judgment or "掌握" not in entry.judgment:
            continue
        first_mastery_entry_by_skill.setdefault(entry.skill_id, entry)

    records: list[MasteryRecord] = []
    error_mode_order = {
        mode: index for index, (mode, _) in enumerate(ERROR_MODE_PATTERNS)
    }
    for skill in skills:
        mastery_entry = first_mastery_entry_by_skill.get(skill.skill_id)
        if mastery_entry and mastery_entry.entry_date:
            skill_entries_before_mastery = [
                entry
                for entry in entries
                if entry.skill_id == skill.skill_id
                and entry.header_index <= mastery_entry.header_index
            ]
            attempt_count = sum(
                1
                for entry in skill_entries_before_mastery
                if "练习课" in entry.session_title and "间隔复习" not in entry.session_title
            )
            concept_retry_before_mastery = any(
                "概念" in entry.session_title and "重修" in entry.session_title
                for entry in skill_entries_before_mastery
            )
            if concept_retry_before_mastery:
                mastery_method = "概念重修后通过"
            elif attempt_count > 1:
                mastery_method = "练习重试后通过"
            else:
                mastery_method = "首练通过"

            failure_mode_counter: Counter[str] = Counter()
            for entry in skill_entries_before_mastery:
                if "练习课" not in entry.session_title or "间隔复习" in entry.session_title:
                    continue
                if entry.header_index >= mastery_entry.header_index and "✅" in entry.judgment:
                    continue
                failure_mode_counter.update(
                    normalize_error_modes(extract_error_mode_text(entry))
                )
            primary_failure_types = "无"
            if failure_mode_counter:
                top_failure_modes = sorted(
                    failure_mode_counter.items(),
                    key=lambda item: (-item[1], error_mode_order[item[0]]),
                )[:3]
                primary_failure_types = "；".join(
                    f"{mode}×{count}" if count > 1 else mode
                    for mode, count in top_failure_modes
                )

            delayed_validation_entry = next(
                (
                    entry
                    for entry in entries
                    if entry.skill_id == skill.skill_id
                    and entry.entry_date
                    and entry.entry_date >= mastery_entry.entry_date
                    and "延迟验证" in entry.session_title
                    and "✅" in entry.judgment
                ),
                None,
            )
            delayed_validation = (
                f"是（{format_date(delayed_validation_entry.entry_date)}）"
                if delayed_validation_entry and delayed_validation_entry.entry_date
                else "未记录"
            )
            records.append(
                MasteryRecord(
                    skill_id=skill.skill_id,
                    skill_name=skill.name,
                    first_mastery_date=mastery_entry.entry_date,
                    mastery_method=mastery_method,
                    final_accuracy=short_accuracy(mastery_entry.accuracy),
                    attempt_count=attempt_count,
                    primary_failure_types=primary_failure_types,
                    delayed_validation=delayed_validation,
                )
            )
            continue

        if skill.first_mastery_date:
            final_accuracy = skill.history_accuracies[-1] if skill.history_accuracies else "—"
            records.append(
                MasteryRecord(
                    skill_id=skill.skill_id,
                    skill_name=skill.name,
                    first_mastery_date=skill.first_mastery_date,
                    mastery_method="历史导入",
                    final_accuracy=final_accuracy,
                    attempt_count=len(skill.history_accuracies),
                    primary_failure_types="待补充",
                    delayed_validation="待补充",
                )
            )

    return sorted(
        records,
        key=lambda record: (record.first_mastery_date, int(record.skill_id.split("-")[1])),
    )


def render_mastery_records(skills: list[Skill], entries: list[HomeworkEntry]) -> str:
    records = build_mastery_records(skills, entries)
    lines = [
        "> 由 `teacher/homework_log.md` 的首次“掌握”事件自动生成。",
        "> 记录首次达标时的通过方式、累计练习次数、主要失败类型，以及是否经过延迟验证，不受后续回退或重学影响。",
        "",
        "| 技能点 | 首次掌握日期 | 通过方式 | 最终准确率 | 首次达标耗费次数 | 主要失败类型 | 延迟验证 |",
        "|-------|---------|---------|-----------|----------------|-------------|---------|",
    ]
    if not records:
        lines.append("| （空） | — | — | — | — | — | — |")
        return "\n".join(lines)

    for record in records:
        lines.append(
            f"| {record.skill_id} | {record.first_mastery_date.isoformat()} | {record.mastery_method} | {record.final_accuracy} | {record.attempt_count} | {record.primary_failure_types} | {record.delayed_validation} |"
        )
    return "\n".join(lines)


def render_status_legend() -> str:
    return "\n".join(
        [
            "> 若状态显示 `✅ 待延迟验证`，表示已通过当次练习，但尚未完成 24-72 小时后的短测。",
            "",
            "| 图标 | 状态 | 含义 |",
            "|------|------|------|",
            "| 🔒 | 未解锁 | 前置技能点未掌握 |",
            "| ⬜ | 未学 | 可以开始，尚未进行概念课 |",
            "| 🔵 | 概念已完成 | 概念课已完成，等待练习课 |",
            "| 🟡 | 学习中 | 练习课进行中，未达掌握标准 |",
            "| ✅ | 已掌握 | 达到掌握标准 |",
            "| 🔄 | 复习到期 | 间隔复习时间到 |",
            "| 💚 | 长期掌握 | 完成第3次及以上复习 |",
        ]
    )


def render_overview(skills: list[Skill], today: date) -> str:
    mastered_count = sum(skill.is_mastered for skill in skills)
    delayed_count = sum(skill.needs_delayed_validation for skill in skills)
    active_count = sum(skill.is_active for skill in skills)
    locked_count = sum(skill.status.startswith("🔒") for skill in skills)
    delayed_due_count = len(delayed_validation_due_skills(skills, today))
    due_count = len(review_due_skills(skills, today))
    policy = scheduling_policy(skills, today)
    return "\n".join(
        [
            "| 项目 | 数值 |",
            "|------|------|",
            f"| 总技能点数 | {len(skills)} |",
            f"| 已掌握 | {mastered_count} |",
            f"| 待延迟验证 | {delayed_count} |",
            f"| 学习中 | {active_count} |",
            f"| 未解锁 | {locked_count} |",
            f"| 今日延迟验证到期 | {delayed_due_count} |",
            f"| 今日复习到期 | {due_count} |",
            f"| 今日调度策略 | {policy.headline} |",
        ]
    )


def render_learnable_section(skills: list[Skill], skills_by_id: dict[str, Skill], today: date) -> str:
    learnable = currently_learnable_skills(skills, skills_by_id)
    available_new_skills = [skill for skill in learnable if skill.status.startswith("⬜")]
    policy = scheduling_policy(skills, today)
    lines = ["（按双主线展示；前置技能已掌握，或无前置依赖）", ""]
    lines.extend(render_track_learnable_blocks(available_new_skills))
    lines.extend(
        [
            "",
            f"> 今日调度策略：{policy.headline}",
            f"> {policy.detail}",
            f"> 当前系统日期：{today.isoformat()}。",
        ]
    )
    return "\n".join(lines)


def render_delayed_validation_queue(skills: list[Skill], today: date) -> str:
    due_skills = delayed_validation_due_skills(skills, today)
    lines = [
        "> 由最近一次练习达标自动生成，默认安排在 24-72 小时内回测独立提取能力。",
        "> 延迟验证未通过前，不进入稳定掌握，也不解锁依赖它的新技能点。",
        "",
    ]
    if not due_skills:
        lines.append("*（空）*")
        return "\n".join(lines)

    for skill in due_skills:
        if skill.delayed_validation_due == today:
            status = "今日到期"
        else:
            overdue_days = (today - skill.delayed_validation_due).days
            status = f"已逾期 {overdue_days} 天"
        lines.append(
            f"- {skill.skill_id}：{skill.name}（延迟验证到期 {skill.delayed_validation_due.isoformat()}，{status}）"
        )
    return "\n".join(lines)


def render_scheduling_policy(skills: list[Skill], today: date) -> str:
    policy = scheduling_policy(skills, today)
    return "\n".join(
        [
            f"**今日策略**：{policy.headline}",
            "",
            policy.detail,
        ]
    )


def render_due_queue(
    skills: list[Skill],
    today: date,
    homework_entries: list[HomeworkEntry] | None = None,
) -> str:
    due_skills = review_due_skills(skills, today, homework_entries)
    lines = [
        "> 由 `skill_graph.md` 的技能明细和系统日期自动生成。",
        "> 会话开始时优先处理最该先清的技能点。",
        "> 排序依据：上次复习是否勉强维持 / 未通过、逾期天数、最近错误模式数量。",
        "",
    ]
    if not due_skills:
        lines.append("*（空）*")
        return "\n".join(lines)

    for skill in due_skills:
        next_round = skill.review_round + 1
        if skill.review_due == today:
            status = "今日到期"
        else:
            overdue_days = (today - skill.review_due).days
            status = f"已逾期 {overdue_days} 天"
        priority_reason = (
            review_priority_snapshot(skill, homework_entries, today).reason
            if homework_entries
            else status
        )
        lines.append(
            f"- {skill.skill_id}：{skill.name}（第{next_round}次复习到期 {skill.review_due.isoformat()}，{status}；优先原因：{priority_reason}）"
        )
    return "\n".join(lines)


def render_review_schedule(skills: list[Skill]) -> str:
    lines = [
        "> 以当前“最近达标日期”为基准自动推算。通过复习后，系统会滚动刷新“复习到期”。",
        "",
        "| 技能点 | 第1次复习到期 | 第2次到期 | 第3次到期 | 第4次到期 |",
        "|-------|------------|---------|---------|---------|",
    ]
    mastered_skills = [skill for skill in skills if skill.is_mastered]
    if not mastered_skills:
        lines.append("| （空） | — | — | — | — |")
        return "\n".join(lines)

    for skill in mastered_skills:
        first_due, second_due, third_due, fourth_due = compute_review_schedule(
            skill.review_anchor_date
        )
        lines.append(
            f"| {skill.skill_id} | {first_due} | {second_due} | {third_due} | {fourth_due} |"
        )
    return "\n".join(lines)


def render_review_status(skill: Skill, today: date) -> str:
    if not skill.review_due:
        return "—"
    next_round = skill.review_round + 1
    if skill.review_due < today:
        return f"第{next_round}次复习已到期 {skill.review_due.isoformat()}"
    if skill.review_due == today:
        return f"第{next_round}次复习今日到期"
    return f"第{next_round}次复习到期 {skill.review_due.isoformat()}"


def render_active_skills(skills: list[Skill]) -> str:
    active_skills = [skill for skill in skills if skill.is_active]
    if not active_skills:
        return "*（空）*"

    lines = [
        "| 技能点 | 状态 | 最后练习 | 准确率 |",
        "|-------|------|---------|-------|",
    ]
    for skill in active_skills:
        latest_accuracy = skill.history_accuracies[-1] if skill.history_accuracies else "—"
        lines.append(
            f"| {skill.skill_id}：{skill.name} | {skill.status} | {format_date(skill.last_practice)} | {latest_accuracy} |"
        )
    return "\n".join(lines)


def render_mastered_skills(skills: list[Skill], today: date) -> str:
    mastered_skills = [skill for skill in skills if skill.is_mastered]
    if not mastered_skills:
        return "*（空）*"

    mastered_skills.sort(
        key=lambda skill: (
            skill.first_mastery_date or skill.latest_mastery_date or date.min,
            skill.number,
        )
    )
    lines = [
        "| 技能点 | 首次掌握 | 最近达标 | 复习状态 |",
        "|-------|---------|---------|---------|",
    ]
    for skill in mastered_skills:
        lines.append(
            f"| {skill.skill_id}：{skill.name} | {format_date(skill.first_mastery_date)} | {format_date(skill.latest_mastery_date)} | {render_review_status(skill, today)} |"
        )
    return "\n".join(lines)


def render_recent_entries(entries: list[HomeworkEntry]) -> str:
    if not entries:
        return "*（空）*"

    recent_entries = entries[-5:]
    lines = [
        "| 日期 | 技能点 | 准确率 | 判定 |",
        "|------|-------|-------|------|",
    ]
    for entry in recent_entries:
        if entry.skill_id and entry.skill_name:
            skill_label = f"{entry.skill_id}：{entry.skill_name}"
        else:
            skill_label = entry.session_title
        lines.append(
            f"| {format_date(entry.entry_date)} | {skill_label} | {entry.accuracy} | {entry.judgment} |"
        )
    return "\n".join(lines)


def first_mastery_dates(skills: list[Skill]) -> list[date]:
    return sorted(
        skill.first_mastery_date
        for skill in skills
        if skill.first_mastery_date
    )


def first_review_completion(entries: list[HomeworkEntry]) -> str:
    for entry in entries:
        if "间隔复习" in entry.session_title and "复习完成" in entry.judgment:
            return format_date(entry.entry_date)
    return "—"


def stage_completion_date(skills: dict[str, Skill], start: int, end: int) -> str:
    stage_skills = [skills[f"SK-{number:03d}"] for number in range(start, end + 1)]
    if not all(skill.is_mastered for skill in stage_skills):
        return "—"
    return format_date(max(skill.review_anchor_date for skill in stage_skills if skill.review_anchor_date))


def track_completion_date(skills: dict[str, Skill], track_code: str) -> str:
    track_skills = skills_in_track(list(skills.values()), track_code)
    if not track_skills or not all(skill.is_mastered for skill in track_skills):
        return "—"
    return format_date(
        max(skill.review_anchor_date for skill in track_skills if skill.review_anchor_date)
    )


def render_milestones(skills: list[Skill], entries: list[HomeworkEntry]) -> str:
    mastered_dates = first_mastery_dates(skills)
    nth_mastered = {
        1: format_date(mastered_dates[0]) if len(mastered_dates) >= 1 else "—",
        5: format_date(mastered_dates[4]) if len(mastered_dates) >= 5 else "—",
        10: format_date(mastered_dates[9]) if len(mastered_dates) >= 10 else "—",
    }
    long_term_dates = sorted(
        skill.latest_mastery_date
        for skill in skills
        if skill.status.startswith("💚") and skill.latest_mastery_date
    )
    skills_by_id = {skill.skill_id: skill for skill in skills}

    lines = [
        "| 里程碑 | 完成日期 |",
        "|-------|---------|",
        f"| 第1个技能点掌握 | {nth_mastered[1]} |",
        f"| 第5个技能点掌握 | {nth_mastered[5]} |",
        f"| 第10个技能点掌握 | {nth_mastered[10]} |",
        f"| 完成第一次间隔复习 | {first_review_completion(entries)} |",
        f"| 第一个技能点进入\"长期掌握\" | {format_date(long_term_dates[0]) if long_term_dates else '—'} |",
        f"| 完成第一阶段（SK-001~018全部掌握）| {stage_completion_date(skills_by_id, 1, 18)} |",
        f"| 完成第二阶段（SK-019~030全部掌握）| {stage_completion_date(skills_by_id, 19, 30)} |",
        f"| 完成第三阶段（SK-031~042全部掌握）| {stage_completion_date(skills_by_id, 31, 42)} |",
        f"| 完成第四阶段（SK-043~057全部掌握）| {stage_completion_date(skills_by_id, 43, 57)} |",
        f"| 完成主线A（货币 / 宏观 / 周期）| {track_completion_date(skills_by_id, 'macro_cycle')} |",
        f"| 完成主线B（风险 / 执行 / 交易结构）| {track_completion_date(skills_by_id, 'risk_execution')} |",
    ]

    if all(skill.is_mastered for skill in skills):
        final_date = format_date(max(skill.review_anchor_date for skill in skills if skill.review_anchor_date))
    else:
        final_date = "—"
    lines.append(f"| 所有57个技能点掌握 | {final_date} |")
    return "\n".join(lines)


def render_practice_trend(entries: list[HomeworkEntry]) -> str:
    practice_entries = [
        entry for entry in entries
        if "练习课" in entry.session_title and entry.skill_id and entry.skill_name
    ]
    if not practice_entries:
        return "| 日期 | 技能点 | 准确率 | 判定 | 主要薄弱点 |\n|------|--------|--------|------|----------|\n| （空） | | | | |"

    lines = [
        "| 日期 | 技能点 | 准确率 | 判定 | 主要薄弱点 |",
        "|------|--------|--------|------|----------|",
    ]
    for entry in practice_entries:
        lines.append(
            f"| {format_date(entry.entry_date)} | {entry.skill_id}：{entry.skill_name} | {entry.accuracy} | {entry.judgment} | {entry.weak_points} |"
        )
    return "\n".join(lines)


def concept_highlight(entry: HomeworkEntry) -> str:
    concept_slice = extract_concept_slice(entry)
    for key in ("复述检验", "学习者当下判断"):
        value = concept_slice.get(key)
        if value and value not in {"通过", "未通过"}:
            return value
    for key in ("关键辨析突破", "核心教学方法"):
        value = extract_named_value(entry.body, key)
        if value:
            return value
    return "待补充"


def concept_improvement(entry: HomeworkEntry) -> str:
    concept_slice = extract_concept_slice(entry)
    for key in ("偏差复盘", "框架边界", "盛言收尾评注"):
        value = concept_slice.get(key) if key in concept_slice else extract_named_value(entry.body, key)
        if value:
            return value
    return "待补充"


def render_concept_performance(entries: list[HomeworkEntry]) -> str:
    concept_entries = [
        entry for entry in entries
        if "概念" in entry.session_title and entry.skill_id and entry.skill_name
    ]
    if not concept_entries:
        return (
            "| 日期 | 技能点 | 开场案例 | 推理亮点 | 需要改进 |\n"
            "|------|--------|---------|---------|---------|\n"
            "| （空） | | | | |"
        )

    lines = [
        "| 日期 | 技能点 | 开场案例 | 推理亮点 | 需要改进 |",
        "|------|--------|---------|---------|---------|",
    ]
    for entry in concept_entries:
        concept_slice = extract_concept_slice(entry)
        case = concept_slice.get("盛言开场案例", "待补充")
        lines.append(
            f"| {format_date(entry.entry_date)} | {entry.skill_id}：{entry.skill_name} | {case} | {concept_highlight(entry)} | {concept_improvement(entry)} |"
        )
    return "\n".join(lines)


def extract_error_mode_text(entry: HomeworkEntry) -> str:
    values: list[str] = []
    for label in ("错误模式", "错误模式（如有）"):
        value = extract_named_value(entry.body, label)
        if value and value not in {"无", "—"}:
            values.append(value)
    return "；".join(values)


def normalize_error_modes(raw: str) -> tuple[str, ...]:
    if not raw or raw in {"无", "—"}:
        return ()

    modes: list[str] = []
    for canonical, aliases in ERROR_MODE_PATTERNS:
        if any(alias in raw for alias in aliases):
            modes.append(canonical)
    return tuple(modes)


def error_modes_for_entry(entry: HomeworkEntry) -> tuple[str, ...]:
    return normalize_error_modes(extract_error_mode_text(entry))


def ordered_teaching_action_triggers(
    triggers: list[TeachingActionTrigger],
) -> list[TeachingActionTrigger]:
    error_mode_order = {
        mode: index for index, (mode, _) in enumerate(ERROR_MODE_PATTERNS)
    }
    return sorted(
        triggers,
        key=lambda trigger: (
            ACTION_BUCKET_ORDER[trigger.bucket],
            error_mode_order[trigger.error_mode],
        ),
    )


def resets_teaching_cycle(entry: HomeworkEntry) -> bool:
    if "概念" in entry.session_title:
        return True
    return "✅" in entry.judgment


def latest_triggered_teaching_actions(
    entries: list[HomeworkEntry],
    skill_id: str | None = None,
) -> dict[str, list[TeachingActionTrigger]]:
    relevant_entries = [
        entry
        for entry in entries
        if entry.skill_id and (skill_id is None or entry.skill_id == skill_id)
    ]
    grouped_entries: dict[str, list[HomeworkEntry]] = {}
    for entry in relevant_entries:
        grouped_entries.setdefault(entry.skill_id, []).append(entry)

    triggered_actions: dict[str, list[TeachingActionTrigger]] = {}
    for current_skill_id, skill_entries in grouped_entries.items():
        ordered_entries = sorted(skill_entries, key=lambda entry: entry.header_index)
        latest_scored_index = next(
            (
                index
                for index in range(len(ordered_entries) - 1, -1, -1)
                if ordered_entries[index].accuracy != "—"
            ),
            None,
        )
        if latest_scored_index is None:
            continue

        latest_entry = ordered_entries[latest_scored_index]
        if resets_teaching_cycle(latest_entry):
            continue

        latest_modes = error_modes_for_entry(latest_entry)
        if not latest_modes:
            continue

        cycle_start_index = 0
        for index in range(latest_scored_index - 1, -1, -1):
            if resets_teaching_cycle(ordered_entries[index]):
                cycle_start_index = index + 1
                break

        cycle_entries = [
            entry
            for entry in ordered_entries[cycle_start_index : latest_scored_index + 1]
            if entry.accuracy != "—"
        ]
        mode_sets = [set(error_modes_for_entry(entry)) for entry in cycle_entries]
        triggers: list[TeachingActionTrigger] = []
        for mode in latest_modes:
            if mode not in ERROR_ACTION_RULES:
                continue
            streak = 1
            for previous_modes in reversed(mode_sets[:-1]):
                if mode not in previous_modes:
                    break
                streak += 1
            if streak < 2:
                continue
            rule = ERROR_ACTION_RULES[mode]
            triggers.append(
                TeachingActionTrigger(
                    skill_id=current_skill_id,
                    skill_name=latest_entry.skill_name or current_skill_id,
                    error_mode=mode,
                    streak=streak,
                    bucket=rule["bucket"],
                    next_session=rule["next_session"],
                    detail=rule["detail"],
                )
            )
        if triggers:
            triggered_actions[current_skill_id] = ordered_teaching_action_triggers(triggers)
    return triggered_actions


def triggered_teaching_actions_for_skill(
    entries: list[HomeworkEntry],
    skill_id: str,
) -> list[TeachingActionTrigger]:
    return latest_triggered_teaching_actions(entries, skill_id).get(skill_id, [])


def render_teaching_action_trigger(trigger: TeachingActionTrigger) -> str:
    return (
        f"连续{trigger.streak}次{trigger.error_mode} → "
        f"{trigger.next_session}：{trigger.detail}"
    )


def summarize_mandatory_action_for_skill(
    entries: list[HomeworkEntry],
    skill_id: str | None,
) -> str:
    if not skill_id:
        return "无"
    triggers = triggered_teaching_actions_for_skill(entries, skill_id)
    if not triggers:
        return "无"
    return "；".join(render_teaching_action_trigger(trigger) for trigger in triggers)


def infer_weakness_categories(entry: HomeworkEntry) -> tuple[str, ...]:
    error_mode_text = extract_error_mode_text(entry)
    normalized_modes = normalize_error_modes(error_mode_text)
    combined_text = "；".join(
        part
        for part in (
            entry.weak_points,
            error_mode_text,
            "；".join(normalized_modes),
        )
        if part and part not in {"无", "—"}
    )
    if not combined_text:
        return ()

    categories: list[str] = []
    for category, keywords in WEAKNESS_PATTERNS:
        if any(keyword in combined_text for keyword in keywords):
            categories.append(category)
    return tuple(categories)


def scored_entries(entries: list[HomeworkEntry]) -> list[HomeworkEntry]:
    return [
        entry
        for entry in entries
        if entry.skill_id and entry.entry_date and entry.accuracy != "—"
    ]


def weakness_counter(entries: list[HomeworkEntry]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for entry in scored_entries(entries):
        counter.update(infer_weakness_categories(entry))
    return counter


def ordered_weakness_items(counter: Counter[str]) -> list[tuple[str, int]]:
    weakness_order = {
        category: index for index, (category, _) in enumerate(WEAKNESS_PATTERNS)
    }
    return sorted(
        counter.items(),
        key=lambda item: (-item[1], weakness_order[item[0]]),
    )


def ordered_error_mode_items(counter: Counter[str]) -> list[tuple[str, int]]:
    error_mode_order = {
        mode: index for index, (mode, _) in enumerate(ERROR_MODE_PATTERNS)
    }
    return sorted(
        counter.items(),
        key=lambda item: (-item[1], error_mode_order[item[0]]),
    )


def recent_error_scope_entries(
    entries: list[HomeworkEntry],
    today: date,
    recent_days: int = 14,
    fallback_limit: int = 5,
) -> tuple[list[HomeworkEntry], str]:
    recent_window_start = today - timedelta(days=recent_days - 1)
    recent_entries = [
        entry
        for entry in scored_entries(entries)
        if recent_window_start <= entry.entry_date <= today
    ]
    recent_entries_with_errors = [
        entry for entry in recent_entries if error_modes_for_entry(entry)
    ]
    if recent_entries_with_errors:
        return (
            recent_entries_with_errors,
            f"最近{recent_days}天（{format_date(recent_window_start)} 至 {format_date(today)}）",
        )

    fallback_entries = [
        entry for entry in scored_entries(entries) if error_modes_for_entry(entry)
    ][-fallback_limit:]
    if fallback_entries:
        return (
            fallback_entries,
            f"最近{len(fallback_entries)}条有结果记录（回退）",
        )
    return ([], f"最近{recent_days}天（{format_date(recent_window_start)} 至 {format_date(today)}）")


def error_repeat_rate(scope_entries: list[HomeworkEntry]) -> tuple[int, int]:
    counter: Counter[str] = Counter()
    for entry in scope_entries:
        counter.update(error_modes_for_entry(entry))
    total_hits = sum(counter.values())
    repeated_hits = sum(count for count in counter.values() if count >= 2)
    return repeated_hits, total_hits


def question_result_is_miss(result: str) -> bool:
    stripped = result.strip()
    return stripped.startswith(("✗", "⚠️"))


def question_type_effectiveness_rows(
    entries: list[HomeworkEntry],
    limit: int = 5,
) -> list[tuple[str, int, int, float]]:
    total_counter: Counter[str] = Counter()
    miss_counter: Counter[str] = Counter()
    for entry in scored_entries(entries):
        for question_type, result in parse_shaw_question_rows(entry.body):
            total_counter[question_type] += 1
            if question_result_is_miss(result):
                miss_counter[question_type] += 1
    rows = [
        (
            question_type,
            miss_counter[question_type],
            total,
            miss_counter[question_type] / total,
        )
        for question_type, total in total_counter.items()
        if total
    ]
    rows.sort(key=lambda item: (-item[3], -item[1], -item[2], item[0]))
    return rows[:limit]


def question_bank_effectiveness_rows(
    entries: list[HomeworkEntry],
    limit: int = 8,
) -> list[tuple[str, int, int, float]]:
    total_counter: Counter[str] = Counter()
    miss_counter: Counter[str] = Counter()
    for entry in scored_entries(entries):
        fallback_source = extract_named_value(entry.body, "题库来源")
        for record in parse_shaw_question_records(entry.body):
            source = record.question_bank_id
            if source in {"", "—", "自拟"}:
                source = fallback_source or ""
            if not source:
                continue
            total_counter[source] += 1
            if question_result_is_miss(record.result):
                miss_counter[source] += 1
    rows = [
        (
            source,
            miss_counter[source],
            total,
            miss_counter[source] / total,
        )
        for source, total in total_counter.items()
        if total
    ]
    rows.sort(key=lambda item: (-item[3], -item[1], -item[2], item[0]))
    return rows[:limit]


def render_concept_resource_trace(slice_info: dict[str, str]) -> str:
    display_labels = {
        "资源段落": "资源",
        "证据包条目": "证据包条目",
        "图示编号": "图示编号",
    }
    trace_parts = [
        f"{display_labels[field]}：{slice_info[field]}"
        for field in ("资源段落", "证据包条目", "图示编号")
        if slice_info.get(field)
    ]
    return "；".join(trace_parts) if trace_parts else "未记录"


def render_practice_resource_trace(entry: HomeworkEntry) -> str:
    trace_parts: list[str] = []
    resource_section = extract_named_value(entry.body, "使用资源段落")
    if resource_section and resource_section not in {"—", "无"}:
        trace_parts.append(f"资源：{resource_section}")
    diagram = extract_named_value(entry.body, "使用图示")
    if diagram and diagram not in {"—", "无"}:
        trace_parts.append(f"图示编号：{diagram}")
    return "；".join(trace_parts) if trace_parts else "未记录"


def concept_follow_up_rows(
    entries: list[HomeworkEntry],
    limit: int = 5,
) -> list[tuple[str, str, str, str]]:
    concept_entries = [
        entry
        for entry in entries
        if "概念" in entry.session_title and entry.skill_id and entry.skill_name and entry.entry_date
    ]
    scored = scored_entries(entries)
    rows: list[tuple[str, str, str, str, int]] = []
    for concept_entry in concept_entries:
        slice_info = extract_concept_slice(concept_entry)
        slice_label = (
            slice_info.get("案例切片")
            or slice_info.get("盛言开场案例")
            or "待补充"
        )
        previous_scored = next(
            (
                entry
                for entry in reversed(scored)
                if entry.skill_id == concept_entry.skill_id
                and entry.header_index < concept_entry.header_index
            ),
            None,
        )
        next_scored = next(
            (
                entry
                for entry in scored
                if entry.skill_id == concept_entry.skill_id
                and entry.header_index > concept_entry.header_index
            ),
            None,
        )
        if next_scored:
            outcome = f"{short_accuracy(next_scored.accuracy)} {next_scored.judgment}"
        else:
            outcome = "待后续结果"

        previous_modes = set(error_modes_for_entry(previous_scored)) if previous_scored else set()
        next_modes = set(error_modes_for_entry(next_scored)) if next_scored else set()
        repeated_modes = [mode for mode, _ in ERROR_MODE_PATTERNS if mode in previous_modes & next_modes]
        if not next_scored:
            repeat_status = "待后续记录"
        elif repeated_modes:
            repeat_status = f"仍重复：{'、'.join(repeated_modes)}"
        elif previous_modes and not next_modes:
            repeat_status = "主要重复错误已清零"
        elif previous_modes:
            repeat_status = "主要重复错误未延续"
        else:
            repeat_status = "前测不足"

        rows.append(
            (
                format_date(concept_entry.entry_date),
                f"{concept_entry.skill_id}：{concept_entry.skill_name}",
                slice_label,
                f"{outcome}；{repeat_status}",
                concept_entry.header_index,
            )
        )
    rows.sort(key=lambda item: item[4], reverse=True)
    return [(date_text, skill, slice_label, summary) for date_text, skill, slice_label, summary, _ in rows[:limit]]


def resource_trace_follow_up_rows(
    entries: list[HomeworkEntry],
    limit: int = 5,
) -> list[tuple[str, str, str, str]]:
    concept_entries = [
        entry
        for entry in entries
        if "概念" in entry.session_title and entry.skill_id and entry.skill_name and entry.entry_date
    ]
    scored = scored_entries(entries)
    rows: list[tuple[str, str, str, str, int]] = []
    for concept_entry in concept_entries:
        slice_info = extract_concept_slice(concept_entry)
        trace = render_concept_resource_trace(slice_info)
        if trace == "未记录":
            continue
        next_scored = next(
            (
                entry
                for entry in scored
                if entry.skill_id == concept_entry.skill_id
                and entry.header_index > concept_entry.header_index
            ),
            None,
        )
        outcome = (
            f"{short_accuracy(next_scored.accuracy)} {next_scored.judgment}"
            if next_scored
            else "待后续结果"
        )
        rows.append(
            (
                format_date(concept_entry.entry_date),
                f"{concept_entry.skill_id}：{concept_entry.skill_name}",
                trace,
                outcome,
                concept_entry.header_index,
            )
        )

    for practice_entry in scored_entries(entries):
        trace = render_practice_resource_trace(practice_entry)
        if trace == "未记录":
            continue
        rows.append(
            (
                format_date(practice_entry.entry_date),
                f"{practice_entry.skill_id}：{practice_entry.skill_name}",
                trace,
                f"{short_accuracy(practice_entry.accuracy)} {practice_entry.judgment}",
                practice_entry.header_index,
            )
        )
    rows.sort(key=lambda item: item[4], reverse=True)
    return [(date_text, skill, trace, outcome) for date_text, skill, trace, outcome, _ in rows[:limit]]


def render_content_effectiveness_metrics(entries: list[HomeworkEntry]) -> str:
    concept_rows = concept_follow_up_rows(entries)
    question_rows = question_type_effectiveness_rows(entries)
    resource_rows = resource_trace_follow_up_rows(entries)
    question_bank_rows = question_bank_effectiveness_rows(entries)

    lines = [
        "> 当前指标优先回答三件事：哪些案例切片之后能接住后续练习，哪些资源/题库被使用后效果如何，哪些题型最容易持续失分。",
        "",
        "### 案例切片后续跟踪",
        "",
    ]
    if concept_rows:
        lines.extend(
            [
                "| 日期 | 技能点 | 案例切片 | 概念后最近结果 |",
                "|------|--------|---------|---------------|",
                *[
                    f"| {date_text} | {skill} | {slice_label} | {summary} |"
                    for date_text, skill, slice_label, summary in concept_rows
                ],
            ]
        )
    else:
        lines.append("*（暂无可跟踪的概念课后续结果）*")

    lines.extend(["", "### 资源使用后续跟踪", ""])
    if resource_rows:
        lines.extend(
            [
                "| 日期 | 技能点 | 资源 / 证据 / 图示 | 后续结果 |",
                "|------|--------|------------------|---------|",
                *[
                    f"| {date_text} | {skill} | {trace} | {outcome} |"
                    for date_text, skill, trace, outcome in resource_rows
                ],
            ]
        )
    else:
        lines.append("*（暂无资源段落 / 证据包 / 图示编号追踪）*")

    lines.extend(["", "### 题库题号效果", ""])
    if question_bank_rows:
        lines.extend(
            [
                "| 题库来源 / 题号 | 失误数 | 总题数 | 失误率 |",
                "|----------------|--------|--------|--------|",
                *[
                    f"| {source} | {misses} | {total} | {rate:.0%} |"
                    for source, misses, total, rate in question_bank_rows
                ],
            ]
        )
    else:
        lines.append("*（暂无题库题号追踪）*")

    lines.extend(["", "### 题型失误热度", ""])
    if question_rows:
        lines.extend(
            [
                "| 题型 | 失误数 | 总题数 | 失误率 |",
                "|------|--------|--------|--------|",
                *[
                    f"| {question_type} | {misses} | {total} | {rate:.0%} |"
                    for question_type, misses, total, rate in question_rows
                ],
            ]
        )
    else:
        lines.append("*（暂无题型统计）*")

    return "\n".join(lines)


def dominant_teaching_categories(
    session_entries: list[HomeworkEntry],
    all_entries: list[HomeworkEntry],
    skill_id: str | None,
    limit: int = 2,
) -> list[str]:
    candidate_groups = [
        scored_entries(session_entries),
        [
            entry
            for entry in scored_entries(all_entries)
            if skill_id and entry.skill_id == skill_id
        ],
        scored_entries(all_entries),
    ]
    for entries in candidate_groups:
        categories = [
            category
            for category, _ in ordered_weakness_items(weakness_counter(entries))
        ][:limit]
        if categories:
            return categories
    return []


def summarize_next_concept_follow_up(
    session_entries: list[HomeworkEntry],
    all_entries: list[HomeworkEntry],
    skill_id: str | None,
) -> str:
    categories = dominant_teaching_categories(session_entries, all_entries, skill_id)
    if not categories:
        return "待补充"
    return "；".join(
        f"{category}：{WEAKNESS_RECOMMENDATIONS[category]['concept'].rstrip('。；')}"
        for category in categories
    ) + "。"


def summarize_next_practice_bias(
    session_entries: list[HomeworkEntry],
    all_entries: list[HomeworkEntry],
    skill_id: str | None,
) -> str:
    categories = dominant_teaching_categories(session_entries, all_entries, skill_id)
    if not categories:
        return "待补充"
    return "；".join(
        f"{category}：{WEAKNESS_RECOMMENDATIONS[category]['practice'].rstrip('。；')}"
        for category in categories
    ) + "。"


def render_teaching_control_panel(entries: list[HomeworkEntry], today: date) -> str:
    practice_entries = scored_entries(entries)
    recent_error_entries, recent_error_scope_label = recent_error_scope_entries(entries, today)
    lines = [
        "> 由 `teacher/homework_log.md` 自动生成，用于指导盛言 / Shaw 的当前教学重点。",
        f"> 统计口径：全部有结果的练习/延迟验证/复习记录；高频错误默认看最近两周，若窗口为空则回退到最近 5 条有结果记录。",
        "",
    ]
    if not practice_entries:
        lines.append("*（暂无可用练习/复习数据）*")
        return "\n".join(lines)

    weakness_counts = weakness_counter(practice_entries)
    weakness_skills: dict[str, list[str]] = {}
    recent_error_counter: Counter[str] = Counter()

    for entry in practice_entries:
        categories = infer_weakness_categories(entry)
        for category in categories:
            weakness_skills.setdefault(category, []).append(entry.skill_id or "—")
    for entry in recent_error_entries:
        recent_error_counter.update(error_modes_for_entry(entry))

    top_categories = ordered_weakness_items(weakness_counts)[:3]

    lines.extend(
        [
            "### 当前前三大稳定弱点",
            "",
            "| 弱点簇 | 命中次数 | 最近涉及技能点 | 教学含义 |",
            "|-------|---------|---------------|---------|",
        ]
    )
    if not top_categories:
        lines.append("| （空） | — | — | 暂无可聚类的薄弱点。 |")
    else:
        for category, count in top_categories:
            recent_skills: list[str] = []
            seen_skills: set[str] = set()
            for skill_id in reversed(weakness_skills.get(category, [])):
                if skill_id in seen_skills:
                    continue
                seen_skills.add(skill_id)
                recent_skills.append(skill_id)
                if len(recent_skills) == 3:
                    break
            meaning = WEAKNESS_RECOMMENDATIONS[category]["meaning"]
            lines.append(
                f"| {category} | {count} | {', '.join(recent_skills) or '—'} | {meaning} |"
            )

    lines.extend(
        [
            "",
            "### 最近两周高频错误模式",
            "",
            f"> 当前使用：{recent_error_scope_label}",
            "",
            "| 错误模式 | 最近两周出现次数 |",
            "|---------|----------------|",
        ]
    )
    recent_modes = ordered_error_mode_items(recent_error_counter)
    if not recent_modes:
        lines.append("| （空） | 0 |")
    else:
        for mode, count in recent_modes:
            lines.append(f"| {mode} | {count} |")

    lines.extend(
        [
            "",
            "### 已触发的硬规则",
            "",
            "| 技能点 | 连续错误 | 下次会话强制动作 |",
            "|-------|---------|----------------|",
        ]
    )
    triggered_actions = latest_triggered_teaching_actions(practice_entries)
    if not triggered_actions:
        lines.append("| （空） | — | 当前没有命中的强制教学动作。 |")
    else:
        for skill_id in sorted(triggered_actions, key=lambda current_skill_id: int(current_skill_id.split("-")[1])):
            for trigger in triggered_actions[skill_id]:
                lines.append(
                    f"| {skill_id}：{trigger.skill_name} | {trigger.error_mode}（连续{trigger.streak}次） | {trigger.next_session}：{trigger.detail} |"
                )

    lines.extend(["", "### 概念课推荐追问方式", ""])
    if not top_categories:
        lines.append("- 暂无推荐，先继续积累练习数据。")
    else:
        for category, _ in top_categories:
            lines.append(
                f"- `{category}`：{WEAKNESS_RECOMMENDATIONS[category]['concept']}"
            )

    lines.extend(["", "### 练习课推荐题型偏置", ""])
    if not top_categories:
        lines.append("- 暂无推荐，先继续积累练习数据。")
    else:
        for category, _ in top_categories:
            lines.append(
                f"- `{category}`：{WEAKNESS_RECOMMENDATIONS[category]['practice']}"
            )

    return "\n".join(lines)


def render_operating_metrics(
    skills: list[Skill],
    entries: list[HomeworkEntry],
    today: date,
) -> str:
    window_start = today - timedelta(days=6)
    weekly_stable_mastery = sum(
        1
        for skill in skills
        if skill.review_anchor_date and window_start <= skill.review_anchor_date <= today
    )
    weekly_review_cleared = sum(
        1
        for entry in entries
        if entry.entry_date
        and window_start <= entry.entry_date <= today
        and "间隔复习" in entry.session_title
        and "复习完成" in entry.judgment
    )
    mastery_records = build_mastery_records(skills, entries)
    average_attempts = (
        sum(record.attempt_count for record in mastery_records) / len(mastery_records)
        if mastery_records
        else None
    )
    error_scope_entries, error_scope_label = recent_error_scope_entries(entries, today)
    repeated_hits, total_hits = error_repeat_rate(error_scope_entries)
    if total_hits:
        repeat_rate = f"{repeated_hits}/{total_hits}（{repeated_hits / total_hits:.0%}）"
    else:
        repeat_rate = "0/0（—）"

    return "\n".join(
        [
            f"> 周指标按 {format_date(window_start)} 至 {format_date(today)} 统计；错误重复率使用 {error_scope_label}。",
            "",
            "| 指标 | 数值 | 口径 |",
            "|------|------|------|",
            f"| 每周新增稳定掌握 | {weekly_stable_mastery} | 最近7天进入稳定掌握节奏的技能点数 |",
            f"| 每周消化复习债 | {weekly_review_cleared} | 最近7天完成的间隔复习次数 |",
            f"| 单技能平均首次达标次数 | {average_attempts:.1f} 次 | 已有掌握记录的首次达标平均练习次数 |" if average_attempts is not None else "| 单技能平均首次达标次数 | — | 暂无掌握记录 |",
            f"| 高频错误重复率 | {repeat_rate} | 重复出现的错误模式命中 / 总错误模式命中 |",
        ]
    )


def sync_learner_profile(text: str, entries: list[HomeworkEntry], today: date) -> str:
    synced = replace_section(
        text,
        "概念课表现记录",
        "教学控制面板",
        "\n".join(
            [
                "> 由 `teacher/homework_log.md` 中结构化的概念课记录自动生成。",
                "> 概念课日志应包含：案例 dossier / 案例切片 / 开场案例 / 已知 / 未知 / 当下判断 / 结果揭示 / 偏差复盘 / 复述检验。",
                "",
                render_concept_performance(entries),
            ]
        ),
    )
    synced = replace_section(
        synced,
        "教学控制面板",
        "练习课准确率趋势",
        render_teaching_control_panel(entries, today),
    )
    return replace_section(
        synced,
        "练习课准确率趋势",
        "盛言的当前评价",
        "\n".join(
            [
                "> 由 `teacher/homework_log.md` 自动生成。",
                "> 每次会话结束前运行：`python3 tools/learning_state.py sync`。",
                "",
                render_practice_trend(entries),
            ]
        ),
    )


def render_progress(skills: list[Skill], entries: list[HomeworkEntry], today: date) -> str:
    long_term_count = sum(skill.status.startswith("💚") for skill in skills)
    mastered_count = sum(
        skill.is_mastered and not skill.status.startswith("💚")
        for skill in skills
    )
    delayed_count = sum(skill.needs_delayed_validation for skill in skills)
    concept_done_count = sum(skill.status.startswith("🔵") for skill in skills)
    learning_count = sum(skill.status.startswith("🟡") for skill in skills)
    unlearned_count = sum(skill.status.startswith("⬜") for skill in skills)
    locked_count = sum(skill.status.startswith("🔒") for skill in skills)
    delayed_due_count = len(delayed_validation_due_skills(skills, today))
    due_count = len(review_due_skills(skills, today))
    skills_by_id = {skill.skill_id: skill for skill in skills}

    return "\n".join(
        [
            "# 学习进度（progress.md）",
            "",
            "> 本文件由 `teacher/skill_graph.md` 和 `teacher/homework_log.md` 自动生成。",
            f"> 当前系统日期：{today.isoformat()}。",
            "> `skill_graph.md` 的技能明细是唯一状态权威；本文件只做汇总展示。",
            "> 每次会话结束前运行：`python3 tools/learning_state.py sync`。",
            "",
            "---",
            "",
            "## 总体进度",
            "",
            "| 项目 | 数值 |",
            "|------|------|",
            f"| 总技能点 | {len(skills)} |",
            f"| 💚 长期掌握 | {long_term_count} |",
            f"| ✅ 稳定掌握（待复习） | {mastered_count} |",
            f"| 🧪 待延迟验证 | {delayed_count} |",
            f"| 🔵 概念已完成 | {concept_done_count} |",
            f"| 🟡 学习中 | {learning_count} |",
            f"| ⬜ 未学（可解锁） | {unlearned_count} |",
            f"| 🔒 未解锁 | {locked_count} |",
            f"| ⏳ 今日延迟验证到期 | {delayed_due_count} |",
            f"| 🔄 今日复习到期 | {due_count} |",
            "",
            "---",
            "",
            "## 今日调度策略",
            "",
            render_scheduling_policy(skills, today),
            "",
            "---",
            "",
            "## 双主线推进",
            "",
            render_dual_track_progress(skills, skills_by_id),
            "",
            "---",
            "",
            "## 运营指标",
            "",
            render_operating_metrics(skills, entries, today),
            "",
            "---",
            "",
            "## 内容效果指标",
            "",
            render_content_effectiveness_metrics(entries),
            "",
            "---",
            "",
            "## 当前活跃技能点",
            "",
            "（正在进行概念课或练习课的技能点）",
            "",
            render_active_skills(skills),
            "",
            "---",
            "",
            "## 已掌握技能点",
            "",
            render_mastered_skills(skills, today),
            "",
            "---",
            "",
            "## 近期练习记录（按日志顺序最近5条）",
            "",
            render_recent_entries(entries),
            "",
            "---",
            "",
            "## 今日延迟验证",
            "",
            "（即时通过后 24-72 小时内的短测，未通过前不视为稳定掌握）",
            "",
            render_delayed_validation_queue(skills, today).split("\n", 2)[2] if render_delayed_validation_queue(skills, today).count("\n") >= 2 else "*（空）*",
            "",
            "---",
            "",
            "## 今日到期复习",
            "",
            "（每次会话开场时优先处理）",
            "",
            render_due_queue(skills, today, entries).split("\n", 3)[3] if render_due_queue(skills, today, entries).count("\n") >= 3 else "*（空）*",
            "",
            "---",
            "",
            "## 里程碑记录",
            "",
            render_milestones(skills, entries),
            "",
        ]
    )


def render_skill_graph(skills: list[Skill], entries: list[HomeworkEntry], today: date) -> str:
    skills_by_id = {skill.skill_id: skill for skill in skills}
    ordered_skills = sorted(skills, key=lambda skill: skill.number)

    stage_sections: list[str] = []
    for start, end, title in STAGE_DEFINITIONS:
        stage_skills = [skill for skill in ordered_skills if start <= skill.number <= end]
        if not stage_skills:
            continue
        stage_sections.append(
            "\n\n---\n\n".join(
                [
                    f"## {title}（SK-{start:03d} ~ SK-{end:03d}）",
                    *[render_skill_block(skill) for skill in stage_skills],
                ]
            )
        )

    sections = [
        "\n".join(
            [
                "# 技能图谱（skill_graph.md）",
                "",
                "> 本文件的技能明细是系统唯一状态权威。",
                "> 概览、当前可学习技能、掌握记录、今日延迟验证、今日复习队列、间隔复习时间表由 `python3 tools/learning_state.py sync` 自动重建。",
                "> `概念课完成` 字段会结合 `homework_log.md` 与 `session_archive.md` 自动补齐重修日期。",
                "> `首次掌握日期` 与 `最近达标日期` 会结合 `homework_log.md` 自动校正。",
                "> `主要参考资源` 会按技能点自动映射到资源库中的核心材料。",
                "> 不要手动编辑状态字段，通过指令操作。",
            ]
        ),
        "## 概览\n\n" + render_overview(ordered_skills, today),
        "## 当前可学习的技能点\n\n" + render_learnable_section(ordered_skills, skills_by_id, today),
        "\n".join(
            [
                "## 技能点目录",
                "",
                '> 格式说明：每次练习课后，Claude Code 更新"状态"、"最后练习"、"历史准确率"、"复习到期"；掌握相关日期由日志自动回算；"主要参考资源" 按技能点自动映射。',
                "> 掌握标准：中强度，10题答对8题。",
            ]
        ),
        *stage_sections,
        "## 掌握记录（按时间）\n\n" + render_mastery_records(ordered_skills, entries),
        "## 今日延迟验证\n\n" + render_delayed_validation_queue(ordered_skills, today),
        "## 今日复习队列\n\n" + render_due_queue(ordered_skills, today, entries),
        "## 间隔复习时间表\n\n" + render_review_schedule(ordered_skills),
        "## 状态图例\n\n" + render_status_legend(),
    ]
    return "\n\n---\n\n".join(sections) + "\n"


def sync_skill_graph(
    skills: list[Skill],
    entries: list[HomeworkEntry],
    today: date,
    concept_events_by_skill: dict[str, list[ConceptEvent]],
) -> str:
    synced_skills = apply_concept_events(skills, concept_events_by_skill)
    return render_skill_graph(synced_skills, entries, today)


def validate_skills(
    skills: list[Skill],
    skills_by_id: dict[str, Skill],
    today: date,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if len(skills) != 57:
        errors.append(f"Expected 57 skill sections, found {len(skills)}.")

    seen_ids: set[str] = set()
    for skill in skills:
        if skill.skill_id in seen_ids:
            errors.append(f"Duplicate skill id found: {skill.skill_id}.")
        seen_ids.add(skill.skill_id)

        if skill.status_icon not in ALLOWED_STATUS_PREFIXES:
            errors.append(f"{skill.skill_id} has an unknown 状态 value: {skill.status}.")
            continue

        concept_dates = parse_all_iso_dates(skill.concept_completed)
        has_concept = skill.concept_completed != "—"
        has_first_mastery = skill.first_mastery_date is not None
        has_latest_mastery = skill.latest_mastery_date is not None
        has_delayed_due = skill.delayed_validation_due is not None
        has_delayed_pass = skill.delayed_validation_passed_date is not None
        if has_concept and not concept_dates:
            errors.append(f"{skill.skill_id} has a non-empty 概念课完成 field but no parseable date.")

        if skill.history_accuracies and not skill.last_practice:
            errors.append(f"{skill.skill_id} has 历史准确率 but is missing 最后练习.")
        if skill.last_practice and not skill.history_accuracies:
            warnings.append(f"{skill.skill_id} has 最后练习 but no 历史准确率 entries.")

        if concept_dates and skill.last_practice and skill.last_practice < max(concept_dates):
            errors.append(f"{skill.skill_id} has 最后练习 earlier than the latest 概念课完成 date.")
        if concept_dates and skill.latest_mastery_date and skill.latest_mastery_date < max(concept_dates):
            errors.append(f"{skill.skill_id} has 最近达标日期 earlier than the latest 概念课完成 date.")
        if has_first_mastery and has_latest_mastery and skill.latest_mastery_date < skill.first_mastery_date:
            errors.append(f"{skill.skill_id} has 最近达标日期 earlier than 首次掌握日期.")
        if has_delayed_due and has_delayed_pass:
            errors.append(f"{skill.skill_id} has both 延迟验证到期 and 延迟验证通过日期 populated.")
        if has_delayed_pass and has_latest_mastery and skill.delayed_validation_passed_date < skill.latest_mastery_date:
            errors.append(f"{skill.skill_id} has 延迟验证通过日期 earlier than 最近达标日期.")
        if has_delayed_due and has_latest_mastery and skill.delayed_validation_due <= skill.latest_mastery_date:
            errors.append(f"{skill.skill_id} has 延迟验证到期 that is not later than 最近达标日期.")
        if skill.latest_mastery_date and skill.last_practice and skill.last_practice < skill.latest_mastery_date:
            warnings.append(f"{skill.skill_id} has 最后练习 earlier than 最近达标日期.")

        prereqs_met = all(skills_by_id[prereq].is_mastered for prereq in skill.prereqs)
        if skill.status.startswith("🔒") and prereqs_met:
            errors.append(f"{skill.skill_id} is locked but all prerequisites are mastered.")
        if not skill.status.startswith("🔒") and skill.prereqs and not prereqs_met:
            errors.append(f"{skill.skill_id} is unlocked but prerequisites are not all mastered.")

        if skill.status.startswith("🔒"):
            if has_concept or has_first_mastery or has_latest_mastery or has_delayed_due or has_delayed_pass or skill.last_practice or skill.history_accuracies or skill.review_due:
                errors.append(f"{skill.skill_id} is 未解锁 but has learning history fields populated.")
            if skill.review_round != 0:
                errors.append(f"{skill.skill_id} is 未解锁 but 复习轮次 is not 0.")

        elif skill.status.startswith("⬜"):
            if has_concept or has_first_mastery or has_latest_mastery or has_delayed_due or has_delayed_pass or skill.last_practice or skill.history_accuracies or skill.review_due:
                errors.append(f"{skill.skill_id} is 未学 but has downstream learning fields populated.")
            if skill.review_round != 0:
                errors.append(f"{skill.skill_id} is 未学 but 复习轮次 is not 0.")

        elif skill.status.startswith("🔵"):
            if not has_concept:
                errors.append(f"{skill.skill_id} is 概念已完成 but missing 概念课完成.")
            if has_first_mastery or has_latest_mastery or has_delayed_due or has_delayed_pass or skill.review_due:
                errors.append(f"{skill.skill_id} is 概念已完成 but has mastered/review fields populated.")
            if skill.last_practice or skill.history_accuracies:
                errors.append(f"{skill.skill_id} is 概念已完成 but has practice history.")

        elif skill.status.startswith("🟡"):
            if not has_concept:
                errors.append(f"{skill.skill_id} is 学习中 but missing 概念课完成.")
            if not skill.last_practice or not skill.history_accuracies:
                errors.append(f"{skill.skill_id} is 学习中 but is missing practice history.")
            if skill.review_due:
                errors.append(f"{skill.skill_id} is 学习中 but has 复习到期 populated.")
            if has_delayed_due:
                errors.append(f"{skill.skill_id} is 学习中 but has 延迟验证到期 populated.")
            if has_latest_mastery and not has_first_mastery:
                errors.append(f"{skill.skill_id} is 学习中 and has 最近达标日期 but missing 首次掌握日期.")

        elif skill.status.startswith("✅"):
            if not has_concept:
                errors.append(f"{skill.skill_id} is 已掌握 but missing 概念课完成.")
            if not has_first_mastery:
                errors.append(f"{skill.skill_id} is 已掌握 but missing 首次掌握日期.")
            if not has_latest_mastery:
                errors.append(f"{skill.skill_id} is 已掌握 but missing 最近达标日期.")
            if not skill.last_practice or not skill.history_accuracies:
                errors.append(f"{skill.skill_id} is 已掌握 but practice history is incomplete.")
            if skill.needs_delayed_validation:
                if not has_delayed_due:
                    errors.append(f"{skill.skill_id} is 待延迟验证 but missing 延迟验证到期.")
                if has_delayed_pass:
                    errors.append(f"{skill.skill_id} is 待延迟验证 but already has 延迟验证通过日期.")
                if skill.review_due:
                    errors.append(f"{skill.skill_id} is 待延迟验证 but already has 复习到期.")
            else:
                if not has_delayed_pass:
                    errors.append(f"{skill.skill_id} is 已掌握 but missing 延迟验证通过日期.")
                if not skill.review_due:
                    errors.append(f"{skill.skill_id} is 已掌握 but missing 复习到期.")

        elif skill.status.startswith("🔄"):
            if not has_concept or not has_first_mastery or not has_latest_mastery or not has_delayed_pass or not skill.last_practice or not skill.history_accuracies:
                errors.append(f"{skill.skill_id} is 复习到期 but mastery/practice fields are incomplete.")
            if not skill.review_due:
                errors.append(f"{skill.skill_id} is 复习到期 but missing 复习到期.")
            elif skill.review_due > today:
                errors.append(f"{skill.skill_id} is marked 复习到期 but 复习到期 is later than today.")

        elif skill.status.startswith("💚"):
            if not has_concept or not has_first_mastery or not has_latest_mastery or not has_delayed_pass or not skill.last_practice or not skill.history_accuracies:
                errors.append(f"{skill.skill_id} is 长期掌握 but mastery/practice fields are incomplete.")
            if not skill.review_due:
                errors.append(f"{skill.skill_id} is 长期掌握 but missing 复习到期.")
            if skill.review_round < 3:
                errors.append(f"{skill.skill_id} is 长期掌握 but 复习轮次 is below 3.")

        if skill.is_mastered and skill.review_round < 0:
            errors.append(f"{skill.skill_id} has a negative 复习轮次.")
        if skill.review_due and not skill.is_mastered:
            errors.append(f"{skill.skill_id} has a 复习到期 date but is not in a mastered state.")

    return errors, warnings


def validate_skill_history_against_log(
    skills: list[Skill],
    entries: list[HomeworkEntry],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    latest_accuracy_entry_by_skill: dict[str, HomeworkEntry] = {}
    first_mastery_entry_by_skill: dict[str, HomeworkEntry] = {}
    latest_mastery_entry_by_skill: dict[str, HomeworkEntry] = {}
    for entry in entries:
        if not entry.skill_id:
            continue
        if entry.accuracy != "—":
            latest_accuracy_entry_by_skill[entry.skill_id] = entry
        if (
            "间隔复习" not in entry.session_title
            and "复习课" not in entry.session_title
            and "延迟验证" not in entry.session_title
            and "✅" in entry.judgment
            and "掌握" in entry.judgment
        ):
            first_mastery_entry_by_skill.setdefault(entry.skill_id, entry)
            latest_mastery_entry_by_skill[entry.skill_id] = entry

    for skill in skills:
        latest_accuracy_entry = latest_accuracy_entry_by_skill.get(skill.skill_id)
        if latest_accuracy_entry:
            if skill.last_practice != latest_accuracy_entry.entry_date:
                errors.append(
                    f"{skill.skill_id} has 最后练习 {format_date(skill.last_practice)} but the latest log entry is {format_date(latest_accuracy_entry.entry_date)}."
                )
            if skill.history_accuracies:
                latest_logged_accuracy = short_accuracy(latest_accuracy_entry.accuracy)
                if skill.history_accuracies[-1] != latest_logged_accuracy:
                    errors.append(
                        f"{skill.skill_id} has 历史准确率 tail {skill.history_accuracies[-1]} but the latest log entry is {latest_logged_accuracy}."
                    )
            elif skill.last_practice:
                warnings.append(
                    f"{skill.skill_id} has 最后练习 but no 历史准确率, while homework_log.md has accuracy-bearing entries."
                )
        elif skill.last_practice or skill.history_accuracies:
            warnings.append(
                f"{skill.skill_id} has practice history fields populated but no matching accuracy-bearing entry in homework_log.md."
            )

        first_mastery_entry = first_mastery_entry_by_skill.get(skill.skill_id)
        if skill.first_mastery_date and first_mastery_entry and skill.first_mastery_date != first_mastery_entry.entry_date:
            errors.append(
                f"{skill.skill_id} has 首次掌握日期 {format_date(skill.first_mastery_date)} but the first mastery log entry is {format_date(first_mastery_entry.entry_date)}."
            )

        latest_mastery_entry = latest_mastery_entry_by_skill.get(skill.skill_id)
        if skill.latest_mastery_date and latest_mastery_entry and skill.latest_mastery_date != latest_mastery_entry.entry_date:
            errors.append(
                f"{skill.skill_id} has 最近达标日期 {format_date(skill.latest_mastery_date)} but the latest mastery log entry is {format_date(latest_mastery_entry.entry_date)}."
            )

    return errors, warnings


def validate_homework_log(entries: list[HomeworkEntry]) -> list[str]:
    warnings: list[str] = []
    previous_date: date | None = None
    for entry in entries:
        if not entry.entry_date:
            continue
        if previous_date and entry.entry_date < previous_date:
            warnings.append(
                "homework_log.md is not append-only by date order; recent-entry summaries use file order."
            )
            break
        previous_date = entry.entry_date

    for entry in entries:
        if "概念" not in entry.session_title:
            continue
        concept_slice = extract_concept_slice(entry)
        missing = [
            field for field in CONCEPT_SLICE_FIELDS
            if field not in concept_slice
        ]
        if missing:
            warnings.append(
                f"concept entry '{entry.session_title}' is missing structured fields: {', '.join(missing)}."
            )
    return warnings


def validate_homework_structure(text: str) -> list[str]:
    warnings: list[str] = []
    if "概念课" in text and "每次练习课结束后，追加以下格式：" in text:
        warnings.append(
            "homework_log.md records concept/review events too; update the format note so writers do not treat it as practice-only."
        )
    if "概念课（或概念重修）建议使用如下结构" not in text:
        warnings.append(
            "homework_log.md should document the structured concept-session fields (案例 dossier/案例切片/资源段落/证据包条目/图示编号/已知/未知/当下判断/结果揭示/偏差复盘/复述检验)."
        )
    if "题库题号" not in text or "题库来源" not in text:
        warnings.append(
            "homework_log.md should document practice resource trace fields (题库题号/题库来源/使用资源段落/使用图示)."
        )
    return warnings


def validate_session_archive_structure(text: str) -> list[str]:
    warnings: list[str] = []
    if "最近3条记录" in text and "文件底部最后3条" not in text:
        warnings.append(
            "session_archive.md should state that recency is determined by the last 3 entries in file order."
        )
    return warnings


def validate_session_archive_entries(entries: list[ArchiveEntry]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required_fields = ("技能点", "状态变化", "本节核心", "盛言的评注", "遗留问题")
    optional_fields = {
        "薄弱点",
        "Root 错题解析要点",
        "案例 dossier",
        "案例切片",
        "资源段落",
        "证据包条目",
        "图示编号",
        "下次会话强制动作",
        "下次概念课建议追问",
        "下次练习课建议题型",
    }

    for entry in entries:
        missing = [field for field in required_fields if field not in entry.fields]
        if missing:
            errors.append(
                f"session_archive entry '{entry.header}' is missing required fields: {', '.join(missing)}."
            )

        unknown_fields = [field for field in entry.fields if field not in {*required_fields, *optional_fields}]
        if unknown_fields:
            warnings.append(
                f"session_archive entry '{entry.header}' has non-standard fields: {', '.join(unknown_fields)}."
            )

        if "技能点" in entry.fields and not entry.skill_id:
            errors.append(
                f"session_archive entry '{entry.header}' has an unparsable 技能点 field."
            )

    return errors, warnings


def write_if_changed(path: Path, content: str) -> bool:
    normalized = content.rstrip() + "\n"
    current = path.read_text() if path.exists() else None
    if current == normalized:
        return False
    path.write_text(normalized)
    return True


def normalized_text(content: str) -> str:
    return content.rstrip() + "\n"


def collect_changed_outputs(outputs: dict[Path, str]) -> dict[Path, str]:
    changed: dict[Path, str] = {}
    for path, content in outputs.items():
        normalized = normalized_text(content)
        current = path.read_text() if path.exists() else None
        if current != normalized:
            changed[path] = normalized
    return changed


def relative_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def build_unified_diff(path: Path, current: str | None, desired: str) -> str:
    before_lines = (current or "").splitlines()
    after_lines = desired.splitlines()
    return "\n".join(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile=f"a/{relative_display_path(path)}",
            tofile=f"b/{relative_display_path(path)}",
            lineterm="",
        )
    )


def emit_changed_output_diffs(changed_outputs: dict[Path, str]) -> None:
    for path, desired in changed_outputs.items():
        current = path.read_text() if path.exists() else None
        diff = build_unified_diff(path, current, desired)
        if diff:
            print(diff)


def write_backup_snapshot(
    changed_outputs: dict[Path, str],
    backup_root: Path = BACKUP_ROOT,
) -> Path | None:
    existing_contents = {
        path: path.read_text()
        for path in changed_outputs
        if path.exists()
    }
    if not existing_contents:
        return None

    backup_dir = backup_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    for path, content in existing_contents.items():
        try:
            relative_path = path.relative_to(ROOT)
        except ValueError:
            relative_path = Path(path.name)
        destination = backup_dir / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content)
    return backup_dir


def validate_generated_freshness(
    texts: dict[Path, str],
    today: date,
) -> list[str]:
    errors: list[str] = []
    for path, text in texts.items():
        dates = {
            date.fromisoformat(match)
            for match in re.findall(r"当前系统日期(?:\*\*)?\s*[：:]\s*(\d{4}-\d{2}-\d{2})", text)
        }
        stale_dates = sorted(value for value in dates if value != today)
        if stale_dates:
            stale_text = "、".join(value.isoformat() for value in stale_dates)
            errors.append(
                f"{relative_display_path(path)} has stale 当前系统日期 {stale_text}; expected {today.isoformat()}."
            )
    return errors


def main() -> int:
    args = parse_args()
    today = date.fromisoformat(args.today) if args.today else date.today()

    skill_graph_text = SKILL_GRAPH_PATH.read_text()
    homework_log_text = HOMEWORK_LOG_PATH.read_text()
    session_archive_text = SESSION_ARCHIVE_PATH.read_text()
    archive_drafts_text = (
        SESSION_ARCHIVE_DRAFTS_PATH.read_text()
        if SESSION_ARCHIVE_DRAFTS_PATH.exists()
        else ""
    )
    learner_profile_text = LEARNER_PROFILE_PATH.read_text()
    normalized_homework_log = normalize_homework_log(homework_log_text)
    normalized_session_archive = normalize_session_archive(session_archive_text)
    promoted_headers: list[str] = []
    if args.command == "promote-archive-drafts":
        draft_entries = parse_session_archive_entries(
            normalize_session_archive(archive_drafts_text)
        )
        draft_errors, draft_warnings = validate_session_archive_entries(draft_entries)
        if draft_errors:
            for error in draft_errors:
                print(f"ERROR: archive draft cannot be promoted: {error}")
            return 1
        for warning in draft_warnings:
            print(f"WARNING: archive draft before promotion: {warning}")
        normalized_session_archive, promoted_headers = promote_archive_drafts(
            normalized_session_archive,
            archive_drafts_text,
        )

    skills = parse_skill_graph(skill_graph_text)
    homework_entries = parse_homework_log(normalized_homework_log)
    archive_entries = parse_session_archive_entries(normalized_session_archive)
    mastery_snapshots = collect_mastery_snapshots(homework_entries)
    skills = apply_mastery_snapshots(skills, mastery_snapshots)
    delayed_validation_snapshots = collect_delayed_validation_snapshots(homework_entries)
    skills = apply_delayed_validation_snapshots(skills, delayed_validation_snapshots)
    skills_by_id = {skill.skill_id: skill for skill in skills}
    concept_events_by_skill = collect_concept_events(skills, homework_entries, archive_entries)

    skill_errors, skill_warnings = validate_skills(skills, skills_by_id, today)
    skill_history_errors, skill_history_warnings = validate_skill_history_against_log(skills, homework_entries)
    log_warnings = validate_homework_log(homework_entries)
    structure_warnings = validate_homework_structure(homework_log_text)
    archive_warnings = validate_session_archive_structure(session_archive_text)
    archive_errors, archive_entry_warnings = validate_session_archive_entries(archive_entries)
    warnings = [
        *skill_warnings,
        *skill_history_warnings,
        *log_warnings,
        *structure_warnings,
        *archive_warnings,
        *archive_entry_warnings,
    ]

    synced_skill_graph = sync_skill_graph(skills, homework_entries, today, concept_events_by_skill)
    rendered_progress = render_progress(skills, homework_entries, today)
    synced_learner_profile = sync_learner_profile(
        learner_profile_text,
        homework_entries,
        today,
    )
    rendered_session_briefing = render_session_briefing(
        skills,
        homework_entries,
        archive_entries,
        today,
    )
    rendered_archive_drafts = render_session_archive_drafts(homework_entries, archive_entries)
    current_archive_drafts = archive_drafts_text
    current_session_briefing = (
        SESSION_BRIEFING_PATH.read_text()
        if SESSION_BRIEFING_PATH.exists()
        else ""
    )
    desired_outputs = {
        HOMEWORK_LOG_PATH: normalized_homework_log,
        SESSION_ARCHIVE_PATH: normalized_session_archive,
        SESSION_ARCHIVE_DRAFTS_PATH: rendered_archive_drafts,
        SESSION_BRIEFING_PATH: rendered_session_briefing,
        LEARNER_PROFILE_PATH: synced_learner_profile,
        SKILL_GRAPH_PATH: synced_skill_graph,
        PROGRESS_PATH: rendered_progress,
    }
    changed_outputs = collect_changed_outputs(desired_outputs)

    if args.command == "check":
        errors = [*skill_errors, *skill_history_errors, *archive_errors]
        errors.extend(
            validate_generated_freshness(
                {
                    SKILL_GRAPH_PATH: skill_graph_text,
                    PROGRESS_PATH: PROGRESS_PATH.read_text(),
                    SESSION_BRIEFING_PATH: current_session_briefing,
                },
                today,
            )
        )
        if synced_skill_graph.rstrip() + "\n" != skill_graph_text:
            errors.append("teacher/skill_graph.md generated sections are out of sync.")
        if rendered_progress.rstrip() + "\n" != PROGRESS_PATH.read_text():
            errors.append("teacher/progress.md is out of sync with the source data.")
        if normalized_homework_log.rstrip() + "\n" != homework_log_text:
            errors.append("teacher/homework_log.md is out of normalized chronological order.")
        if normalized_session_archive.rstrip() + "\n" != session_archive_text:
            errors.append("teacher/session_archive.md is out of normalized chronological order.")
        if synced_learner_profile.rstrip() + "\n" != learner_profile_text:
            errors.append(
                "teacher/learner_profile.md is out of sync with teaching-control-panel or practice-trend data."
            )
        if rendered_session_briefing.rstrip() + "\n" != current_session_briefing:
            errors.append("teacher/session_briefing.md is out of sync with current scheduling guidance.")
        if rendered_archive_drafts.rstrip() + "\n" != current_archive_drafts:
            errors.append("teacher/session_archive_drafts.md is out of sync with archive draft data.")

        if args.diff and changed_outputs:
            emit_changed_output_diffs(changed_outputs)
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        return 1 if errors else 0

    if args.diff and changed_outputs:
        emit_changed_output_diffs(changed_outputs)

    backup_dir: Path | None = None
    if args.backup:
        backup_dir = write_backup_snapshot(changed_outputs)

    changed_files: list[str] = []
    if write_if_changed(HOMEWORK_LOG_PATH, normalized_homework_log):
        changed_files.append(str(HOMEWORK_LOG_PATH.relative_to(ROOT)))
    if write_if_changed(SESSION_ARCHIVE_PATH, normalized_session_archive):
        changed_files.append(str(SESSION_ARCHIVE_PATH.relative_to(ROOT)))
    if write_if_changed(SESSION_ARCHIVE_DRAFTS_PATH, rendered_archive_drafts):
        changed_files.append(str(SESSION_ARCHIVE_DRAFTS_PATH.relative_to(ROOT)))
    if write_if_changed(SESSION_BRIEFING_PATH, rendered_session_briefing):
        changed_files.append(str(SESSION_BRIEFING_PATH.relative_to(ROOT)))
    if write_if_changed(LEARNER_PROFILE_PATH, synced_learner_profile):
        changed_files.append(str(LEARNER_PROFILE_PATH.relative_to(ROOT)))
    if write_if_changed(SKILL_GRAPH_PATH, synced_skill_graph):
        changed_files.append(str(SKILL_GRAPH_PATH.relative_to(ROOT)))
    if write_if_changed(PROGRESS_PATH, rendered_progress):
        changed_files.append(str(PROGRESS_PATH.relative_to(ROOT)))

    for warning in warnings:
        print(f"WARNING: {warning}")

    if args.command == "promote-archive-drafts":
        if promoted_headers:
            print("Promoted archive drafts:")
            for header in promoted_headers:
                print(f"  - {header}")
        else:
            print("No archive drafts were eligible for promotion.")

    if backup_dir:
        print(f"Backup snapshot: {relative_display_path(backup_dir)}")

    if changed_files:
        print("Updated:")
        for changed_file in changed_files:
            print(f"  - {changed_file}")
    else:
        print("No generated files changed.")

    combined_errors = [*skill_errors, *skill_history_errors, *archive_errors]
    if combined_errors:
        for error in combined_errors:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
