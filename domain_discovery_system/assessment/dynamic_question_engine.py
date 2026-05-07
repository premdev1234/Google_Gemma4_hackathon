from domain_discovery_system.ai.gemma_service import (
    generate_dynamic_question,
)

# =========================================================
# DYNAMIC QUESTION POOL
# =========================================================
print("\ndysnamic_question_engine.py loaded\n")
QUESTION_POOL = [
    {
        "id": 1,
        "question": "How would you debug a failing " "distributed system?",
        "trait": "systems_thinking",
        "difficulty": "hard",
        "category": "technical",
        "min_confidence": 0.7,
    },
    {
        "id": 2,
        "question": "Describe a time you handled " "stress during deadlines.",
        "trait": "stress_tolerance",
        "difficulty": "medium",
        "category": "behavioral",
        "min_confidence": 0.4,
    },
    {
        "id": 3,
        "question": "Why did you change your answer " "multiple times?",
        "trait": "confidence",
        "difficulty": "easy",
        "category": "clarification",
        "min_confidence": 0.0,
    },
]

# =========================================================
# SELECT NEXT QUESTION
# =========================================================


def select_next_question(
    confidence_score: float,
    contradiction_severity: float,
    behavioral_risk: float,
):
    # -------------------------------------
    # HIGH CONTRADICTION
    # -------------------------------------

    if contradiction_severity >= 0.7:

        for question in QUESTION_POOL:

            if question["category"] == "clarification":

                return question

    # -------------------------------------
    # HIGH CONFIDENCE
    # -------------------------------------

    if confidence_score >= 0.7:

        for question in QUESTION_POOL:

            if question["difficulty"] == "hard":

                return question

    # -------------------------------------
    # HIGH BEHAVIORAL RISK
    # -------------------------------------

    if behavioral_risk >= 0.6:

        for question in QUESTION_POOL:

            if question["difficulty"] == "easy":

                return question

    # -------------------------------------
    # DEFAULT
    # -------------------------------------

    return QUESTION_POOL[1]


# =========================================================
# AI GENERATED QUESTION
# =========================================================


def generate_ai_followup(
    traits: dict,
    behavioral_analysis: dict,
    contradiction_analysis: dict,
):

    ai_question = generate_dynamic_question(
        traits=traits,
        behavioral_analysis=behavioral_analysis,
        contradiction_analysis=contradiction_analysis,
    )

    return ai_question


# =========================================================
# AI FOLLOW-UP TEST
# =========================================================

if __name__ == "__main__":

    traits = {
        "analytical_thinking": 0.91,
        "persistence": 0.87,
        "systems_thinking": 0.82,
        "stress_tolerance": 0.45,
    }

    behavioral_analysis = {
        "hesitation_score": 0.43,
        "confidence_score": 0.58,
        "focus_score": 0.78,
        "behavioral_risk": 0.36,
    }

    contradiction_analysis = {
        "contradiction_severity": 0.7,
        "contradiction_summary": "User shows conflicting " "stress tolerance patterns.",
    }

    result = generate_ai_followup(
        traits=traits,
        behavioral_analysis=behavioral_analysis,
        contradiction_analysis=contradiction_analysis,
    )

    print("\n================================")
    print("AI GENERATED QUESTION")
    print("================================\n")

    print(result)
