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


def analyze_cognitive_profile(user_data: dict) -> Dict[str, Any]:

    # -----------------------------------------------------
    # EXTRACT BEHAVIOR DATA
    # -----------------------------------------------------

    behavior = user_data.get("behavior", {})

    response_time = behavior.get(
        "average_response_time",
        0,
    )

    answer_changes = behavior.get(
        "answer_change_count",
        0,
    )

    inactivity_time = behavior.get(
        "inactivity_time",
        0,
    )

    tab_switches = behavior.get(
        "tab_switch_count",
        0,
    )

    # -----------------------------------------------------
    # CALCULATE BEHAVIORAL SCORES
    # -----------------------------------------------------

    hesitation_score = calculate_hesitation_score(
        response_time=response_time,
        answer_changes=answer_changes,
        inactivity_time=inactivity_time,
    )

    confidence_score = calculate_confidence_score(
        hesitation_score=hesitation_score,
        answer_changes=answer_changes,
    )

    focus_score = calculate_focus_score(
        tab_switches=tab_switches,
        inactivity_time=inactivity_time,
    )

    behavioral_risk = calculate_behavioral_risk(
        hesitation_score=hesitation_score,
        confidence_score=confidence_score,
        focus_score=focus_score,
    )

    # -----------------------------------------------------
    # EXTRACT QUESTION RESPONSES
    # -----------------------------------------------------

    responses = user_data.get("responses", [])

    # -----------------------------------------------------
    # CONTRADICTION ANALYSIS
    # -----------------------------------------------------

    contradictions = detect_contradictions(responses)

    contradiction_severity = calculate_contradiction_severity(contradictions)

    contradiction_summary = generate_contradiction_summary(contradictions)

    followup_trigger = generate_followup_trigger(contradiction_severity)
    # -----------------------------------------------------
    # GENERATE HUMAN SUMMARY
    # -----------------------------------------------------

    behavior_summary = generate_behavior_summary(
        hesitation_score=hesitation_score,
        confidence_score=confidence_score,
        focus_score=focus_score,
        behavioral_risk=behavioral_risk,
    )

    # -----------------------------------------------------
    # BUILD GEMMA PROMPT
    # -----------------------------------------------------

    prompt = f"""
    Analyze this user's cognitive profile.

    =====================================
    USER TRAITS
    =====================================

    {json.dumps(user_data.get("traits", {}), indent=2)}

    =====================================
    BEHAVIORAL ANALYSIS
    =====================================

    Hesitation Score: {hesitation_score}

    Confidence Score: {confidence_score}

    Focus Score: {focus_score}

    Behavioral Risk: {behavioral_risk}

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
    {followup_trigger}
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

    Be analytical and structured.
    """

    # -----------------------------------------------------
    # SEND TO GEMMA
    # -----------------------------------------------------

    result = generate_response(prompt)

    # -----------------------------------------------------
    # ATTACH BEHAVIORAL DATA
    # -----------------------------------------------------

    result["behavioral_analysis"] = {
        "hesitation_score": hesitation_score,
        "confidence_score": confidence_score,
        "focus_score": focus_score,
        "behavioral_risk": behavioral_risk,
        "behavior_summary": behavior_summary,
    }
    # -----------------------------------------------------
    # ATTACH CONTRADICTION ANALYSIS
    # -----------------------------------------------------

    result["contradiction_analysis"] = {
        "contradictions": contradictions,
        "contradiction_severity": contradiction_severity,
        "contradiction_summary": contradiction_summary,
        "followup_trigger": followup_trigger,
    }
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
