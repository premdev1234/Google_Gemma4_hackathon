# =========================================================
# IMPORTS
# =========================================================

from typing import List, Dict

# =========================================================
# DETECT CONTRADICTIONS
# =========================================================


def detect_contradictions(
    responses: List[Dict],
):

    contradictions = []

    total = len(responses)

    for i in range(total):

        for j in range(i + 1, total):

            first = responses[i]
            second = responses[j]

            # Same trait
            if first["trait"] == second["trait"]:

                score_diff = abs(first["score"] - second["score"])

                # Strong contradiction
                if score_diff >= 0.6:

                    contradictions.append(
                        {
                            "trait": first["trait"],
                            "question_1": first["question"],
                            "question_2": second["question"],
                            "score_1": first["score"],
                            "score_2": second["score"],
                            "difference": round(score_diff, 2),
                        }
                    )

    return contradictions


# =========================================================
# CONTRADICTION SEVERITY
# =========================================================


def calculate_contradiction_severity(
    contradictions: List[Dict],
):

    if not contradictions:

        return 0.0

    total_difference = 0

    for contradiction in contradictions:

        total_difference += contradiction["difference"]

    severity = total_difference / len(contradictions)

    return round(min(severity, 1.0), 2)


# =========================================================
# CONTRADICTION SUMMARY
# =========================================================


def generate_contradiction_summary(
    contradictions: List[Dict],
):

    if not contradictions:

        return "No major contradictions detected."

    summary = []

    for contradiction in contradictions:

        text = (
            f"User shows conflicting "
            f"signals in trait "
            f"'{contradiction['trait']}'. "
            f"One response scored "
            f"{contradiction['score_1']} "
            f"while another scored "
            f"{contradiction['score_2']}."
        )

        summary.append(text)

    return " ".join(summary)


# =========================================================
# FOLLOW-UP TRIGGER
# =========================================================


def generate_followup_trigger(
    contradiction_severity: float,
):

    if contradiction_severity >= 0.7:

        return {
            "trigger_followup": True,
            "priority": "high",
            "reason": "High contradiction detected.",
        }

    elif contradiction_severity >= 0.4:

        return {
            "trigger_followup": True,
            "priority": "medium",
            "reason": "Moderate contradiction detected.",
        }

    else:

        return {
            "trigger_followup": False,
            "priority": "low",
            "reason": "Profile appears stable.",
        }


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    sample_responses = [
        {
            "question": "I enjoy solving difficult systems.",
            "trait": "persistence",
            "score": 0.9,
        },
        {
            "question": "I avoid mentally demanding tasks.",
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

    contradictions = detect_contradictions(sample_responses)

    severity = calculate_contradiction_severity(contradictions)

    summary = generate_contradiction_summary(contradictions)

    followup = generate_followup_trigger(severity)

    print("\n================================")
    print("CONTRADICTION ANALYSIS")
    print("================================\n")

    print("Contradictions:\n")
    print(contradictions)

    print("\nSeverity:")
    print(severity)

    print("\nSummary:")
    print(summary)

    print("\nFollow-up Trigger:")
    print(followup)
