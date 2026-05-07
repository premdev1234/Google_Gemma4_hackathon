# =========================================================
# GEMMA SERVICE
# =========================================================

import ollama
import json
from datetime import datetime
from typing import Dict, Any
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

# =========================================================
# MODEL CONFIG
# =========================================================

MODEL_NAME = "gemma4:e2b"

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are Cognitive Twin AI.

Your role:
- Analyze cognitive behavior
- Detect contradictions
- Evaluate reasoning quality
- Generate adaptive follow-up questions
- Recommend engineering career domains
- Provide explainable reasoning

Always:
- Think analytically
- Be structured
- Be psychologically aware
- Give concise but intelligent responses
"""

# =========================================================
# GENERATE RESPONSE
# =========================================================

# =========================================================
# GENERATE RESPONSE
# =========================================================


def generate_response(user_prompt: str) -> Dict[str, Any]:

    try:

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        print("\nFULL OLLAMA RESPONSE:\n")
        print(response)

        content = response.get("message", {}).get("content", "").strip()

        if not content:

            content = "Gemma returned empty response."

        return {
            "status": "success",
            "response": content,
            "model": MODEL_NAME,
        }

    except Exception as e:

        print("\nERROR:\n")
        print(str(e))

        return {
            "status": "error",
            "message": str(e),
        }


# =========================================================
# COGNITIVE ANALYSIS
# =========================================================

# =========================================================
# COGNITIVE PROFILE ANALYSIS
# =========================================================

# =========================================================
# COGNITIVE PROFILE ANALYSIS
# =========================================================


def analyze_cognitive_profile(
    user_data: dict,
) -> Dict[str, Any]:

    # -----------------------------------------------------
    # EXTRACT DATA
    # -----------------------------------------------------

    traits = user_data.get(
        "traits",
        {},
    )

    behavioral_analysis = user_data.get(
        "behavioral_analysis",
        {},
    )

    contradiction_analysis = user_data.get(
        "contradiction_analysis",
        {},
    )

    # -----------------------------------------------------
    # EXTRACT BEHAVIORAL SCORES
    # -----------------------------------------------------

    hesitation_score = behavioral_analysis.get(
        "hesitation_score",
        0.0,
    )

    confidence_score = behavioral_analysis.get(
        "confidence_score",
        0.0,
    )

    focus_score = behavioral_analysis.get(
        "focus_score",
        0.0,
    )

    behavioral_risk = behavioral_analysis.get(
        "behavioral_risk",
        0.0,
    )

    behavior_summary = behavioral_analysis.get(
        "behavior_summary",
        "No behavioral summary available.",
    )

    # -----------------------------------------------------
    # EXTRACT CONTRADICTION DATA
    # -----------------------------------------------------

    contradiction_severity = contradiction_analysis.get(
        "contradiction_severity",
        0.0,
    )

    contradiction_summary = contradiction_analysis.get(
        "contradiction_summary",
        "No contradictions detected.",
    )

    followup_trigger = contradiction_analysis.get(
        "followup_trigger",
        {},
    )

    # -----------------------------------------------------
    # BUILD GEMMA PROMPT
    # -----------------------------------------------------

    prompt = f"""
    Analyze this user's cognitive profile.

    =====================================
    USER TRAITS
    =====================================

    {json.dumps(traits, indent=2)}

    =====================================
    BEHAVIORAL ANALYSIS
    =====================================

    Hesitation Score:
    {hesitation_score}

    Confidence Score:
    {confidence_score}

    Focus Score:
    {focus_score}

    Behavioral Risk:
    {behavioral_risk}

    Behavior Summary:
    {behavior_summary}

    =====================================
    CONTRADICTION ANALYSIS
    =====================================

    Contradiction Severity:
    {contradiction_severity}

    Contradiction Summary:
    {contradiction_summary}

    Follow-up Trigger:
    {json.dumps(followup_trigger, indent=2)}

    =====================================
    TASK
    =====================================

    Generate:

    1. Top strengths
    2. Weaknesses
    3. Cognitive risks
    4. Best engineering domains
    5. Burnout probability
    6. Learning recommendations
    7. Psychological interpretation
    8. Confidence analysis
    9. Contradiction interpretation
    10. Need for adaptive follow-up

    Be analytical, structured,
    psychologically aware,
    and concise.
    """

    # -----------------------------------------------------
    # SEND TO GEMMA
    # -----------------------------------------------------

    result = generate_response(prompt)

    # -----------------------------------------------------
    # ATTACH ANALYSIS
    # -----------------------------------------------------

    result["behavioral_analysis"] = behavioral_analysis

    result["contradiction_analysis"] = contradiction_analysis

    return result


# =========================================================
# FOLLOW-UP QUESTION GENERATION
# =========================================================


def generate_followup_question(context_data: dict):

    prompt = f"""
    Generate ONE intelligent follow-up question.

    Context:
    {json.dumps(context_data, indent=2)}

    Goal:
    - clarify ambiguity
    - probe reasoning
    - detect true cognitive behavior

    Rules:
    - natural tone
    - psychologically intelligent
    - concise
    - high signal question
    """

    return generate_response(prompt)


# =========================================================
# DOMAIN RECOMMENDATION
# =========================================================


def recommend_engineering_domain(user_profile: dict):

    prompt = f"""
    Recommend the best engineering domain.

    User Profile:
    {json.dumps(user_profile, indent=2)}

    Consider:
    - analytical thinking
    - persistence
    - systems thinking
    - creativity
    - stress tolerance
    - behavioral signals

    Return:
    1. Best domain
    2. Why
    3. Growth potential
    4. Difficulty level
    5. Suggested roadmap
    """

    return generate_response(prompt)


# =========================================================
# GENERATE DYNAMIC QUESTION
# =========================================================


def generate_dynamic_question(
    traits: dict,
    behavioral_analysis: dict,
    contradiction_analysis: dict,
):

    # -----------------------------------------------------
    # BUILD PROMPT
    # -----------------------------------------------------

    prompt = f"""
    You are an adaptive cognitive interviewer.

    =====================================
    USER TRAITS
    =====================================

    {json.dumps(traits, indent=2)}

    =====================================
    BEHAVIORAL ANALYSIS
    =====================================

    {json.dumps(behavioral_analysis, indent=2)}

    =====================================
    CONTRADICTION ANALYSIS
    =====================================

    {json.dumps(contradiction_analysis, indent=2)}

    =====================================
    TASK
    =====================================

    Generate ONE intelligent follow-up
    question.

    Goal:
    - clarify contradictions
    - probe reasoning depth
    - test confidence
    - evaluate cognitive behavior

    Rules:
    - natural conversational tone
    - psychologically intelligent
    - concise
    - high signal question
    - avoid generic interview questions

    Return ONLY the question.
    """

    # -----------------------------------------------------
    # SEND TO GEMMA
    # -----------------------------------------------------

    result = generate_response(prompt)

    return result


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    sample_user = {
        "traits": {
            "analytical_thinking": 0.91,
            "persistence": 0.87,
            "systems_thinking": 0.82,
            "stress_tolerance": 0.45,
        },
        "behavior": {
            "average_response_time": 25,
            "answer_change_count": 4,
            "inactivity_time": 14,
            "tab_switch_count": 3,
        },
        "responses": [
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
        ],
    }

    result = analyze_cognitive_profile(sample_user)

    print("\n====================================")
    print("COGNITIVE ANALYSIS")
    print("====================================\n")

    print(result)
