"""Article 12 - Record-Keeping.

High-risk AI systems shall technically allow for the automatic recording of
events (logs) over the lifetime of the system.
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
_ART = 12

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
            "High-risk AI systems shall technically allow for the automatic recording "
            "of events (logs) over the lifetime of the system."
        ),
    ),
    Clause(
        id=_cid(2),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        text=(
            "In order to ensure a level of traceability of the functioning of a "
            "high-risk AI system that is appropriate to the intended purpose of the "
            "system, logging capabilities shall enable the recording of events relevant "
            "to the identification of situations that may result in the AI system "
            "presenting a risk within the meaning of Article 79(1) or lead to a "
            "substantial modification."
        ),
    ),
    Clause(
        id=_cid(3),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        text=(
            "Logging capabilities shall conform to recognised standards or common "
            "specifications to ensure interoperability and facilitate post-market "
            "monitoring."
        ),
    ),
    Clause(
        id=_cid(4),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        text=(
            "Logging capabilities shall ensure a level of traceability of the AI "
            "system's functioning throughout its lifecycle that is appropriate to the "
            "intended purpose of the system."
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
            "Logging capabilities shall enable the monitoring of the operation of "
            "the high-risk AI system with respect to the occurrence of situations "
            "that may result in the AI system presenting a risk."
        ),
        parent_clause_id=_cid(4),
    ),
    Clause(
        id=_cid(4, "b"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        subsection_letter="b",
        text=(
            "Logging capabilities shall facilitate the post-market monitoring "
            "referred to in Article 72, including by providing the basis for such "
            "monitoring to be carried out effectively."
        ),
        parent_clause_id=_cid(4),
    ),
    Clause(
        id=_cid(4, "c"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        subsection_letter="c",
        text=(
            "Logging capabilities shall include recording of the period of each use "
            "of the system, the reference database against which input data has been "
            "checked, the input data for which the search has led to a match, and "
            "the identification of the natural persons involved in the verification "
            "of the results."
        ),
        parent_clause_id=_cid(4),
    ),
]

# ---------------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------------
REQUIREMENTS: list[Requirement] = [
    Requirement(
        id="REQ-EU-AI-ACT-012-01-001",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="enable automatic recording of events (logs) over the system lifetime",
        object="automatic logging capability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(1, quote="shall technically allow for the automatic recording of events (logs)")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-012-02-001",
        clause_id=_cid(2),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure logging enables recording of risk-relevant events and substantial modifications",
        object="risk-related event logging",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(2, quote="recording of events relevant to the identification of situations that may result in the AI system presenting a risk")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-012-03-001",
        clause_id=_cid(3),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure logging capabilities conform to recognised standards or common specifications",
        object="logging standards compliance",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(3, quote="conform to recognised standards or common specifications")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-012-04-001",
        clause_id=_cid(4),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure traceability of AI system functioning throughout lifecycle",
        object="lifecycle traceability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(4, quote="traceability of the AI system's functioning throughout its lifecycle")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-012-04A-001",
        clause_id=_cid(4, "a"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="enable monitoring of operation for risk-presenting situations",
        object="operational monitoring capability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(4, "a", quote="enable the monitoring of the operation of the high-risk AI system")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-012-04B-001",
        clause_id=_cid(4, "b"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="facilitate post-market monitoring through logging",
        object="post-market monitoring support",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(4, "b", quote="facilitate the post-market monitoring")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-012-04C-001",
        clause_id=_cid(4, "c"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="record usage periods, reference databases, matched input data and verification personnel",
        object="detailed usage records",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.85,
        citations=[_cite(4, "c", quote="recording of the period of each use of the system")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-012-03-002",
        clause_id=_cid(3),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure logging interoperability",
        object="logging interoperability",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.85,
        citations=[_cite(3, quote="ensure interoperability")],
    ),
]

# ---------------------------------------------------------------------------
# Rules & evaluation functions
# ---------------------------------------------------------------------------

def _eval_logging_enabled(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("automatic_logging_enabled", False) else "fail"

def _eval_logging_risk_events(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    caps = profile.get("logging_capabilities", [])
    has_risk_logging = any("risk" in c.lower() or "incident" in c.lower() for c in caps)
    return "pass" if has_risk_logging else "fail"

def _eval_logging_standards(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("logging_conforms_to_standards", False) else "fail"

def _eval_logging_traceability(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    caps = profile.get("logging_capabilities", [])
    return "pass" if len(caps) >= 2 else "fail"

def _eval_logging_monitoring(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    caps = profile.get("logging_capabilities", [])
    has_monitoring = any("monitor" in c.lower() or "operation" in c.lower() for c in caps)
    return "pass" if has_monitoring else "fail"

def _eval_post_market(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("post_market_monitoring_supported", False) else "fail"

def _eval_usage_records(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    caps = profile.get("logging_capabilities", [])
    has_usage = any("usage" in c.lower() or "period" in c.lower() or "session" in c.lower() for c in caps)
    return "pass" if has_usage else "fail"


RULES: list[Rule] = [
    Rule(
        id="RULE-EU-AI-ACT-012-01-001",
        requirement_id="REQ-EU-AI-ACT-012-01-001",
        rule_type=RuleType.AUTOMATED,
        title="Automatic event logging must be enabled",
        description="Verify that the system technically supports automatic recording of events (logs).",
        inputs_needed=["is_high_risk", "automatic_logging_enabled"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif automatic_logging_enabled: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Implement automatic event logging throughout the system lifecycle.",
        test_cases=[
            TestCase(id="TC-012-01-P", description="Logging enabled", input_data={"is_high_risk": True, "automatic_logging_enabled": True}, expected_result="pass"),
            TestCase(id="TC-012-01-F", description="Logging disabled", input_data={"is_high_risk": True, "automatic_logging_enabled": False}, expected_result="fail"),
        ],
        citations=[_cite(1, quote="shall technically allow for the automatic recording of events")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-012-02-001",
        requirement_id="REQ-EU-AI-ACT-012-02-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Risk-relevant events must be logged",
        description="Verify that logging captures events relevant to risk identification.",
        inputs_needed=["is_high_risk", "logging_capabilities"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif has risk logging: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Add logging for risk-relevant events including anomalies, errors, and safety-critical decisions.",
        test_cases=[
            TestCase(id="TC-012-02-P", description="Risk logging present", input_data={"is_high_risk": True, "logging_capabilities": ["risk event tracking"]}, expected_result="pass"),
            TestCase(id="TC-012-02-F", description="No risk logging", input_data={"is_high_risk": True, "logging_capabilities": ["basic access logs"]}, expected_result="fail"),
        ],
        citations=[_cite(2, quote="recording of events relevant to the identification of situations")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-012-03-001",
        requirement_id="REQ-EU-AI-ACT-012-03-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Logging must conform to recognised standards",
        description="Verify that logging capabilities conform to recognised standards or common specifications.",
        inputs_needed=["is_high_risk", "extra.logging_conforms_to_standards"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif standards: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Align logging capabilities with recognised standards such as ISO 27001 or equivalent.",
        test_cases=[
            TestCase(id="TC-012-03-P", description="Standards compliant", input_data={"is_high_risk": True, "extra": {"logging_conforms_to_standards": True}}, expected_result="pass"),
            TestCase(id="TC-012-03-F", description="No standards", input_data={"is_high_risk": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(3, quote="conform to recognised standards or common specifications")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-012-04-001",
        requirement_id="REQ-EU-AI-ACT-012-04-001",
        rule_type=RuleType.AUTOMATED,
        title="Logging must ensure lifecycle traceability",
        description="Verify that logging capabilities ensure traceability throughout the system lifecycle.",
        inputs_needed=["is_high_risk", "logging_capabilities"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif len(caps)>=2: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Implement comprehensive logging covering all lifecycle stages with sufficient detail for traceability.",
        test_cases=[
            TestCase(id="TC-012-04-P", description="Sufficient logging", input_data={"is_high_risk": True, "logging_capabilities": ["input/output logging", "decision audit trail"]}, expected_result="pass"),
            TestCase(id="TC-012-04-F", description="Insufficient logging", input_data={"is_high_risk": True, "logging_capabilities": ["basic"]}, expected_result="fail"),
        ],
        citations=[_cite(4, quote="traceability of the AI system's functioning throughout its lifecycle")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-012-04A-001",
        requirement_id="REQ-EU-AI-ACT-012-04A-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Logging must enable operational monitoring",
        description="Verify that logging enables monitoring of the AI system operation.",
        inputs_needed=["is_high_risk", "logging_capabilities"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif monitoring in caps: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Add operational monitoring capabilities to the logging system.",
        test_cases=[
            TestCase(id="TC-012-4A-P", description="Monitoring enabled", input_data={"is_high_risk": True, "logging_capabilities": ["operational monitoring"]}, expected_result="pass"),
            TestCase(id="TC-012-4A-F", description="No monitoring", input_data={"is_high_risk": True, "logging_capabilities": ["basic"]}, expected_result="fail"),
        ],
        citations=[_cite(4, "a", quote="enable the monitoring of the operation")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-012-04B-001",
        requirement_id="REQ-EU-AI-ACT-012-04B-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Logging must facilitate post-market monitoring",
        description="Verify that logging facilitates post-market monitoring as per Article 72.",
        inputs_needed=["is_high_risk", "extra.post_market_monitoring_supported"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif supported: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Implement logging features that support post-market monitoring requirements.",
        test_cases=[
            TestCase(id="TC-012-4B-P", description="Post-market supported", input_data={"is_high_risk": True, "extra": {"post_market_monitoring_supported": True}}, expected_result="pass"),
            TestCase(id="TC-012-4B-F", description="Post-market not supported", input_data={"is_high_risk": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(4, "b", quote="facilitate the post-market monitoring")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-012-04C-001",
        requirement_id="REQ-EU-AI-ACT-012-04C-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Usage periods and verification personnel must be recorded",
        description="Verify that logging records usage periods, reference databases, and verification personnel.",
        inputs_needed=["is_high_risk", "logging_capabilities"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif usage in caps: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Add logging of usage sessions, reference database checks, and human verification records.",
        test_cases=[
            TestCase(id="TC-012-4C-P", description="Usage recorded", input_data={"is_high_risk": True, "logging_capabilities": ["session usage tracking"]}, expected_result="pass"),
            TestCase(id="TC-012-4C-F", description="No usage recording", input_data={"is_high_risk": True, "logging_capabilities": ["error logs"]}, expected_result="fail"),
        ],
        citations=[_cite(4, "c", quote="recording of the period of each use of the system")],
    ),
]

EVALUATION_FUNCTIONS: dict[str, callable] = {
    "RULE-EU-AI-ACT-012-01-001": _eval_logging_enabled,
    "RULE-EU-AI-ACT-012-02-001": _eval_logging_risk_events,
    "RULE-EU-AI-ACT-012-03-001": _eval_logging_standards,
    "RULE-EU-AI-ACT-012-04-001": _eval_logging_traceability,
    "RULE-EU-AI-ACT-012-04A-001": _eval_logging_monitoring,
    "RULE-EU-AI-ACT-012-04B-001": _eval_post_market,
    "RULE-EU-AI-ACT-012-04C-001": _eval_usage_records,
}
