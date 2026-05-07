# =========================================================
# IMPORTS
# =========================================================

from typing import Dict

# =========================================================
# HESITATION SCORE
# =========================================================


def calculate_hesitation_score(
    response_time: float,
    answer_changes: int,
    inactivity_time: float,
):

    hesitation = 0.0
    # Response time impact
    hesitation += min(response_time / 60, 1.0) * 0.4
    # Answer changes impact
    hesitation += min(answer_changes / 10, 1.0) * 0.3
    # Inactivity impact
    hesitation += min(inactivity_time / 30, 1.0) * 0.3
    return round(min(hesitation, 1.0), 2)


# =========================================================
# CONFIDENCE SCORE
# =========================================================


def calculate_confidence_score(
    hesitation_score: float,
    answer_changes: int,
):
    confidence = 1.0
    confidence -= hesitation_score * 0.6
    confidence -= min(answer_changes / 10, 1.0) * 0.4

    return round(max(confidence, 0.0), 2)


# =========================================================
# FOCUS SCORE
# =========================================================


def calculate_focus_score(
    tab_switches: int,
    inactivity_time: float,
):
    focus = 1.0
    focus -= min(tab_switches / 15, 1.0) * 0.5
    focus -= min(inactivity_time / 60, 1.0) * 0.5
    return round(max(focus, 0.0), 2)


# =========================================================
# BEHAVIORAL RISK
# =========================================================


def calculate_behavioral_risk(
    hesitation_score: float,
    confidence_score: float,
    focus_score: float,
):
    risk = 0.0
    risk += hesitation_score * 0.4
    risk += (1 - confidence_score) * 0.3
    risk += (1 - focus_score) * 0.3
    return round(min(risk, 1.0), 2)


# =========================================================
# BEHAVIOR SUMMARY
# =========================================================
def generate_behavior_summary(
    hesitation_score: float,
    confidence_score: float,
    focus_score: float,
    behavioral_risk: float,
):
    summary = []

    # Hesitation
    if hesitation_score > 0.7:
        summary.append("User shows high hesitation and over-analysis.")
    elif hesitation_score > 0.4:
        summary.append("User shows moderate hesitation.")
    else:
        summary.append("User appears decisive.")

    # Confidence
    if confidence_score > 0.75:
        summary.append("User demonstrates strong confidence.")
    elif confidence_score > 0.5:
        summary.append("User confidence is moderate.")
    else:
        summary.append("User confidence appears unstable.")

    # Focus
    if focus_score > 0.75:
        summary.append("User maintains strong focus.")
    elif focus_score > 0.5:
        summary.append("User focus is moderately stable.")
    else:
        summary.append("User shows signs of distraction.")

    # Risk
    if behavioral_risk > 0.7:
        summary.append("High cognitive overload risk detected.")
    elif behavioral_risk > 0.4:
        summary.append("Moderate behavioral risk detected.")
    else:
        summary.append("Behavioral profile appears stable.")

    return " ".join(summary)


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":
    hesitation = calculate_hesitation_score(
        response_time=25,
        answer_changes=4,
        inactivity_time=12,
    )
    confidence = calculate_confidence_score(
        hesitation_score=hesitation,
        answer_changes=4,
    )
    focus = calculate_focus_score(
        tab_switches=3,
        inactivity_time=12,
    )
    risk = calculate_behavioral_risk(
        hesitation_score=hesitation,
        confidence_score=confidence,
        focus_score=focus,
    )
    summary = generate_behavior_summary(
        hesitation_score=hesitation,
        confidence_score=confidence,
        focus_score=focus,
        behavioral_risk=risk,
    )

    print("\n===================================")
    print("BEHAVIORAL ANALYSIS")
    print("===================================\n")

    print("Hesitation Score:", hesitation)
    print("Confidence Score:", confidence)
    print("Focus Score:", focus)
    print("Behavioral Risk:", risk)

    print("\nBehavior Summary:\n")
    print(summary)
