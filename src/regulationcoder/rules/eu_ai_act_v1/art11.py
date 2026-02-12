"""Article 11 - Technical Documentation.

Providers shall draw up technical documentation before the system is placed
on the market or put into service. Documentation shall be kept up to date.
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
_ART = 11

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
            "The technical documentation of a high-risk AI system shall be drawn up "
            "before that system is placed on the market or put into service and shall "
            "be kept up to date."
        ),
    ),
    Clause(
        id=_cid(1, "a"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=1,
        subsection_letter="a",
        text=(
            "The technical documentation shall be drawn up in such a way as to "
            "demonstrate that the high-risk AI system complies with the requirements "
            "set out in this Section."
        ),
        parent_clause_id=_cid(1),
    ),
    Clause(
        id=_cid(1, "b"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=1,
        subsection_letter="b",
        text=(
            "The technical documentation shall provide national competent authorities "
            "and notified bodies with all the necessary information to assess the "
            "compliance of the high-risk AI system with those requirements."
        ),
        parent_clause_id=_cid(1),
    ),
    Clause(
        id=_cid(1, "c"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=1,
        subsection_letter="c",
        text=(
            "The technical documentation shall contain, at a minimum, the elements "
            "set out in Annex IV, including a general description of the AI system, "
            "a detailed description of the elements of the system and of the process "
            "for its development, and detailed information about the monitoring, "
            "functioning and control of the AI system."
        ),
        parent_clause_id=_cid(1),
    ),
    Clause(
        id=_cid(1, "d"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=1,
        subsection_letter="d",
        text=(
            "The technical documentation shall be written in a clear, comprehensive, "
            "and intelligible form, so as to be understood by persons with appropriate "
            "technical expertise."
        ),
        parent_clause_id=_cid(1),
    ),
    Clause(
        id=_cid(2),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        text=(
            "The Commission shall, by means of implementing acts, establish a "
            "standardised form for the technical documentation to facilitate the "
            "fulfilment of the requirements."
        ),
    ),
    Clause(
        id=_cid(3),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        text=(
            "Where a high-risk AI system related to a product that is covered by the "
            "Union harmonisation legislation listed in Annex I, Section A, a single "
            "set of technical documentation shall be drawn up containing all the "
            "information set out in Annex IV as well as the information required "
            "under that Union harmonisation legislation."
        ),
    ),
]

# ---------------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------------
REQUIREMENTS: list[Requirement] = [
    Requirement(
        id="REQ-EU-AI-ACT-011-01-001",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="draw up technical documentation before system is placed on market",
        object="technical documentation",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(1, quote="technical documentation shall be drawn up before that system is placed on the market")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-011-01-002",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="keep technical documentation up to date",
        object="technical documentation",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(1, quote="shall be kept up to date")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-011-01A-001",
        clause_id=_cid(1, "a"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="demonstrate compliance through technical documentation",
        object="compliance demonstration",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(1, "a", quote="demonstrate that the high-risk AI system complies with the requirements")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-011-01B-001",
        clause_id=_cid(1, "b"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="provide authorities with information to assess compliance",
        object="documentation for authorities",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(1, "b", quote="provide national competent authorities and notified bodies with all the necessary information")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-011-01C-001",
        clause_id=_cid(1, "c"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="include minimum elements from Annex IV in technical documentation",
        object="Annex IV elements in documentation",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(1, "c", quote="contain, at a minimum, the elements set out in Annex IV")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-011-01D-001",
        clause_id=_cid(1, "d"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="write documentation in clear, comprehensive and intelligible form",
        object="documentation clarity",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(1, "d", quote="written in a clear, comprehensive, and intelligible form")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-011-03-001",
        clause_id=_cid(3),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system related to harmonised product",
        action="draw up single set of technical documentation combining Annex IV and product legislation",
        object="combined technical documentation",
        conditions=[Condition(description="System is related to a product covered by Union harmonisation legislation in Annex I, Section A")],
        scope="High-risk AI systems related to harmonised products",
        confidence=0.85,
        citations=[_cite(3, quote="a single set of technical documentation shall be drawn up")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-011-01-003",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="make technical documentation available and accessible",
        object="documentation accessibility",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.85,
        citations=[_cite(1, quote="technical documentation of a high-risk AI system shall be drawn up")],
    ),
]

# ---------------------------------------------------------------------------
# Rules & evaluation functions
# ---------------------------------------------------------------------------

def _eval_techdoc_exists(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("technical_documentation_exists", False) else "fail"

def _eval_techdoc_up_to_date(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("technical_documentation_exists", False):
        return "fail"
    extra = profile.get("extra", {})
    return "pass" if extra.get("technical_documentation_up_to_date", True) else "fail"

def _eval_techdoc_compliance_demo(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("technical_documentation_exists", False):
        return "fail"
    extra = profile.get("extra", {})
    return "pass" if extra.get("techdoc_demonstrates_compliance", True) else "fail"

def _eval_techdoc_authorities(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("technical_documentation_exists", False):
        return "fail"
    extra = profile.get("extra", {})
    return "pass" if extra.get("techdoc_available_to_authorities", True) else "fail"

def _eval_techdoc_annex_iv(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("techdoc_contains_annex_iv_elements", False) else "fail"

def _eval_techdoc_clarity(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("technical_documentation_exists", False):
        return "fail"
    extra = profile.get("extra", {})
    return "pass" if extra.get("techdoc_clear_and_comprehensive", True) else "fail"

def _eval_techdoc_accessible(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    url = profile.get("technical_documentation_url", "")
    return "pass" if profile.get("technical_documentation_exists", False) and url else "fail"


RULES: list[Rule] = [
    Rule(
        id="RULE-EU-AI-ACT-011-01-001",
        requirement_id="REQ-EU-AI-ACT-011-01-001",
        rule_type=RuleType.AUTOMATED,
        title="Technical documentation must exist before market placement",
        description="Verify that technical documentation has been drawn up before the AI system is placed on the market.",
        inputs_needed=["is_high_risk", "technical_documentation_exists"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif technical_documentation_exists: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Create comprehensive technical documentation in accordance with Annex IV before placing the system on the market.",
        test_cases=[
            TestCase(id="TC-011-01-P", description="Doc exists", input_data={"is_high_risk": True, "technical_documentation_exists": True}, expected_result="pass"),
            TestCase(id="TC-011-01-F", description="Doc missing", input_data={"is_high_risk": True, "technical_documentation_exists": False}, expected_result="fail"),
        ],
        citations=[_cite(1, quote="technical documentation shall be drawn up before that system is placed on the market")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-011-01-002",
        requirement_id="REQ-EU-AI-ACT-011-01-002",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Technical documentation must be kept up to date",
        description="Verify that technical documentation is kept up to date throughout the system lifecycle.",
        inputs_needed=["is_high_risk", "technical_documentation_exists", "extra.technical_documentation_up_to_date"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif up_to_date: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Establish a process for regularly updating technical documentation when changes occur.",
        test_cases=[
            TestCase(id="TC-011-02-P", description="Doc up to date", input_data={"is_high_risk": True, "technical_documentation_exists": True, "extra": {"technical_documentation_up_to_date": True}}, expected_result="pass"),
            TestCase(id="TC-011-02-F", description="Doc outdated", input_data={"is_high_risk": True, "technical_documentation_exists": True, "extra": {"technical_documentation_up_to_date": False}}, expected_result="fail"),
        ],
        citations=[_cite(1, quote="shall be kept up to date")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-011-01A-001",
        requirement_id="REQ-EU-AI-ACT-011-01A-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Documentation must demonstrate compliance",
        description="Verify that technical documentation demonstrates compliance with Chapter III Section 2 requirements.",
        inputs_needed=["is_high_risk", "technical_documentation_exists", "extra.techdoc_demonstrates_compliance"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif demonstrates_compliance: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Ensure documentation explicitly addresses and demonstrates compliance with each requirement.",
        test_cases=[
            TestCase(id="TC-011-1A-P", description="Compliance demonstrated", input_data={"is_high_risk": True, "technical_documentation_exists": True, "extra": {"techdoc_demonstrates_compliance": True}}, expected_result="pass"),
        ],
        citations=[_cite(1, "a", quote="demonstrate that the high-risk AI system complies")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-011-01B-001",
        requirement_id="REQ-EU-AI-ACT-011-01B-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Documentation must be available to authorities",
        description="Verify that documentation provides authorities with all necessary compliance information.",
        inputs_needed=["is_high_risk", "technical_documentation_exists", "extra.techdoc_available_to_authorities"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif available: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Ensure documentation is accessible and provides sufficient information for authority review.",
        test_cases=[
            TestCase(id="TC-011-1B-P", description="Available to authorities", input_data={"is_high_risk": True, "technical_documentation_exists": True, "extra": {"techdoc_available_to_authorities": True}}, expected_result="pass"),
        ],
        citations=[_cite(1, "b", quote="provide national competent authorities")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-011-01C-001",
        requirement_id="REQ-EU-AI-ACT-011-01C-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Documentation must contain Annex IV minimum elements",
        description="Verify that technical documentation contains at minimum the elements set out in Annex IV.",
        inputs_needed=["is_high_risk", "extra.techdoc_contains_annex_iv_elements"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif annex_iv: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Review documentation against Annex IV checklist and add any missing elements.",
        test_cases=[
            TestCase(id="TC-011-1C-P", description="Annex IV covered", input_data={"is_high_risk": True, "extra": {"techdoc_contains_annex_iv_elements": True}}, expected_result="pass"),
            TestCase(id="TC-011-1C-F", description="Annex IV missing", input_data={"is_high_risk": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(1, "c", quote="contain, at a minimum, the elements set out in Annex IV")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-011-01D-001",
        requirement_id="REQ-EU-AI-ACT-011-01D-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Documentation must be clear and comprehensive",
        description="Verify that documentation is written in a clear, comprehensive, and intelligible form.",
        inputs_needed=["is_high_risk", "technical_documentation_exists", "extra.techdoc_clear_and_comprehensive"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif clear: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Ensure documentation uses clear language, logical structure, and is understandable by technical experts.",
        test_cases=[
            TestCase(id="TC-011-1D-P", description="Clear docs", input_data={"is_high_risk": True, "technical_documentation_exists": True, "extra": {"techdoc_clear_and_comprehensive": True}}, expected_result="pass"),
        ],
        citations=[_cite(1, "d", quote="clear, comprehensive, and intelligible form")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-011-01-003",
        requirement_id="REQ-EU-AI-ACT-011-01-003",
        rule_type=RuleType.AUTOMATED,
        title="Technical documentation must be accessible at a known location",
        description="Verify that technical documentation is accessible (e.g., URL or internal repository).",
        inputs_needed=["is_high_risk", "technical_documentation_exists", "technical_documentation_url"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif exists and url: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Provide a URL or internal reference to the location where documentation can be accessed.",
        test_cases=[
            TestCase(id="TC-011-03-P", description="URL provided", input_data={"is_high_risk": True, "technical_documentation_exists": True, "technical_documentation_url": "https://docs.example.com"}, expected_result="pass"),
            TestCase(id="TC-011-03-F", description="No URL", input_data={"is_high_risk": True, "technical_documentation_exists": True, "technical_documentation_url": ""}, expected_result="fail"),
        ],
        citations=[_cite(1, quote="technical documentation shall be drawn up")],
    ),
]

EVALUATION_FUNCTIONS: dict[str, callable] = {
    "RULE-EU-AI-ACT-011-01-001": _eval_techdoc_exists,
    "RULE-EU-AI-ACT-011-01-002": _eval_techdoc_up_to_date,
    "RULE-EU-AI-ACT-011-01A-001": _eval_techdoc_compliance_demo,
    "RULE-EU-AI-ACT-011-01B-001": _eval_techdoc_authorities,
    "RULE-EU-AI-ACT-011-01C-001": _eval_techdoc_annex_iv,
    "RULE-EU-AI-ACT-011-01D-001": _eval_techdoc_clarity,
    "RULE-EU-AI-ACT-011-01-003": _eval_techdoc_accessible,
}
