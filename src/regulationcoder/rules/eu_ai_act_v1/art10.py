"""Article 10 - Data and Data Governance.

Training, validation and testing data sets shall meet quality criteria.
Data governance and management practices shall be established.
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
_ART = 10

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
            "High-risk AI systems which make use of techniques involving the "
            "training of AI models with data shall be developed on the basis of "
            "training, validation and testing data sets that meet the quality "
            "criteria referred to in paragraphs 2 to 5."
        ),
    ),
    Clause(
        id=_cid(2),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        text=(
            "Training, validation and testing data sets shall be subject to data "
            "governance and management practices appropriate for the intended purpose "
            "of the high-risk AI system."
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
            "Data governance and management practices shall concern the relevant "
            "design choices including data collection processes and their origin, "
            "and in the case of personal data, the original purpose of the data collection."
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
            "Data governance and management practices shall concern data-preparation "
            "processing operations, such as annotation, labelling, cleaning, updating, "
            "enrichment and aggregation."
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
            "Training, validation and testing data sets shall be relevant, sufficiently "
            "representative, and to the best extent possible, free of errors and complete "
            "in view of the intended purpose."
        ),
    ),
    Clause(
        id=_cid(4),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        text=(
            "Training, validation and testing data sets shall take into account, to "
            "the extent required by the intended purpose, the characteristics or "
            "elements that are particular to the specific geographical, contextual, "
            "behavioural or functional setting within which the high-risk AI system "
            "is intended to be used."
        ),
    ),
    Clause(
        id=_cid(5),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=5,
        text=(
            "To the extent that it is strictly necessary for the purpose of ensuring "
            "bias detection and correction in relation to the high-risk AI systems, "
            "the providers of such systems may exceptionally process special categories "
            "of personal data, subject to appropriate safeguards for the fundamental "
            "rights and freedoms of natural persons."
        ),
    ),
    Clause(
        id=_cid(2, "f"),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        subsection_letter="f",
        text=(
            "Data governance and management practices shall concern examination in "
            "view of possible biases that are likely to affect the health and safety "
            "of persons, have a negative impact on fundamental rights or lead to "
            "discrimination prohibited under Union law, especially where data outputs "
            "influence inputs for future operations."
        ),
        parent_clause_id=_cid(2),
    ),
]

# ---------------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------------
REQUIREMENTS: list[Requirement] = [
    Requirement(
        id="REQ-EU-AI-ACT-010-01-001",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="develop AI models on the basis of datasets meeting quality criteria",
        object="training, validation and testing data sets",
        conditions=[Condition(description="System uses techniques involving training of AI models with data")],
        scope="High-risk AI systems using training data",
        confidence=0.95,
        citations=[_cite(1, quote="developed on the basis of training, validation and testing data sets that meet the quality criteria")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-010-02-001",
        clause_id=_cid(2),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="apply data governance and management practices",
        object="training, validation and testing data sets",
        scope="High-risk AI systems using training data",
        confidence=0.95,
        citations=[_cite(2, quote="subject to data governance and management practices appropriate for the intended purpose")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-010-02A-001",
        clause_id=_cid(2, "a"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="document data collection processes and data origin",
        object="data collection and origin documentation",
        scope="High-risk AI systems using training data",
        confidence=0.90,
        citations=[_cite(2, "a", quote="relevant design choices including data collection processes and their origin")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-010-02B-001",
        clause_id=_cid(2, "b"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="document data-preparation processing operations",
        object="annotation, labelling, cleaning, updating, enrichment and aggregation procedures",
        scope="High-risk AI systems using training data",
        confidence=0.90,
        citations=[_cite(2, "b", quote="data-preparation processing operations, such as annotation, labelling, cleaning")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-010-03-001",
        clause_id=_cid(3),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure datasets are relevant, representative, and free of errors",
        object="training, validation and testing data sets",
        scope="High-risk AI systems using training data",
        confidence=0.95,
        citations=[_cite(3, quote="relevant, sufficiently representative, and to the best extent possible, free of errors")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-010-04-001",
        clause_id=_cid(4),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="account for geographical, contextual, behavioural and functional settings in datasets",
        object="data representativeness for deployment context",
        scope="High-risk AI systems using training data",
        confidence=0.85,
        citations=[_cite(4, quote="characteristics or elements that are particular to the specific geographical, contextual, behavioural or functional setting")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-010-02F-001",
        clause_id=_cid(2, "f"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="examine data for possible biases affecting health, safety, fundamental rights or causing prohibited discrimination",
        object="bias examination process",
        scope="High-risk AI systems using training data",
        confidence=0.95,
        citations=[_cite(2, "f", quote="examination in view of possible biases that are likely to affect the health and safety of persons")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-010-05-001",
        clause_id=_cid(5),
        modality=Modality.MAY,
        subject="Provider of high-risk AI system",
        action="process special categories of personal data for bias detection with appropriate safeguards",
        object="special categories of personal data",
        conditions=[Condition(description="Strictly necessary for bias detection and correction")],
        scope="High-risk AI systems processing special category data",
        confidence=0.90,
        citations=[_cite(5, quote="may exceptionally process special categories of personal data, subject to appropriate safeguards")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-010-03-002",
        clause_id=_cid(3),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure training data relevance is documented for the intended purpose",
        object="data relevance documentation",
        scope="High-risk AI systems using training data",
        confidence=0.90,
        citations=[_cite(3, quote="relevant, sufficiently representative")],
    ),
]

# ---------------------------------------------------------------------------
# Rules & evaluation functions
# ---------------------------------------------------------------------------

def _eval_data_governance(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("uses_training_data", False):
        return "not_applicable"
    return "pass" if profile.get("data_governance_practices_documented", False) else "fail"

def _eval_data_collection_documented(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("uses_training_data", False):
        return "not_applicable"
    return "pass" if profile.get("data_collection_process_documented", False) else "fail"

def _eval_data_preprocessing(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("uses_training_data", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("data_preprocessing_documented", False) else "fail"

def _eval_data_relevance(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("uses_training_data", False):
        return "not_applicable"
    return "pass" if profile.get("training_data_relevance_documented", False) else "fail"

def _eval_data_representativeness(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("uses_training_data", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    return "pass" if extra.get("data_representativeness_documented", False) else "fail"

def _eval_bias_examination(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("uses_training_data", False):
        return "not_applicable"
    bias = profile.get("bias_examination_report")
    if not bias:
        return "fail"
    if isinstance(bias, dict):
        covers_all = (
            bias.get("covers_health_safety", False)
            and bias.get("covers_fundamental_rights", False)
            and bias.get("covers_prohibited_discrimination", False)
        )
    else:
        covers_all = False
    return "pass" if covers_all else "fail"

def _eval_special_data_safeguards(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    if not extra.get("processes_special_category_data", False):
        return "not_applicable"
    return "pass" if extra.get("special_data_safeguards_in_place", False) else "fail"

def _eval_dataset_quality(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    if not profile.get("uses_training_data", False):
        return "not_applicable"
    datasets = profile.get("dataset_names", [])
    return "pass" if len(datasets) > 0 else "fail"


RULES: list[Rule] = [
    Rule(
        id="RULE-EU-AI-ACT-010-02-001",
        requirement_id="REQ-EU-AI-ACT-010-02-001",
        rule_type=RuleType.AUTOMATED,
        title="Data governance practices must be documented",
        description="Verify that data governance and management practices are documented and appropriate for the intended purpose.",
        inputs_needed=["is_high_risk", "uses_training_data", "data_governance_practices_documented"],
        evaluation_logic="if not is_high_risk or not uses_training_data: result='not_applicable'\nelif data_governance_practices_documented: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Document data governance and management practices covering the full data lifecycle.",
        test_cases=[
            TestCase(id="TC-010-02-P", description="Governance documented", input_data={"is_high_risk": True, "uses_training_data": True, "data_governance_practices_documented": True}, expected_result="pass"),
            TestCase(id="TC-010-02-F", description="Governance missing", input_data={"is_high_risk": True, "uses_training_data": True, "data_governance_practices_documented": False}, expected_result="fail"),
        ],
        citations=[_cite(2, quote="subject to data governance and management practices")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-010-02A-001",
        requirement_id="REQ-EU-AI-ACT-010-02A-001",
        rule_type=RuleType.AUTOMATED,
        title="Data collection process must be documented",
        description="Verify that data collection processes and data origin are documented.",
        inputs_needed=["is_high_risk", "uses_training_data", "data_collection_process_documented"],
        evaluation_logic="if not is_high_risk or not uses_training_data: result='not_applicable'\nelif data_collection_process_documented: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Document data collection processes including sources, methods, and original purpose.",
        test_cases=[
            TestCase(id="TC-010-2A-P", description="Collection documented", input_data={"is_high_risk": True, "uses_training_data": True, "data_collection_process_documented": True}, expected_result="pass"),
            TestCase(id="TC-010-2A-F", description="Collection not documented", input_data={"is_high_risk": True, "uses_training_data": True, "data_collection_process_documented": False}, expected_result="fail"),
        ],
        citations=[_cite(2, "a", quote="data collection processes and their origin")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-010-02B-001",
        requirement_id="REQ-EU-AI-ACT-010-02B-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Data preprocessing operations must be documented",
        description="Verify that data-preparation processing operations are documented.",
        inputs_needed=["is_high_risk", "uses_training_data", "extra.data_preprocessing_documented"],
        evaluation_logic="if not is_high_risk or not uses_training_data: result='not_applicable'\nelif extra.get('data_preprocessing_documented'): result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Document all data-preparation operations including annotation, labelling, cleaning and enrichment procedures.",
        test_cases=[
            TestCase(id="TC-010-2B-P", description="Preprocessing documented", input_data={"is_high_risk": True, "uses_training_data": True, "extra": {"data_preprocessing_documented": True}}, expected_result="pass"),
            TestCase(id="TC-010-2B-F", description="Preprocessing not documented", input_data={"is_high_risk": True, "uses_training_data": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(2, "b", quote="data-preparation processing operations")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-010-03-001",
        requirement_id="REQ-EU-AI-ACT-010-03-001",
        rule_type=RuleType.AUTOMATED,
        title="Training data relevance must be documented",
        description="Verify that training data relevance for the intended purpose is documented.",
        inputs_needed=["is_high_risk", "uses_training_data", "training_data_relevance_documented"],
        evaluation_logic="if not is_high_risk or not uses_training_data: result='not_applicable'\nelif training_data_relevance_documented: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Document how training datasets are relevant and representative for the intended purpose.",
        test_cases=[
            TestCase(id="TC-010-03-P", description="Relevance documented", input_data={"is_high_risk": True, "uses_training_data": True, "training_data_relevance_documented": True}, expected_result="pass"),
            TestCase(id="TC-010-03-F", description="Relevance not documented", input_data={"is_high_risk": True, "uses_training_data": True, "training_data_relevance_documented": False}, expected_result="fail"),
        ],
        citations=[_cite(3, quote="relevant, sufficiently representative, and to the best extent possible, free of errors")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-010-04-001",
        requirement_id="REQ-EU-AI-ACT-010-04-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Data representativeness for deployment context must be documented",
        description="Verify that datasets account for the geographical, contextual and functional settings of deployment.",
        inputs_needed=["is_high_risk", "uses_training_data", "extra.data_representativeness_documented"],
        evaluation_logic="if not is_high_risk or not uses_training_data: result='not_applicable'\nelif extra.get('data_representativeness_documented'): result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Document how training data accounts for the specific deployment context and population characteristics.",
        test_cases=[
            TestCase(id="TC-010-04-P", description="Representativeness documented", input_data={"is_high_risk": True, "uses_training_data": True, "extra": {"data_representativeness_documented": True}}, expected_result="pass"),
            TestCase(id="TC-010-04-F", description="Representativeness not documented", input_data={"is_high_risk": True, "uses_training_data": True, "extra": {}}, expected_result="fail"),
        ],
        citations=[_cite(4, quote="characteristics or elements that are particular to the specific geographical, contextual, behavioural or functional setting")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-010-02F-001",
        requirement_id="REQ-EU-AI-ACT-010-02F-001",
        rule_type=RuleType.AUTOMATED,
        title="Bias examination must cover health, safety, fundamental rights and discrimination",
        description="Verify that a bias examination has been conducted covering health/safety, fundamental rights, and prohibited discrimination.",
        inputs_needed=["is_high_risk", "uses_training_data", "bias_examination_report"],
        evaluation_logic="if not is_high_risk or not uses_training_data: result='not_applicable'\nelif bias covers all: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Conduct a comprehensive bias examination covering health/safety impacts, fundamental rights implications, and prohibited discrimination grounds.",
        test_cases=[
            TestCase(id="TC-010-2F-P", description="Full bias examination", input_data={"is_high_risk": True, "uses_training_data": True, "bias_examination_report": {"covers_health_safety": True, "covers_fundamental_rights": True, "covers_prohibited_discrimination": True}}, expected_result="pass"),
            TestCase(id="TC-010-2F-F", description="Incomplete bias examination", input_data={"is_high_risk": True, "uses_training_data": True, "bias_examination_report": {"covers_health_safety": True, "covers_fundamental_rights": False}}, expected_result="fail"),
        ],
        citations=[_cite(2, "f", quote="examination in view of possible biases")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-010-05-001",
        requirement_id="REQ-EU-AI-ACT-010-05-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Special category data processing must have appropriate safeguards",
        description="Verify that processing of special categories of personal data is strictly necessary and has appropriate safeguards.",
        inputs_needed=["is_high_risk", "extra.processes_special_category_data", "extra.special_data_safeguards_in_place"],
        evaluation_logic="if not special_category: result='not_applicable'\nelif safeguards: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Implement appropriate safeguards for any processing of special categories of personal data.",
        test_cases=[
            TestCase(id="TC-010-05-P", description="Safeguards in place", input_data={"is_high_risk": True, "extra": {"processes_special_category_data": True, "special_data_safeguards_in_place": True}}, expected_result="pass"),
            TestCase(id="TC-010-05-NA", description="No special data", input_data={"is_high_risk": True, "extra": {"processes_special_category_data": False}}, expected_result="not_applicable"),
        ],
        citations=[_cite(5, quote="appropriate safeguards for the fundamental rights and freedoms")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-010-01-001",
        requirement_id="REQ-EU-AI-ACT-010-01-001",
        rule_type=RuleType.AUTOMATED,
        title="Datasets meeting quality criteria must be used",
        description="Verify that training, validation and testing datasets are identified and meet quality criteria.",
        inputs_needed=["is_high_risk", "uses_training_data", "dataset_names"],
        evaluation_logic="if not is_high_risk or not uses_training_data: result='not_applicable'\nelif len(dataset_names)>0: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Identify and document all training, validation and testing datasets with their quality criteria.",
        test_cases=[
            TestCase(id="TC-010-01-P", description="Datasets identified", input_data={"is_high_risk": True, "uses_training_data": True, "dataset_names": ["train_v1"]}, expected_result="pass"),
            TestCase(id="TC-010-01-F", description="No datasets", input_data={"is_high_risk": True, "uses_training_data": True, "dataset_names": []}, expected_result="fail"),
        ],
        citations=[_cite(1, quote="training, validation and testing data sets that meet the quality criteria")],
    ),
]

EVALUATION_FUNCTIONS: dict[str, callable] = {
    "RULE-EU-AI-ACT-010-02-001": _eval_data_governance,
    "RULE-EU-AI-ACT-010-02A-001": _eval_data_collection_documented,
    "RULE-EU-AI-ACT-010-02B-001": _eval_data_preprocessing,
    "RULE-EU-AI-ACT-010-03-001": _eval_data_relevance,
    "RULE-EU-AI-ACT-010-04-001": _eval_data_representativeness,
    "RULE-EU-AI-ACT-010-02F-001": _eval_bias_examination,
    "RULE-EU-AI-ACT-010-05-001": _eval_special_data_safeguards,
    "RULE-EU-AI-ACT-010-01-001": _eval_dataset_quality,
}
