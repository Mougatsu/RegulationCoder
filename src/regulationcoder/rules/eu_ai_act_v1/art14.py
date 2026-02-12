"""Article 14 - Human Oversight.

High-risk AI systems shall be designed and developed in such a way as to be
effectively overseen by natural persons during the period in which they are
in use, including with appropriate human-machine interface tools.
"""

from regulationcoder.models.citation import Citation
from regulationcoder.models.clause import Clause
from regulationcoder.models.requirement import Condition, Modality, Requirement
from regulationcoder.models.rule import Rule, RuleType, Severity, TestCase

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_REG_ID = "eu-ai-act-v1"
_DOC_VERSION = "2024-1689-oj"
_ART = 14

def _cid(para: int, sub: str | None = None) -> str:
    base = f"{_REG_ID}/art{_ART:02d}/para{para}"
    return f"{base}/sub-{sub}" if sub else base

def _cite(para: int, sub: str | None = None, quote: str = "") -> Citation:
    return Citation(
        clause_id=_cid(para, sub),
        article_ref=f"Article {_ART}",
        paragraph_ref=str(para),
        subsection_ref=sub,
        exact_quote=quote,
    )

# ---------------------------------------------------------------------------
# Clauses
# ---------------------------------------------------------------------------
CLAUSES: list[Clause] = [
    Clause(
        id=_cid(1),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=1,
        text=(
            "High-risk AI systems shall be designed and developed in such a way, "
            "including with appropriate human-machine interface tools, as to be "
            "effectively overseen by natural persons during the period in which "
            "they are in use."
        ),
    ),
    Clause(
        id=_cid(2),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        text=(
            "Human oversight shall aim at minimising the risks to health, safety "
            "or fundamental rights that may emerge when a high-risk AI system is "
            "used in accordance with its intended purpose or under conditions of "
            "reasonably foreseeable misuse."
        ),
    ),
    Clause(
        id=_cid(4, "a"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        subsection_letter="a",
        text=(
            "The measures referred to in paragraph 1 shall enable the individuals "
            "to whom human oversight is assigned to fully understand the capacities "
            "and limitations of the high-risk AI system and be able to duly monitor "
            "its operation."
        ),
    ),
    Clause(
        id=_cid(4, "b"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        subsection_letter="b",
        text=(
            "The measures shall enable the individuals to remain aware of the "
            "possible tendency of automatically relying or over-relying on the "
            "output produced by a high-risk AI system (automation bias), in "
            "particular for high-risk AI systems used to provide information or "
            "recommendations for decisions to be taken by natural persons."
        ),
    ),
    Clause(
        id=_cid(4, "c"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        subsection_letter="c",
        text=(
            "The measures shall enable the individuals to be able to correctly "
            "interpret the high-risk AI system's output, taking into account, for "
            "example, the interpretation tools and methods available."
        ),
    ),
    Clause(
        id=_cid(4, "d"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        subsection_letter="d",
        text=(
            "The measures shall enable the individuals to be able to decide, in "
            "any particular situation, not to use the high-risk AI system or to "
            "otherwise disregard, override or reverse the output of the high-risk "
            "AI system."
        ),
    ),
    Clause(
        id=_cid(4, "e"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        subsection_letter="e",
        text=(
            "The measures shall enable the individuals to be able to intervene in "
            "the operation of the high-risk AI system or interrupt the system "
            "through a 'stop' button or a similar procedure that allows the system "
            "to come to a halt in a safe state."
        ),
    ),
    Clause(
        id=_cid(5),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=5,
        text=(
            "For the purpose of paragraph 1, the high-risk AI system shall be "
            "provided to the deployer in such a way that natural persons to whom "
            "human oversight is assigned are enabled, as appropriate and proportionate "
            "to the risks, to properly monitor the system in use."
        ),
    ),
]

# ---------------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------------
REQUIREMENTS: list[Requirement] = [
    Requirement(
        id="REQ-EU-AI-ACT-014-01-001",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="design system to be effectively overseen by natural persons during use",
        object="human oversight capability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(1, quote="effectively overseen by natural persons during the period in which they are in use")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-014-02-001",
        clause_id=_cid(2),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure human oversight minimises risks to health, safety and fundamental rights",
        object="risk minimisation through oversight",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(2, quote="minimising the risks to health, safety or fundamental rights")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-014-04A-001",
        clause_id=_cid(4, "a"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="enable oversight personnel to understand system capacities and limitations",
        object="oversight understanding capability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(4, "a", quote="fully understand the capacities and limitations")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-014-04B-001",
        clause_id=_cid(4, "b"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="implement safeguards against automation bias",
        object="automation bias safeguards",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(4, "b", quote="possible tendency of automatically relying or over-relying on the output (automation bias)")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-014-04C-001",
        clause_id=_cid(4, "c"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="enable correct interpretation of system output",
        object="output interpretation capability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(4, "c", quote="correctly interpret the high-risk AI system's output")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-014-04D-001",
        clause_id=_cid(4, "d"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="enable humans to override, reverse or disregard AI system output",
        object="human override capability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(4, "d", quote="disregard, override or reverse the output")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-014-04E-001",
        clause_id=_cid(4, "e"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="enable humans to interrupt system operation safely",
        object="system interruption capability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(4, "e", quote="interrupt the system through a 'stop' button or a similar procedure")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-014-05-001",
        clause_id=_cid(5),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="provide system so that oversight personnel can properly monitor it",
        object="monitoring enablement",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(5, quote="natural persons to whom human oversight is assigned are enabled to properly monitor")],
    ),
]

# ---------------------------------------------------------------------------
# Rules & evaluation functions
# ---------------------------------------------------------------------------

def _eval_oversight_measures(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    measures = profile.get("human_oversight_measures", [])
    return "pass" if len(measures) >= 1 else "fail"

def _eval_oversight_risk_min(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    measures = profile.get("human_oversight_measures", [])
    return "pass" if len(measures) >= 2 else "fail"

def _eval_understand_capabilities(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    has_limits = profile.get("limitations_documented", False)
    has_instructions = profile.get("instructions_for_use_provided", False)
    return "pass" if has_limits and has_instructions else "fail"

def _eval_automation_bias(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    safeguards = profile.get("automation_bias_safeguards", [])
    return "pass" if len(safeguards) >= 1 else "fail"

def _eval_output_interpretation(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("output_interpretation_tools", False) else "fail"

def _eval_human_override(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("human_can_override", False) else "fail"

def _eval_human_interrupt(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("human_can_interrupt", False) else "fail"

def _eval_monitoring_enabled(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    measures = profile.get("human_oversight_measures", [])
    has_monitoring = any("monitor" in m.lower() for m in measures)
    return "pass" if has_monitoring else "fail"


RULES: list[Rule] = [
    Rule(
        id="RULE-EU-AI-ACT-014-01-001",
        requirement_id="REQ-EU-AI-ACT-014-01-001",
        rule_type=RuleType.AUTOMATED,
        title="Human oversight measures must be implemented",
        description="Verify that the system is designed with human oversight measures for natural persons.",
        inputs_needed=["is_high_risk", "human_oversight_measures"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif len(measures)>=1: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Implement human oversight measures including human-machine interface tools.",
        test_cases=[
            TestCase(id="TC-014-01-P", description="Oversight exists", input_data={"is_high_risk": True, "human_oversight_measures": ["manual review"]}, expected_result="pass"),
            TestCase(id="TC-014-01-F", description="No oversight", input_data={"is_high_risk": True, "human_oversight_measures": []}, expected_result="fail"),
        ],
        citations=[_cite(1, quote="effectively overseen by natural persons")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-014-02-001",
        requirement_id="REQ-EU-AI-ACT-014-02-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Oversight must minimise risks effectively",
        description="Verify that human oversight measures are sufficient to minimise risks to health, safety and fundamental rights.",
        inputs_needed=["is_high_risk", "human_oversight_measures"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif len(measures)>=2: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Implement multiple oversight measures that specifically target identified risks.",
        test_cases=[
            TestCase(id="TC-014-02-P", description="Multiple measures", input_data={"is_high_risk": True, "human_oversight_measures": ["review", "approval"]}, expected_result="pass"),
            TestCase(id="TC-014-02-F", description="Insufficient measures", input_data={"is_high_risk": True, "human_oversight_measures": ["review"]}, expected_result="fail"),
        ],
        citations=[_cite(2, quote="minimising the risks to health, safety or fundamental rights")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-014-04A-001",
        requirement_id="REQ-EU-AI-ACT-014-04A-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Oversight personnel must understand system capabilities and limitations",
        description="Verify that oversight measures enable understanding of system capacities and limitations.",
        inputs_needed=["is_high_risk", "limitations_documented", "instructions_for_use_provided"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif both: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Ensure limitations are documented and instructions for use are provided to oversight personnel.",
        test_cases=[
            TestCase(id="TC-014-4A-P", description="Understanding enabled", input_data={"is_high_risk": True, "limitations_documented": True, "instructions_for_use_provided": True}, expected_result="pass"),
            TestCase(id="TC-014-4A-F", description="No limitation docs", input_data={"is_high_risk": True, "limitations_documented": False, "instructions_for_use_provided": True}, expected_result="fail"),
        ],
        citations=[_cite(4, "a", quote="fully understand the capacities and limitations")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-014-04B-001",
        requirement_id="REQ-EU-AI-ACT-014-04B-001",
        rule_type=RuleType.AUTOMATED,
        title="Automation bias safeguards must be implemented",
        description="Verify that safeguards against automation bias are implemented, especially for decision-support systems.",
        inputs_needed=["is_high_risk", "automation_bias_safeguards"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif len(safeguards)>=1: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Implement automation bias safeguards such as mandatory confirmation steps, uncertainty indicators, or periodic human-only reviews.",
        test_cases=[
            TestCase(id="TC-014-4B-P", description="Safeguards exist", input_data={"is_high_risk": True, "automation_bias_safeguards": ["confirmation step"]}, expected_result="pass"),
            TestCase(id="TC-014-4B-F", description="No safeguards", input_data={"is_high_risk": True, "automation_bias_safeguards": []}, expected_result="fail"),
        ],
        citations=[_cite(4, "b", quote="automation bias")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-014-04C-001",
        requirement_id="REQ-EU-AI-ACT-014-04C-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Output interpretation tools must be available",
        description="Verify that tools and methods for correct interpretation of system output are available.",
        inputs_needed=["is_high_risk", "extra.output_interpretation_tools"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif tools: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Provide interpretation tools such as confidence scores, feature importance, or SHAP values.",
        test_cases=[
            TestCase(id="TC-014-4C-P", description="Tools available", input_data={"is_high_risk": True, "extra": {"output_interpretation_tools": True}}, expected_result="pass"),
            TestCase(id="TC-014-4C-F", description="No tools", input_data={"is_high_risk": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(4, "c", quote="correctly interpret the high-risk AI system's output")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-014-04D-001",
        requirement_id="REQ-EU-AI-ACT-014-04D-001",
        rule_type=RuleType.AUTOMATED,
        title="Human override capability must be available",
        description="Verify that humans can override, reverse or disregard the AI system's output.",
        inputs_needed=["is_high_risk", "human_can_override"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif human_can_override: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Implement mechanisms allowing human operators to override or reverse AI decisions.",
        test_cases=[
            TestCase(id="TC-014-4D-P", description="Override available", input_data={"is_high_risk": True, "human_can_override": True}, expected_result="pass"),
            TestCase(id="TC-014-4D-F", description="No override", input_data={"is_high_risk": True, "human_can_override": False}, expected_result="fail"),
        ],
        citations=[_cite(4, "d", quote="override or reverse the output")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-014-04E-001",
        requirement_id="REQ-EU-AI-ACT-014-04E-001",
        rule_type=RuleType.AUTOMATED,
        title="System interruption capability must be available",
        description="Verify that humans can interrupt or stop the AI system safely.",
        inputs_needed=["is_high_risk", "human_can_interrupt"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif human_can_interrupt: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Implement a 'stop' button or similar procedure that allows the system to halt safely.",
        test_cases=[
            TestCase(id="TC-014-4E-P", description="Interrupt available", input_data={"is_high_risk": True, "human_can_interrupt": True}, expected_result="pass"),
            TestCase(id="TC-014-4E-F", description="No interrupt", input_data={"is_high_risk": True, "human_can_interrupt": False}, expected_result="fail"),
        ],
        citations=[_cite(4, "e", quote="interrupt the system through a 'stop' button")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-014-05-001",
        requirement_id="REQ-EU-AI-ACT-014-05-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Oversight personnel must be able to monitor system in use",
        description="Verify that the system is provided to deployers in a way that enables proper monitoring.",
        inputs_needed=["is_high_risk", "human_oversight_measures"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif monitoring in measures: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Provide monitoring dashboards or tools that enable oversight personnel to monitor system operation in real-time.",
        test_cases=[
            TestCase(id="TC-014-05-P", description="Monitoring enabled", input_data={"is_high_risk": True, "human_oversight_measures": ["real-time monitoring dashboard"]}, expected_result="pass"),
            TestCase(id="TC-014-05-F", description="No monitoring", input_data={"is_high_risk": True, "human_oversight_measures": ["approval gate"]}, expected_result="fail"),
        ],
        citations=[_cite(5, quote="enabled to properly monitor the system in use")],
    ),
]

EVALUATION_FUNCTIONS: dict[str, callable] = {
    "RULE-EU-AI-ACT-014-01-001": _eval_oversight_measures,
    "RULE-EU-AI-ACT-014-02-001": _eval_oversight_risk_min,
    "RULE-EU-AI-ACT-014-04A-001": _eval_understand_capabilities,
    "RULE-EU-AI-ACT-014-04B-001": _eval_automation_bias,
    "RULE-EU-AI-ACT-014-04C-001": _eval_output_interpretation,
    "RULE-EU-AI-ACT-014-04D-001": _eval_human_override,
    "RULE-EU-AI-ACT-014-04E-001": _eval_human_interrupt,
    "RULE-EU-AI-ACT-014-05-001": _eval_monitoring_enabled,
}
