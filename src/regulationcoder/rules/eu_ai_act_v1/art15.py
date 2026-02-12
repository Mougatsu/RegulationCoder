"""Article 15 - Accuracy, Robustness and Cybersecurity.

High-risk AI systems shall be designed and developed in such a way that they
achieve an appropriate level of accuracy, robustness and cybersecurity, and
perform consistently in those respects throughout their lifecycle.
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
_ART = 15

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
            "High-risk AI systems shall be designed and developed in such a way "
            "that they achieve an appropriate level of accuracy, robustness and "
            "cybersecurity, and that they perform consistently in those respects "
            "throughout their lifecycle."
        ),
    ),
    Clause(
        id=_cid(2),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=2,
        text=(
            "The levels of accuracy and the relevant accuracy metrics of high-risk "
            "AI systems shall be declared in the accompanying instructions of use."
        ),
    ),
    Clause(
        id=_cid(3),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=3,
        text=(
            "High-risk AI systems shall be as resilient as possible regarding "
            "errors, faults or inconsistencies that may occur within the system "
            "or the environment in which the system operates, in particular due "
            "to their interaction with natural persons or other systems."
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
            "Technical and organisational measures shall be taken to ensure "
            "robustness, including technical redundancy solutions where appropriate, "
            "such as backup or fail-safe plans."
        ),
        parent_clause_id=_cid(3),
    ),
    Clause(
        id=_cid(4),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=4,
        text=(
            "High-risk AI systems shall be resilient against attempts by "
            "unauthorised third parties to alter their use, outputs or performance "
            "by exploiting the system vulnerabilities."
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
            "The technical solutions aimed at ensuring the cybersecurity of "
            "high-risk AI systems shall be appropriate to the relevant circumstances "
            "and the risks, and may include measures to prevent and control for "
            "attacks trying to manipulate the training data set (data poisoning), "
            "or pre-trained components used in training (model poisoning), inputs "
            "designed to cause the AI model to make a mistake (adversarial examples "
            "or model evasion), confidentiality attacks or model flaws."
        ),
        parent_clause_id=_cid(4),
    ),
    Clause(
        id=_cid(5),
        regulation_id=_REG_ID,
        document_version=_DOC_VERSION,
        article_number=_ART,
        paragraph_number=5,
        text=(
            "High-risk AI systems that continue to learn after being placed on "
            "the market or put into service shall be developed in such a way as "
            "to eliminate or reduce as far as possible the risk of possibly biased "
            "outputs influencing input for future operations (feedback loops) and "
            "as to ensure that any such feedback loops are duly addressed with "
            "appropriate mitigation measures."
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
            "Where appropriate, the accuracy of high-risk AI systems shall be "
            "measured and declared using disaggregated metrics, in particular "
            "when the system has an impact on fundamental rights of different "
            "groups of persons."
        ),
        parent_clause_id=_cid(2),
    ),
]

# ---------------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------------
REQUIREMENTS: list[Requirement] = [
    Requirement(
        id="REQ-EU-AI-ACT-015-01-001",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="achieve appropriate level of accuracy, robustness and cybersecurity",
        object="system accuracy, robustness and cybersecurity",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(1, quote="achieve an appropriate level of accuracy, robustness and cybersecurity")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-015-02-001",
        clause_id=_cid(2),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="declare accuracy levels and metrics in instructions of use",
        object="accuracy metric declaration",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(2, quote="levels of accuracy and the relevant accuracy metrics shall be declared")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-015-02A-001",
        clause_id=_cid(2, "a"),
        modality=Modality.SHOULD,
        subject="Provider of high-risk AI system",
        action="measure and declare accuracy using disaggregated metrics",
        object="disaggregated accuracy metrics",
        conditions=[Condition(description="System impacts fundamental rights of different groups")],
        scope="High-risk AI systems impacting different groups",
        confidence=0.90,
        citations=[_cite(2, "a", quote="accuracy shall be measured and declared using disaggregated metrics")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-015-03-001",
        clause_id=_cid(3),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure system is resilient against errors, faults and inconsistencies",
        object="error resilience",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(3, quote="resilient as possible regarding errors, faults or inconsistencies")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-015-03A-001",
        clause_id=_cid(3, "a"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="take technical and organisational measures for robustness",
        object="robustness measures",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(3, "a", quote="Technical and organisational measures shall be taken to ensure robustness")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-015-04-001",
        clause_id=_cid(4),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure resilience against unauthorized third party manipulation",
        object="third party attack resilience",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(4, quote="resilient against attempts by unauthorised third parties")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-015-04A-001",
        clause_id=_cid(4, "a"),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="implement appropriate cybersecurity measures including defences against data/model poisoning and adversarial attacks",
        object="cybersecurity defences",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.95,
        citations=[_cite(4, "a", quote="technical solutions aimed at ensuring the cybersecurity of high-risk AI systems")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-015-05-001",
        clause_id=_cid(5),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system with continuous learning",
        action="address feedback loop risks with appropriate mitigation",
        object="feedback loop mitigation",
        conditions=[Condition(description="System continues to learn after placement on market")],
        scope="Continuous-learning high-risk AI systems",
        confidence=0.85,
        citations=[_cite(5, quote="eliminate or reduce as far as possible the risk of possibly biased outputs influencing input for future operations")],
    ),
    Requirement(
        id="REQ-EU-AI-ACT-015-01-002",
        clause_id=_cid(1),
        modality=Modality.MUST,
        subject="Provider of high-risk AI system",
        action="ensure accuracy, robustness and cybersecurity are maintained throughout lifecycle",
        object="lifecycle consistency",
        scope="High-risk AI systems under EU AI Act",
        confidence=0.90,
        citations=[_cite(1, quote="perform consistently in those respects throughout their lifecycle")],
    ),
]

# ---------------------------------------------------------------------------
# Rules & evaluation functions
# ---------------------------------------------------------------------------

def _eval_accuracy_documented(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("accuracy_metrics_documented", False) else "fail"

def _eval_accuracy_declared(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    levels = profile.get("accuracy_levels_declared", "")
    return "pass" if levels else "fail"

def _eval_disaggregated_metrics(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("disaggregated_performance_metrics", False) else "fail"

def _eval_robustness_measures(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    measures = profile.get("robustness_measures", [])
    return "pass" if len(measures) >= 1 else "fail"

def _eval_robustness_technical(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    measures = profile.get("robustness_measures", [])
    return "pass" if len(measures) >= 2 else "fail"

def _eval_adversarial_resilience(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    return "pass" if profile.get("adversarial_testing_performed", False) else "fail"

def _eval_cybersecurity(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    measures = profile.get("cybersecurity_measures", [])
    return "pass" if len(measures) >= 2 else "fail"

def _eval_feedback_loops(profile: dict) -> str:
    if not profile.get("is_high_risk", False):
        return "not_applicable"
    extra = profile.get("extra", {})
    if not extra.get("continuous_learning", False):
        return "not_applicable"
    return "pass" if extra.get("feedback_loop_mitigation", False) else "fail"


RULES: list[Rule] = [
    Rule(
        id="RULE-EU-AI-ACT-015-01-001",
        requirement_id="REQ-EU-AI-ACT-015-01-001",
        rule_type=RuleType.AUTOMATED,
        title="Accuracy metrics must be documented",
        description="Verify that accuracy metrics have been documented demonstrating appropriate accuracy levels.",
        inputs_needed=["is_high_risk", "accuracy_metrics_documented"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif accuracy_metrics_documented: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Document accuracy metrics with benchmarks demonstrating appropriate performance levels.",
        test_cases=[
            TestCase(id="TC-015-01-P", description="Metrics documented", input_data={"is_high_risk": True, "accuracy_metrics_documented": True}, expected_result="pass"),
            TestCase(id="TC-015-01-F", description="No metrics", input_data={"is_high_risk": True, "accuracy_metrics_documented": False}, expected_result="fail"),
        ],
        citations=[_cite(1, quote="achieve an appropriate level of accuracy")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-015-02-001",
        requirement_id="REQ-EU-AI-ACT-015-02-001",
        rule_type=RuleType.AUTOMATED,
        title="Accuracy levels must be declared in instructions",
        description="Verify that accuracy levels and relevant metrics are declared in the instructions of use.",
        inputs_needed=["is_high_risk", "accuracy_levels_declared"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif accuracy_levels_declared: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Declare specific accuracy levels and metrics in the instructions for use.",
        test_cases=[
            TestCase(id="TC-015-02-P", description="Levels declared", input_data={"is_high_risk": True, "accuracy_levels_declared": "Precision: 0.91, Recall: 0.88"}, expected_result="pass"),
            TestCase(id="TC-015-02-F", description="Not declared", input_data={"is_high_risk": True, "accuracy_levels_declared": ""}, expected_result="fail"),
        ],
        citations=[_cite(2, quote="levels of accuracy and the relevant accuracy metrics shall be declared")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-015-02A-001",
        requirement_id="REQ-EU-AI-ACT-015-02A-001",
        rule_type=RuleType.AUTOMATED,
        title="Disaggregated performance metrics must be provided",
        description="Verify that accuracy is measured using disaggregated metrics across relevant demographic groups.",
        inputs_needed=["is_high_risk", "disaggregated_performance_metrics"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif disaggregated_performance_metrics: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Measure and declare accuracy using disaggregated metrics across relevant demographic groups.",
        test_cases=[
            TestCase(id="TC-015-2A-P", description="Disaggregated metrics", input_data={"is_high_risk": True, "disaggregated_performance_metrics": True}, expected_result="pass"),
            TestCase(id="TC-015-2A-F", description="No disaggregated metrics", input_data={"is_high_risk": True, "disaggregated_performance_metrics": False}, expected_result="fail"),
        ],
        citations=[_cite(2, "a", quote="accuracy shall be measured and declared using disaggregated metrics")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-015-03-001",
        requirement_id="REQ-EU-AI-ACT-015-03-001",
        rule_type=RuleType.AUTOMATED,
        title="Robustness measures must be implemented",
        description="Verify that the system has robustness measures against errors, faults and inconsistencies.",
        inputs_needed=["is_high_risk", "robustness_measures"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif len(measures)>=1: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Implement robustness measures such as input validation, error handling, and redundancy.",
        test_cases=[
            TestCase(id="TC-015-03-P", description="Robustness present", input_data={"is_high_risk": True, "robustness_measures": ["input validation"]}, expected_result="pass"),
            TestCase(id="TC-015-03-F", description="No robustness", input_data={"is_high_risk": True, "robustness_measures": []}, expected_result="fail"),
        ],
        citations=[_cite(3, quote="resilient as possible regarding errors, faults or inconsistencies")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-015-03A-001",
        requirement_id="REQ-EU-AI-ACT-015-03A-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Technical and organisational robustness measures must be taken",
        description="Verify that technical and organisational measures ensure robustness including redundancy.",
        inputs_needed=["is_high_risk", "robustness_measures"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif len(measures)>=2: result='pass'\nelse: result='fail'",
        severity=Severity.MEDIUM,
        remediation="Implement both technical and organisational robustness measures including redundancy solutions.",
        test_cases=[
            TestCase(id="TC-015-3A-P", description="Multiple measures", input_data={"is_high_risk": True, "robustness_measures": ["input validation", "failover"]}, expected_result="pass"),
            TestCase(id="TC-015-3A-F", description="Insufficient measures", input_data={"is_high_risk": True, "robustness_measures": ["input validation"]}, expected_result="fail"),
        ],
        citations=[_cite(3, "a", quote="Technical and organisational measures shall be taken")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-015-04-001",
        requirement_id="REQ-EU-AI-ACT-015-04-001",
        rule_type=RuleType.AUTOMATED,
        title="Adversarial testing must be performed",
        description="Verify that the system has been tested for resilience against unauthorized manipulation.",
        inputs_needed=["is_high_risk", "adversarial_testing_performed"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif adversarial_testing_performed: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Perform adversarial testing to validate resilience against unauthorized third party manipulation.",
        test_cases=[
            TestCase(id="TC-015-04-P", description="Testing done", input_data={"is_high_risk": True, "adversarial_testing_performed": True}, expected_result="pass"),
            TestCase(id="TC-015-04-F", description="No testing", input_data={"is_high_risk": True, "adversarial_testing_performed": False}, expected_result="fail"),
        ],
        citations=[_cite(4, quote="resilient against attempts by unauthorised third parties")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-015-04A-001",
        requirement_id="REQ-EU-AI-ACT-015-04A-001",
        rule_type=RuleType.AUTOMATED,
        title="Cybersecurity measures must be appropriate",
        description="Verify that cybersecurity measures are implemented including defences against data/model poisoning and adversarial attacks.",
        inputs_needed=["is_high_risk", "cybersecurity_measures"],
        evaluation_logic="if not is_high_risk: result='not_applicable'\nelif len(measures)>=2: result='pass'\nelse: result='fail'",
        severity=Severity.CRITICAL,
        remediation="Implement comprehensive cybersecurity measures covering data poisoning, model poisoning, adversarial examples, and confidentiality attacks.",
        test_cases=[
            TestCase(id="TC-015-4A-P", description="Security present", input_data={"is_high_risk": True, "cybersecurity_measures": ["input sanitization", "access control"]}, expected_result="pass"),
            TestCase(id="TC-015-4A-F", description="Insufficient security", input_data={"is_high_risk": True, "cybersecurity_measures": ["access control"]}, expected_result="fail"),
        ],
        citations=[_cite(4, "a", quote="technical solutions aimed at ensuring the cybersecurity")],
    ),
    Rule(
        id="RULE-EU-AI-ACT-015-05-001",
        requirement_id="REQ-EU-AI-ACT-015-05-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Feedback loop risks must be mitigated for continuous learning systems",
        description="Verify that continuous learning systems address feedback loop risks with mitigation measures.",
        inputs_needed=["is_high_risk", "extra.continuous_learning", "extra.feedback_loop_mitigation"],
        evaluation_logic="if not continuous_learning: result='not_applicable'\nelif mitigation: result='pass'\nelse: result='fail'",
        severity=Severity.HIGH,
        remediation="Implement feedback loop mitigation such as data drift monitoring, output monitoring, and retraining safeguards.",
        test_cases=[
            TestCase(id="TC-015-05-P", description="Mitigation present", input_data={"is_high_risk": True, "extra": {"continuous_learning": True, "feedback_loop_mitigation": True}}, expected_result="pass"),
            TestCase(id="TC-015-05-NA", description="Not continuous", input_data={"is_high_risk": True, "extra": {"continuous_learning": False}}, expected_result="not_applicable"),
        ],
        citations=[_cite(5, quote="feedback loops are duly addressed with appropriate mitigation measures")],
    ),
]

EVALUATION_FUNCTIONS: dict[str, callable] = {
    "RULE-EU-AI-ACT-015-01-001": _eval_accuracy_documented,
    "RULE-EU-AI-ACT-015-02-001": _eval_accuracy_declared,
    "RULE-EU-AI-ACT-015-02A-001": _eval_disaggregated_metrics,
    "RULE-EU-AI-ACT-015-03-001": _eval_robustness_measures,
    "RULE-EU-AI-ACT-015-03A-001": _eval_robustness_technical,
    "RULE-EU-AI-ACT-015-04-001": _eval_adversarial_resilience,
    "RULE-EU-AI-ACT-015-04A-001": _eval_cybersecurity,
    "RULE-EU-AI-ACT-015-05-001": _eval_feedback_loops,
}
