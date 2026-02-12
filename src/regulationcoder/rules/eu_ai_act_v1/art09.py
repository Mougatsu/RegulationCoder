"""Article 9 - Risk Management System.

Providers of high-risk AI systems shall establish, implement, document and
maintain a risk management system throughout the entire lifecycle of the
high-risk AI system.
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
_ART = 9

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
            "A risk management system shall be established, implemented, documented "
            "and maintained in relation to high-risk AI systems."
        ),
    ),
    Clause(
        id=_cid(2),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        text=(
            "The risk management system shall be a continuous iterative process "
            "planned and run throughout the entire lifecycle of a high-risk AI system, "
            "requiring regular systematic review and updating."
        ),
    ),
    Clause(
        id=_cid(2, "a"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        subsection_letter="a",
        text=(
            "The risk management system shall consist of identification and analysis "
            "of the known and reasonably foreseeable risks that the high-risk AI system "
            "can pose to health, safety or fundamental rights."
        ),
        parent_clause_id=_cid(2),
    ),
    Clause(
        id=_cid(2, "b"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        subsection_letter="b",
        text=(
            "The risk management system shall consist of estimation and evaluation of "
            "the risks that may emerge when the high-risk AI system is used in "
            "accordance with its intended purpose and under conditions of reasonably "
            "foreseeable misuse."
        ),
        parent_clause_id=_cid(2),
    ),
    Clause(
        id=_cid(2, "c"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        subsection_letter="c",
        text=(
            "The risk management system shall consist of the adoption of appropriate "
            "and targeted risk management measures designed in light of the effects of "
            "the identified risks on health, safety and fundamental rights."
        ),
        parent_clause_id=_cid(2),
    ),
    Clause(
        id=_cid(3),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        text=(
            "The risk management measures referred to in paragraph 2, point (c) shall "
            "give due consideration to the effects and possible interaction of the "
            "measures, with a view to minimising risks more effectively while "
            "achieving an appropriate balance between the measures."
        ),
    ),
    Clause(
        id=_cid(5),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=5,
        text=(
            "High-risk AI systems shall be tested for the purpose of identifying the "
            "most appropriate and targeted risk management measures. Testing shall "
            "ensure that high-risk AI systems perform consistently for their intended "
            "purpose and that they are in compliance with the requirements set out in "
            "this Chapter."
        ),
    ),
    Clause(
        id=_cid(6),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=6,
        text=(
            "Testing shall be carried out against prior defined metrics and "
            "probabilistic thresholds that are appropriate to the intended purpose "
            "of the high-risk AI system."
        ),
    ),
]

# ---------------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------------
REQUIREMENTS: list[Requirement] = [
    Requirement(
        id="REQ-EU-AI-ACT-009-01-001",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="establish and maintain a risk management system",
        object="high-risk AI system",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(1, quote="A risk management system shall be established, implemented, documented and maintained")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-009-02-001",
        clause_id=_cid(2),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure the risk management system is continuous and iterative throughout the lifecycle",
        object="risk management process",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(2, quote="continuous iterative process planned and run throughout the entire lifecycle")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-009-02A-001",
        clause_id=_cid(2, "a"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="identify and analyze known and reasonably foreseeable risks",
        object="risks to health, safety or fundamental rights",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(2, "a", quote="identification and analysis of the known and reasonably foreseeable risks")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-009-02B-001",
        clause_id=_cid(2, "b"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="estimate and evaluate risks under intended purpose and foreseeable misuse",
        object="risks from intended and misuse scenarios",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(2, "b", quote="estimation and evaluation of the risks that may emerge when the high-risk AI system is used")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-009-02C-001",
        clause_id=_cid(2, "c"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="adopt appropriate and targeted risk management measures",
        object="identified risks",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(2, "c", quote="adoption of appropriate and targeted risk management measures")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-009-03-001",
        clause_id=_cid(3),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure risk management measures consider interaction effects and achieve appropriate balance",
        object="risk mitigation measures",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.85,
        citations=[_cite(3, quote="give due consideration to the effects and possible interaction of the measures")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-009-05-001",
        clause_id=_cid(5),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="test the system to identify appropriate risk management measures",
        object="high-risk AI system testing",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(5, quote="High-risk AI systems shall be tested for the purpose of identifying the most appropriate and targeted risk management measures")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-009-06-001",
        clause_id=_cid(6),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="carry out testing against prior defined metrics and probabilistic thresholds",
        object="testing procedures and metrics",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(6, quote="Testing shall be carried out against prior defined metrics and probabilistic thresholds")],
    ),
]

# ---------------------------------------------------------------------------
# Rules & evaluation functions
# ---------------------------------------------------------------------------

def _eval_rms_established(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("risk_management_system_established", False) else "fail"

def _eval_rms_continuous(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("risk_management_continuous", False) else "fail"

def _eval_risk_identification(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    residual = profile.get("residual_risks_documented", False)
    measures = profile.get("risk_mitigation_measures", [])
    return "pass" if residual and len(measures) > 0 else "fail"

def _eval_misuse_risks(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("foreseeable_misuse_documented", False) else "fail"

def _eval_risk_measures(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    measures = profile.get("risk_mitigation_measures", [])
    return "pass" if len(measures) >= 2 else "fail"

def _eval_measures_balance(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("risk_measures_interaction_assessed", False) else "fail"

def _eval_testing_documented(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("testing_procedures_documented", False) else "fail"

def _eval_testing_metrics(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("testing_metrics_defined", False) else "fail"


RULES: list[Rule] = [
    Rule(
        id="RULE-EU-AI-ACT-009-01-001",
        requirement_id="REQ-EU-AI-ACT-009-01-001",
        rule_type=RuleType.AUTOMATED,
        title="Risk management system must be established",
        description="Verify that a risk management system has been established, implemented, documented and maintained.",
        inputs_needed=["is_high_risk", "risk_management_system_established"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif risk_management_system_established: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Establish a formal risk management system covering the full lifecycle of the AI system.",
        test_cases=[
            TestCase(id="TC-009-01-P", description="High-risk with RMS", input_data={"is_high_risk": True, "risk_management_system_established": True}, expected_result="pass"),
            TestCase(id="TC-009-01-F", description="High-risk without RMS", input_data={"is_high_risk": True, "risk_management_system_established": False}, expected_result="fail"),
            TestCase(id="TC-009-01-NA", description="Not high-risk", input_data={"is_high_risk": False}, expected_result="not_applicable"),
        ],
        citations=[_cite(1, quote="A risk management system shall be established, implemented, documented and maintained")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-009-02-001",
        requirement_id="REQ-EU-AI-ACT-009-02-001",
        rule_type=RuleType.AUTOMATED,
        title="Risk management must be continuous and iterative",
        description="Verify that the risk management system is a continuous iterative process throughout the AI system lifecycle.",
        inputs_needed=["is_high_risk", "risk_management_continuous"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif risk_management_continuous: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Implement continuous risk monitoring with periodic reviews and updates throughout the system lifecycle.",
        test_cases=[
            TestCase(id="TC-009-02-P", description="Continuous RMS", input_data={"is_high_risk": True, "risk_management_continuous": True}, expected_result="pass"),
            TestCase(id="TC-009-02-F", description="Non-continuous RMS", input_data={"is_high_risk": True, "risk_management_continuous": False}, expected_result="fail"),
        ],
        citations=[_cite(2, quote="continuous iterative process planned and run throughout the entire lifecycle")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-009-02A-001",
        requirement_id="REQ-EU-AI-ACT-009-02A-001",
        rule_type=RuleType.AUTOMATED,
        title="Known and foreseeable risks must be identified",
        description="Verify that the provider has identified and analyzed known and reasonably foreseeable risks to health, safety or fundamental rights.",
        inputs_needed=["is_high_risk", "residual_risks_documented", "risk_mitigation_measures"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif residual_risks_documented and len(risk_mitigation_measures)>0: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Document all known and reasonably foreseeable risks with a formal risk identification and analysis process.",
        test_cases=[
            TestCase(id="TC-009-2A-P", description="Risks documented", input_data={"is_high_risk": True, "residual_risks_documented": True, "risk_mitigation_measures": ["m1"]}, expected_result="pass"),
            TestCase(id="TC-009-2A-F", description="Risks not documented", input_data={"is_high_risk": True, "residual_risks_documented": False, "risk_mitigation_measures": []}, expected_result="fail"),
        ],
        citations=[_cite(2, "a", quote="identification and analysis of the known and reasonably foreseeable risks")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-009-02B-001",
        requirement_id="REQ-EU-AI-ACT-009-02B-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Foreseeable misuse risks must be evaluated",
        description="Verify that risks from foreseeable misuse have been estimated and evaluated.",
        inputs_needed=["is_high_risk", "extra.foreseeable_misuse_documented"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif extra.get('foreseeable_misuse_documented'): result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Conduct a misuse scenario analysis and document risk estimates for each foreseeable misuse case.",
        test_cases=[
            TestCase(id="TC-009-2B-P", description="Misuse documented", input_data={"is_high_risk": True, "extra": {"foreseeable_misuse_documented": True}}, expected_result="pass"),
            TestCase(id="TC-009-2B-F", description="Misuse not documented", input_data={"is_high_risk": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(2, "b", quote="estimation and evaluation of the risks that may emerge")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-009-02C-001",
        requirement_id="REQ-EU-AI-ACT-009-02C-001",
        rule_type=RuleType.AUTOMATED,
        title="Risk management measures must be adopted",
        description="Verify that appropriate and targeted risk management measures have been adopted.",
        inputs_needed=["is_high_risk", "risk_mitigation_measures"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif len(risk_mitigation_measures)>=2: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Define and implement at least two risk management measures that address the identified risks.",
        test_cases=[
            TestCase(id="TC-009-2C-P", description="Multiple measures", input_data={"is_high_risk": True, "risk_mitigation_measures": ["m1", "m2"]}, expected_result="pass"),
            TestCase(id="TC-009-2C-F", description="Insufficient measures", input_data={"is_high_risk": True, "risk_mitigation_measures": ["m1"]}, expected_result="fail"),
        ],
        citations=[_cite(2, "c", quote="adoption of appropriate and targeted risk management measures")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-009-03-001",
        requirement_id="REQ-EU-AI-ACT-009-03-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Risk measures interaction must be assessed",
        description="Verify that risk management measures consider interaction effects and achieve appropriate balance.",
        inputs_needed=["is_high_risk", "extra.risk_measures_interaction_assessed"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif extra.get('risk_measures_interaction_assessed'): result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Document how risk management measures interact with each other and demonstrate an appropriate balance.",
        test_cases=[
            TestCase(id="TC-009-03-P", description="Interaction assessed", input_data={"is_high_risk": True, "extra": {"risk_measures_interaction_assessed": True}}, expected_result="pass"),
            TestCase(id="TC-009-03-F", description="Interaction not assessed", input_data={"is_high_risk": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(3, quote="give due consideration to the effects and possible interaction of the measures")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-009-05-001",
        requirement_id="REQ-EU-AI-ACT-009-05-001",
        rule_type=RuleType.AUTOMATED,
        title="System testing procedures must be documented",
        description="Verify that the system has been tested with documented procedures to identify risk management measures.",
        inputs_needed=["is_high_risk", "testing_procedures_documented"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif testing_procedures_documented: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Implement and document testing procedures to identify the most appropriate risk management measures.",
        test_cases=[
            TestCase(id="TC-009-05-P", description="Testing documented", input_data={"is_high_risk": True, "testing_procedures_documented": True}, expected_result="pass"),
            TestCase(id="TC-009-05-F", description="Testing not documented", input_data={"is_high_risk": True, "testing_procedures_documented": False}, expected_result="fail"),
        ],
        citations=[_cite(5, quote="High-risk AI systems shall be tested")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-009-06-001",
        requirement_id="REQ-EU-AI-ACT-009-06-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Testing must use defined metrics and thresholds",
        description="Verify that testing is carried out against prior defined metrics and probabilistic thresholds.",
        inputs_needed=["is_high_risk", "extra.testing_metrics_defined"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif extra.get('testing_metrics_defined'): result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Define explicit metrics and probabilistic thresholds for all testing procedures.",
        test_cases=[
            TestCase(id="TC-009-06-P", description="Metrics defined", input_data={"is_high_risk": True, "extra": {"testing_metrics_defined": True}}, expected_result="pass"),
            TestCase(id="TC-009-06-F", description="Metrics not defined", input_data={"is_high_risk": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(6, quote="Testing shall be carried out against prior defined metrics and probabilistic thresholds")],
    ),
]

EVALUATION_FUNCTIONS: dict[str, callable] = {
    "RULE-EU-AI-ACT-009-01-001": _eval_rms_established,
    "RULE-EU-AI-ACT-009-02-001": _eval_rms_continuous,
    "RULE-EU-AI-ACT-009-02A-001": _eval_risk_identification,
    "RULE-EU-AI-ACT-009-02B-001": _eval_misuse_risks,
    "RULE-EU-AI-ACT-009-02C-001": _eval_risk_measures,
    "RULE-EU-AI-ACT-009-03-001": _eval_measures_balance,
    "RULE-EU-AI-ACT-009-05-001": _eval_testing_documented,
    "RULE-EU-AI-ACT-009-06-001": _eval_testing_metrics,
}
