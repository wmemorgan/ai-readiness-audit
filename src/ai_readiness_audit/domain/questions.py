"""The banded self-assessment question set.

Each question belongs to exactly one locked dimension and offers five options, one per
band (L1..L5). The tool ingests answers to these questions — never documents or artifacts.

Question language traces to the core question of its dimension, aligned to ISO/IEC 42001
domains and NIST AI RMF / GenAI Profile risk vocabulary.
"""

from __future__ import annotations

from .models import AnswerOption, Band, Question
from .rubric import DIMENSIONS


def _q(
    qid: str, dimension_key: str, prompt: str, ladder: tuple[str, str, str, str, str]
) -> Question:
    """Build a question whose five options ascend L1..L5."""
    options = tuple(AnswerOption(band=Band(i + 1), label=label) for i, label in enumerate(ladder))
    return Question(id=qid, dimension_key=dimension_key, prompt=prompt, options=options)


QUESTIONS: tuple[Question, ...] = (
    # --- Governance & Decision Rights ---
    _q(
        "gov-1",
        "governance_decision_rights",
        "Who is accountable for AI outcomes in your organization?",
        (
            "No one is accountable; use is unsanctioned.",
            "Informal — a champion advocates, but ownership is unassigned.",
            "A named executive owns AI, documented in role charters.",
            "A named owner plus a governing body that meets on a cadence.",
            "Board-level oversight with reporting and continuous accountability.",
        ),
    ),
    _q(
        "gov-2",
        "governance_decision_rights",
        "Is there a written AI policy governing acceptable use and approval?",
        (
            "No written policy of any kind.",
            "Scattered guidance; nothing authoritative.",
            "A documented AI policy exists and is communicated.",
            "Policy is enforced with defined approval gates by risk tier.",
            "Policy is versioned, audited, and continuously improved.",
        ),
    ),
    _q(
        "gov-3",
        "governance_decision_rights",
        "How are AI initiatives approved before they ship?",
        (
            "No approval step; anyone can deploy.",
            "Ad hoc sign-off, case by case.",
            "A defined intake and approval path exists.",
            "Approval gates scale with assessed risk and blast radius.",
            "Gated approvals with post-deployment review feeding the next gate.",
        ),
    ),
    # --- Risk & Control Posture ---
    _q(
        "risk-1",
        "risk_control_posture",
        "Are AI-specific risks named (hallucination, leakage, injection, drift)?",
        (
            "Risks are not identified.",
            "A few risks are discussed informally.",
            "AI-specific risks are named and documented.",
            "Named risks are mapped to controls and owners.",
            "Risk register is live, severity-weighted, and reviewed on a cadence.",
        ),
    ),
    _q(
        "risk-2",
        "risk_control_posture",
        "Is there a human-in-the-loop gate calibrated to severity?",
        (
            "No human review of AI output.",
            "Occasional spot checks, undefined.",
            "Human review is defined for sensitive use.",
            "Review depth scales with output severity.",
            "Severity-tiered review with escalation and audit trail.",
        ),
    ),
    _q(
        "risk-3",
        "risk_control_posture",
        "How is model/output drift detected and contained?",
        (
            "Drift is neither defined nor monitored.",
            "Drift is understood as a concept only.",
            "Drift is monitored manually or periodically.",
            "Automated drift signals trigger defined responses.",
            "Continuous drift detection with rollback and containment runbooks.",
        ),
    ),
    # --- Data Readiness ---
    _q(
        "data-1",
        "data_readiness",
        "Is the data intended for AI accessible and inventoried?",
        (
            "Data location and ownership are unknown.",
            "Some sources are known but not catalogued.",
            "A data inventory exists for AI-relevant sources.",
            "Inventory includes lineage and access controls.",
            "Governed catalog with automated lineage and freshness.",
        ),
    ),
    _q(
        "data-2",
        "data_readiness",
        "Is data quality assured for the data AI will consume?",
        (
            "Quality is unmeasured.",
            "Quality issues are handled reactively.",
            "Defined quality checks run before use.",
            "Quality gates block low-quality data automatically.",
            "Continuous quality monitoring with remediation SLAs.",
        ),
    ),
    _q(
        "data-3",
        "data_readiness",
        "Are usage rights and licensing cleared for AI use of this data?",
        (
            "Rights have not been considered.",
            "Assumed acceptable; not verified.",
            "Rights are reviewed before AI use.",
            "Licensing is tracked per dataset with constraints enforced.",
            "Rights and licensing are continuously governed and auditable.",
        ),
    ),
    # --- Security & Privacy ---
    _q(
        "sec-1",
        "security_privacy",
        "How is access to AI systems and their data controlled?",
        (
            "No access controls specific to AI.",
            "Shared credentials or broad access.",
            "Role-based access is defined.",
            "Least-privilege access with periodic review.",
            "Continuously enforced least privilege with just-in-time access.",
        ),
    ),
    _q(
        "sec-2",
        "security_privacy",
        "How is PII handled in AI workflows?",
        (
            "PII exposure is not considered.",
            "Handled case by case, undocumented.",
            "PII handling rules are defined for AI use.",
            "PII is minimized, masked, or isolated by policy.",
            "Automated PII controls with monitoring and disclosure.",
        ),
    ),
    _q(
        "sec-3",
        "security_privacy",
        "Is third-party model/data processing understood and disclosed?",
        (
            "Third-party processing is unknown.",
            "Known informally; not disclosed.",
            "Processing posture is documented.",
            "Contracts and disclosures cover third-party processing.",
            "Processing is governed, disclosed, and continuously verified.",
        ),
    ),
    # --- Talent & Operating Model ---
    _q(
        "talent-1",
        "talent_operating_model",
        "Are the skills to build and run AI present or sourced?",
        (
            "No relevant skills identified.",
            "A few individuals experiment.",
            "Required skills are identified and being sourced.",
            "Build/operate/govern roles are staffed.",
            "A sustained capability with succession and development.",
        ),
    ),
    _q(
        "talent-2",
        "talent_operating_model",
        "Are build, operate, and govern responsibilities defined?",
        (
            "Responsibilities are undefined.",
            "Overlapping, informal responsibilities.",
            "Roles are defined on paper.",
            "Roles are staffed with clear handoffs.",
            "Operating model is measured and continuously improved.",
        ),
    ),
    _q(
        "talent-3",
        "talent_operating_model",
        "Who owns an AI system once it is in production?",
        (
            "No run-state owner.",
            "Ownership is ambiguous after launch.",
            "A run-state owner is named.",
            "Owner has defined runbooks and on-call.",
            "Full lifecycle ownership with SLOs and review.",
        ),
    ),
    # --- Third-Party & Concentration Risk ---
    _q(
        "tp-1",
        "third_party_concentration_risk",
        "Is your model/vendor concentration understood?",
        (
            "Dependencies are not mapped.",
            "Aware of key vendors informally.",
            "Vendor and model dependencies are documented.",
            "Concentration risk is assessed and bounded.",
            "Concentration is continuously monitored with limits.",
        ),
    ),
    _q(
        "tp-2",
        "third_party_concentration_risk",
        "Are third-party AI dependencies contractually controlled?",
        (
            "No relevant contractual terms.",
            "Standard terms; nothing AI-specific.",
            "AI-specific terms exist in key contracts.",
            "Terms cover data use, exit, and liability.",
            "Contracts are governed with active risk management.",
        ),
    ),
    _q(
        "tp-3",
        "third_party_concentration_risk",
        "How portable are you off a given model or vendor?",
        (
            "Fully locked in; no exit path.",
            "Exit is possible but unplanned.",
            "A migration path is documented.",
            "Portability is tested periodically.",
            "Abstraction and drills keep switching cost bounded.",
        ),
    ),
    # --- Measurement & Assurance ---
    _q(
        "meas-1",
        "measurement_assurance",
        "Can you evaluate the quality of AI outputs?",
        (
            "Outputs are not evaluated.",
            "Evaluated by impression, ad hoc.",
            "Defined evaluation criteria exist.",
            "An eval harness runs against real scenarios.",
            "Evaluation is continuous and severity-weighted.",
        ),
    ),
    _q(
        "meas-2",
        "measurement_assurance",
        "Do you measure the severity of failures, not just their rate?",
        (
            "Failures are not measured.",
            "Failure counts only, no severity.",
            "Severity is assessed after incidents.",
            "Severity is built into the evaluation.",
            "Severity-weighted metrics drive control changes.",
        ),
    ),
    _q(
        "meas-3",
        "measurement_assurance",
        "Do you evaluate the evaluation itself for blind spots?",
        (
            "The evaluation is not examined.",
            "Assumed adequate.",
            "Periodic review of eval coverage.",
            "Eval coverage gaps are tracked and closed.",
            "Meta-evaluation is continuous and audited.",
        ),
    ),
)


def questions_for(dimension_key: str) -> tuple[Question, ...]:
    """Return the questions belonging to one dimension, in authored order."""
    return tuple(q for q in QUESTIONS if q.dimension_key == dimension_key)


def question_ids() -> tuple[str, ...]:
    return tuple(q.id for q in QUESTIONS)


# A questionnaire covers every locked dimension with at least one question, and every
# option ascends the full L1..L5 ladder. These are invariants the domain guarantees.
def _covers_every_dimension() -> bool:
    return all(questions_for(d.key) for d in DIMENSIONS)


assert _covers_every_dimension(), "every locked dimension must carry a question set"
