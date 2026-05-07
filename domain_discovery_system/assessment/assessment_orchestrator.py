# =========================================================
# ASSESSMENT ORCHESTRATOR
# =========================================================

print("assessment_orchestrator.py loaded")

# =========================================================
# IMPORTS
# =========================================================

from domain_discovery_system.behavioral_engine.behavioral_engine import (
    calculate_hesitation_score,
    calculate_confidence_score,
    calculate_focus_score,
    calculate_behavioral_risk,
    generate_behavior_summary,
)

from domain_discovery_system.contradiction_engine.contradiction_engine import (
    detect_contradictions,
    calculate_contradiction_severity,
    generate_contradiction_summary,
    generate_followup_trigger,
)

from domain_discovery_system.assessment.dynamic_question_engine import (
    select_next_question,
    generate_ai_followup,
)

from domain_discovery_system.ai.gemma_service import (
    analyze_cognitive_profile,
)

# =========================================================
# ASSESSMENT ORCHESTRATOR CLASS
# =========================================================


class AssessmentOrchestrator:

    # -----------------------------------------------------
    # INIT
    # -----------------------------------------------------

    def __init__(self):

        self.user_profile = {}

        self.behavioral_analysis = {}

        self.contradiction_analysis = {}

        self.current_question = None

        self.session_history = []

    # -----------------------------------------------------
    # START SESSION
    # -----------------------------------------------------

    def start_assessment(self):

        print("\n================================")
        print("ASSESSMENT SESSION STARTED")
        print("================================\n")

    # -----------------------------------------------------
    # PROCESS USER RESPONSE
    # -----------------------------------------------------

    def process_user_response(
        self,
        traits: dict,
        responses: list,
        behavior_data: dict,
    ):

        # ==============================================
        # STEP 1 — BEHAVIORAL ANALYSIS
        # ==============================================

        hesitation_score = calculate_hesitation_score(
            response_time=behavior_data["average_response_time"],
            answer_changes=behavior_data["answer_change_count"],
            inactivity_time=behavior_data["inactivity_time"],
        )

        confidence_score = calculate_confidence_score(
            hesitation_score=hesitation_score,
            answer_changes=behavior_data["answer_change_count"],
        )

        focus_score = calculate_focus_score(
            tab_switches=behavior_data["tab_switch_count"],
            inactivity_time=behavior_data["inactivity_time"],
        )

        behavioral_risk = calculate_behavioral_risk(
            hesitation_score=hesitation_score,
            confidence_score=confidence_score,
            focus_score=focus_score,
        )

        behavior_summary = generate_behavior_summary(
            hesitation_score=hesitation_score,
            confidence_score=confidence_score,
            focus_score=focus_score,
            behavioral_risk=behavioral_risk,
        )

        self.behavioral_analysis = {
            "hesitation_score": hesitation_score,
            "confidence_score": confidence_score,
            "focus_score": focus_score,
            "behavioral_risk": behavioral_risk,
            "behavior_summary": behavior_summary,
        }

        # ==============================================
        # STEP 2 — CONTRADICTION ANALYSIS
        # ==============================================

        contradictions = detect_contradictions(responses)

        contradiction_severity = calculate_contradiction_severity(contradictions)

        contradiction_summary = generate_contradiction_summary(contradictions)

        followup_trigger = generate_followup_trigger(contradiction_severity)

        self.contradiction_analysis = {
            "contradictions": contradictions,
            "contradiction_severity": contradiction_severity,
            "contradiction_summary": contradiction_summary,
            "followup_trigger": followup_trigger,
        }

        # ==============================================
        # STEP 3 — UPDATE USER PROFILE
        # ==============================================

        self.user_profile = {
            "traits": traits,
            "behavior": self.behavioral_analysis,
            "contradictions": self.contradiction_analysis,
        }

        # ==============================================
        # STEP 4 — GEMMA COGNITIVE ANALYSIS
        # ==============================================

        ai_analysis = analyze_cognitive_profile(
            {
                "traits": traits,
                "behavioral_analysis": self.behavioral_analysis,
                "contradiction_analysis": self.contradiction_analysis,
            }
        )

        # ==============================================
        # STEP 5 — RULE-BASED QUESTION
        # ==============================================

        next_question = select_next_question(
            confidence_score=confidence_score,
            contradiction_severity=contradiction_severity,
            behavioral_risk=behavioral_risk,
        )

        self.current_question = next_question

        # ==============================================
        # STEP 6 — AI GENERATED FOLLOW-UP
        # ==============================================

        ai_followup = generate_ai_followup(
            traits=traits,
            behavioral_analysis=self.behavioral_analysis,
            contradiction_analysis=self.contradiction_analysis,
        )

        # ==============================================
        # STEP 7 — SAVE SESSION HISTORY
        # ==============================================

        session_data = {
            "traits": traits,
            "behavioral_analysis": self.behavioral_analysis,
            "contradiction_analysis": self.contradiction_analysis,
            "ai_analysis": ai_analysis,
            "rule_based_question": next_question,
            "ai_followup": ai_followup,
        }

        self.session_history.append(session_data)

        # ==============================================
        # RETURN COMPLETE RESULT
        # ==============================================

        return {
            "behavioral_analysis": self.behavioral_analysis,
            "contradiction_analysis": self.contradiction_analysis,
            "ai_analysis": ai_analysis,
            "rule_based_question": next_question,
            "ai_followup": ai_followup,
        }


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    orchestrator = AssessmentOrchestrator()

    orchestrator.start_assessment()

    # -----------------------------------------------------
    # SAMPLE USER TRAITS
    # -----------------------------------------------------

    traits = {
        "analytical_thinking": 0.91,
        "persistence": 0.87,
        "systems_thinking": 0.82,
        "stress_tolerance": 0.45,
    }

    # -----------------------------------------------------
    # SAMPLE RESPONSES
    # -----------------------------------------------------

    responses = [
        {
            "question": "I enjoy difficult systems.",
            "trait": "persistence",
            "score": 0.9,
        },
        {
            "question": "I avoid mentally demanding work.",
            "trait": "persistence",
            "score": 0.2,
        },
        {
            "question": "I remain calm under pressure.",
            "trait": "stress_tolerance",
            "score": 0.8,
        },
        {
            "question": "I panic during deadlines.",
            "trait": "stress_tolerance",
            "score": 0.1,
        },
    ]

    # -----------------------------------------------------
    # SAMPLE BEHAVIOR
    # -----------------------------------------------------

    behavior_data = {
        "average_response_time": 25,
        "answer_change_count": 4,
        "inactivity_time": 14,
        "tab_switch_count": 3,
    }

    # -----------------------------------------------------
    # RUN FULL PIPELINE
    # -----------------------------------------------------

    result = orchestrator.process_user_response(
        traits=traits,
        responses=responses,
        behavior_data=behavior_data,
    )

    # -----------------------------------------------------
    # DISPLAY RESULTS
    # -----------------------------------------------------

    print("\n================================")
    print("FINAL ASSESSMENT RESULT")
    print("================================\n")

    print("\nBehavioral Analysis:\n")
    print(result["behavioral_analysis"])

    print("\nContradiction Analysis:\n")
    print(result["contradiction_analysis"])

    print("\nRule-Based Question:\n")
    print(result["rule_based_question"])

    print("\nAI Follow-up:\n")
    print(result["ai_followup"])

    print("\nAI Cognitive Analysis:\n")
    print(result["ai_analysis"])
