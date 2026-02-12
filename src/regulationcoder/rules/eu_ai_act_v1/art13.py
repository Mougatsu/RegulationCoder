"""Article 13 - Transparency and Provision of Information to Deployers.

High-risk AI systems shall be designed and developed in such a way as to
ensure that their operation is sufficiently transparent to enable deployers
to interpret the system's output and use it appropriately.
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
_ART = 13

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
            "High-risk AI systems shall be designed and developed in such a way as "
            "to ensure that their operation is sufficiently transparent to enable "
            "deployers to interpret the system's output and use it appropriately."
        ),
    ),
    Clause(
        id=_cid(2),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        text=(
            "High-risk AI systems shall be accompanied by instructions for use in "
            "an appropriate digital format or otherwise that include concise, "
            "complete, correct and clear information that is relevant, accessible "
            "and comprehensible to deployers."
        ),
    ),
    Clause(
        id=_cid(3, "a"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        subsection_letter="a",
        text=(
            "The instructions for use shall contain the identity and the contact "
            "details of the provider and, where applicable, of its authorised "
            "representative."
        ),
    ),
    Clause(
        id=_cid(3, "b"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        subsection_letter="b",
        text=(
            "The instructions for use shall contain the characteristics, capabilities "
            "and limitations of performance of the high-risk AI system, including its "
            "intended purpose, the level of accuracy, robustness and cybersecurity "
            "against which it has been tested and validated, and any known or foreseeable "
            "circumstances that may lead to risks."
        ),
    ),
    Clause(
        id=_cid(3, "c"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        subsection_letter="c",
        text=(
            "The instructions for use shall contain the changes to the high-risk AI "
            "system and its performance which have been pre-determined by the provider "
            "at the moment of the initial conformity assessment."
        ),
    ),
    Clause(
        id=_cid(3, "d"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        subsection_letter="d",
        text=(
            "The instructions for use shall contain the human oversight measures "
            "referred to in Article 14, including the technical measures put in place "
            "to facilitate the interpretation of the outputs of the high-risk AI "
            "system by deployers."
        ),
    ),
    Clause(
        id=_cid(3, "e"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        subsection_letter="e",
        text=(
            "The instructions for use shall contain a description of the intended "
            "purpose of the AI system and any foreseeable misuse circumstances that "
            "could lead to risks to health, safety or fundamental rights."
        ),
    ),
    Clause(
        id=_cid(3, "f"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        subsection_letter="f",
        text=(
            "The instructions for use shall include, where appropriate, the technical "
            "capabilities and characteristics of the high-risk AI system to provide "
            "information that is relevant to explain its output."
        ),
    ),
]

# ---------------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------------
REQUIREMENTS: list[Requirement] = [
    Requirement(
        id="REQ-EU-AI-ACT-013-01-001",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="design system to ensure operation is sufficiently transparent",
        object="operational transparency",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(1, quote="operation is sufficiently transparent to enable deployers to interpret the system's output")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-013-02-001",
        clause_id=_cid(2),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="provide instructions for use in appropriate digital format",
        object="instructions for use",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(2, quote="accompanied by instructions for use in an appropriate digital format")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-013-03A-001",
        clause_id=_cid(3, "a"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="include provider identity and contact details in instructions",
        object="provider identification",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(3, "a", quote="identity and the contact details of the provider")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-013-03B-001",
        clause_id=_cid(3, "b"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="include system characteristics, capabilities and limitations in instructions",
        object="system capability documentation",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(3, "b", quote="characteristics, capabilities and limitations of performance")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-013-03C-001",
        clause_id=_cid(3, "c"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="document pre-determined changes to system and performance",
        object="pre-determined change documentation",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.85,
        citations=[_cite(3, "c", quote="changes to the high-risk AI system and its performance which have been pre-determined")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-013-03D-001",
        clause_id=_cid(3, "d"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="document human oversight measures in instructions for use",
        object="human oversight documentation",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(3, "d", quote="human oversight measures referred to in Article 14")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-013-03E-001",
        clause_id=_cid(3, "e"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="describe intended purpose and foreseeable misuse circumstances",
        object="intended purpose and misuse documentation",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(3, "e", quote="intended purpose of the AI system and any foreseeable misuse circumstances")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-013-03F-001",
        clause_id=_cid(3, "f"),
        modality=Modality.SHOULD,
        subject="Provider of high-risk AI system",
        action="include technical capabilities relevant to explain system output",
        object="output explainability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.85,
        citations=[_cite(3, "f", quote="technical capabilities and characteristics to provide information relevant to explain its output")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-013-03B-002",
        clause_id=_cid(3, "b"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="declare accuracy levels in instructions for use",
        object="accuracy level declaration",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(3, "b", quote="the level of accuracy, robustness and cybersecurity against which it has been tested")],
    ),
]

# ---------------------------------------------------------------------------
# Rules & evaluation functions
# ---------------------------------------------------------------------------

def _eval_transparency(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("system_operation_transparent", False) else "fail"

def _eval_instructions_provided(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("instructions_for_use_provided", False) else "fail"

def _eval_provider_identity(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    provider = profile.get("provider_name", "")
    return "pass" if provider else "fail"

def _eval_capabilities_documented(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("limitations_documented", False) else "fail"

def _eval_intended_purpose(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("intended_purpose_documented", False) else "fail"

def _eval_human_oversight_docs(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    measures = profile.get("human_oversight_measures", [])
    extra = profile.get("extra", {})
    return "pass" if len(measures) > 0 and extra.get("oversight_documented_in_instructions", True) else "fail"

def _eval_misuse_documented(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("foreseeable_misuse_documented", False) else "fail"

def _eval_accuracy_declared(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    levels = profile.get("accuracy_levels_declared", "")
    return "pass" if levels else "fail"


RULES: list[Rule] = [
    Rule(
        id="RULE-EU-AI-ACT-013-01-001",
        requirement_id="REQ-EU-AI-ACT-013-01-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="System operation must be sufficiently transparent",
        description="Verify that the system is designed to ensure operation is transparent enough for deployers to interpret output.",
        inputs_needed=["is_high_risk", "extra.system_operation_transparent"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif transparent: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Design the system with output explanations, confidence scores, or feature attribution to ensure transparency.",
        test_cases=[
            TestCase(id="TC-013-01-P", description="Transparent", input_data={"is_high_risk": True, "extra": {"system_operation_transparent": True}}, expected_result="pass"),
            TestCase(id="TC-013-01-F", description="Not transparent", input_data={"is_high_risk": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(1, quote="operation is sufficiently transparent")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-013-02-001",
        requirement_id="REQ-EU-AI-ACT-013-02-001",
        rule_type=RuleType.AUTOMATED,
        title="Instructions for use must be provided",
        description="Verify that instructions for use are provided in an appropriate digital format.",
        inputs_needed=["is_high_risk", "instructions_for_use_provided"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif instructions_for_use_provided: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Create comprehensive instructions for use in digital format for deployers.",
        test_cases=[
            TestCase(id="TC-013-02-P", description="Instructions provided", input_data={"is_high_risk": True, "instructions_for_use_provided": True}, expected_result="pass"),
            TestCase(id="TC-013-02-F", description="No instructions", input_data={"is_high_risk": True, "instructions_for_use_provided": False}, expected_result="fail"),
        ],
        citations=[_cite(2, quote="accompanied by instructions for use in an appropriate digital format")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-013-03A-001",
        requirement_id="REQ-EU-AI-ACT-013-03A-001",
        rule_type=RuleType.AUTOMATED,
        title="Provider identity must be included in instructions",
        description="Verify that provider identity and contact details are included in instructions.",
        inputs_needed=["is_high_risk", "provider_name"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif provider_name: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Include complete provider identity and contact details in the instructions for use.",
        test_cases=[
            TestCase(id="TC-013-3A-P", description="Provider identified", input_data={"is_high_risk": True, "provider_name": "Acme Corp"}, expected_result="pass"),
        ],
        citations=[_cite(3, "a", quote="identity and the contact details of the provider")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-013-03B-001",
        requirement_id="REQ-EU-AI-ACT-013-03B-001",
        rule_type=RuleType.AUTOMATED,
        title="System capabilities and limitations must be documented",
        description="Verify that system characteristics, capabilities and limitations of performance are documented.",
        inputs_needed=["is_high_risk", "limitations_documented"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif limitations_documented: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Document all system capabilities, limitations, and known performance boundaries.",
        test_cases=[
            TestCase(id="TC-013-3B-P", description="Limitations documented", input_data={"is_high_risk": True, "limitations_documented": True}, expected_result="pass"),
            TestCase(id="TC-013-3B-F", description="No limitation docs", input_data={"is_high_risk": True, "limitations_documented": False}, expected_result="fail"),
        ],
        citations=[_cite(3, "b", quote="characteristics, capabilities and limitations of performance")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-013-03D-001",
        requirement_id="REQ-EU-AI-ACT-013-03D-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Human oversight measures must be documented in instructions",
        description="Verify that human oversight measures are described in the instructions for use.",
        inputs_needed=["is_high_risk", "human_oversight_measures", "extra.oversight_documented_in_instructions"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif measures and documented: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Document human oversight measures in the instructions for use, including interpretation guidance.",
        test_cases=[
            TestCase(id="TC-013-3D-P", description="Oversight documented", input_data={"is_high_risk": True, "human_oversight_measures": ["review"], "extra": {"oversight_documented_in_instructions": True}}, expected_result="pass"),
            TestCase(id="TC-013-3D-F", description="No oversight measures", input_data={"is_high_risk": True, "human_oversight_measures": []}, expected_result="fail"),
        ],
        citations=[_cite(3, "d", quote="human oversight measures referred to in Article 14")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-013-03E-001",
        requirement_id="REQ-EU-AI-ACT-013-03E-001",
        rule_type=RuleType.AUTOMATED,
        title="Intended purpose must be documented",
        description="Verify that intended purpose is clearly documented in instructions.",
        inputs_needed=["is_high_risk", "intended_purpose_documented"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif intended_purpose_documented: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Clearly document the intended purpose and foreseeable misuse circumstances.",
        test_cases=[
            TestCase(id="TC-013-3E-P", description="Purpose documented", input_data={"is_high_risk": True, "intended_purpose_documented": True}, expected_result="pass"),
            TestCase(id="TC-013-3E-F", description="Purpose not documented", input_data={"is_high_risk": True, "intended_purpose_documented": False}, expected_result="fail"),
        ],
        citations=[_cite(3, "e", quote="intended purpose of the AI system")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-013-03B-002",
        requirement_id="REQ-EU-AI-ACT-013-03B-002",
        rule_type=RuleType.AUTOMATED,
        title="Accuracy levels must be declared in instructions",
        description="Verify that accuracy levels are declared in the instructions for use.",
        inputs_needed=["is_high_risk", "accuracy_levels_declared"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif accuracy_levels_declared: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Declare specific accuracy levels and metrics in the instructions for use.",
        test_cases=[
            TestCase(id="TC-013-3B2-P", description="Accuracy declared", input_data={"is_high_risk": True, "accuracy_levels_declared": "F1=0.92"}, expected_result="pass"),
            TestCase(id="TC-013-3B2-F", description="No accuracy declared", input_data={"is_high_risk": True, "accuracy_levels_declared": ""}, expected_result="fail"),
        ],
        citations=[_cite(3, "b", quote="the level of accuracy")],
    ),
]

EVALUATION_FUNCTIONS: dict[str, callable] = {
    "RULE-EU-AI-ACT-013-01-001": _eval_transparency,
    "RULE-EU-AI-ACT-013-02-001": _eval_instructions_provided,
    "RULE-EU-AI-ACT-013-03A-001": _eval_provider_identity,
    "RULE-EU-AI-ACT-013-03B-001": _eval_capabilities_documented,
    "RULE-EU-AI-ACT-013-03D-001": _eval_human_oversight_docs,
    "RULE-EU-AI-ACT-013-03E-001": _eval_intended_purpose,
    "RULE-EU-AI-ACT-013-03B-002": _eval_accuracy_declared,
}
