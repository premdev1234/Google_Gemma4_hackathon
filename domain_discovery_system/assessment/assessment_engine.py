# domain_discovery_system/assessment_engine/assessment_engine.py

from sqlalchemy.orm import Session

from domain_discovery_system.database.models import (
    AssessmentSession,
    UserResponse,
    StaticQuestion,
    StaticQuestionOption,
    UserTraitScore,
)

# =========================================================
# START ASSESSMENT SESSION
# =========================================================


def start_assessment_session(db: Session, user_id: int):

    try:

        session = AssessmentSession(
            user_id=user_id,
            session_status="active",
            total_questions_answered=0,
            fatigue_level=0.0,
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        return {"status": "success", "data": session}

    except Exception as e:

        db.rollback()

        return {"status": "error", "message": str(e)}

    finally:

        pass


# =========================================================
# SAVE USER RESPONSE
# =========================================================


def save_user_response(
    db: Session,
    user_id: int,
    assessment_session_id: int,
    question_id: int,
    selected_option_ids: list,
    response_duration_seconds: float,
    answer_change_count: int = 0,
):

    try:

        response = UserResponse(
            user_id=user_id,
            assessment_session_id=assessment_session_id,
            question_source="static",
            question_id=question_id,
            selected_option_ids=selected_option_ids,
            response_duration_seconds=response_duration_seconds,
            answer_change_count=answer_change_count,
        )

        db.add(response)

        session = (
            db.query(AssessmentSession)
            .filter(AssessmentSession.id == assessment_session_id)
            .first()
        )

        if session:
            session.total_questions_answered += 1

        db.commit()
        db.refresh(response)

        return {"status": "success", "data": response}

    except Exception as e:

        db.rollback()

        return {"status": "error", "message": str(e)}

    finally:

        pass


# =========================================================
# CALCULATE TRAIT SCORES
# =========================================================


def calculate_trait_scores(
    db: Session,
    user_id: int,
    assessment_session_id: int,
):

    try:

        responses = (
            db.query(UserResponse)
            .filter(
                UserResponse.user_id == user_id,
                UserResponse.assessment_session_id == assessment_session_id,
            )
            .all()
        )

        trait_scores = {}

        for response in responses:

            question = (
                db.query(StaticQuestion)
                .filter(StaticQuestion.id == response.question_id)
                .first()
            )

            if not question:
                continue

            trait_id = question.trait_id

            trait_scores.setdefault(trait_id, [])

            for option_id in response.selected_option_ids:

                option = (
                    db.query(StaticQuestionOption)
                    .filter(StaticQuestionOption.id == option_id)
                    .first()
                )

                if option:
                    trait_scores[trait_id].append(option.option_score)

        for trait_id, scores in trait_scores.items():

            raw_score = sum(scores)

            normalized_score = raw_score / len(scores) if scores else 0

            existing_score = (
                db.query(UserTraitScore)
                .filter(
                    UserTraitScore.user_id == user_id,
                    UserTraitScore.trait_id == trait_id,
                )
                .first()
            )

            if existing_score:

                existing_score.raw_score = raw_score
                existing_score.normalized_score = normalized_score
                existing_score.confidence_score = 0.85

            else:

                db.add(
                    UserTraitScore(
                        user_id=user_id,
                        trait_id=trait_id,
                        raw_score=raw_score,
                        normalized_score=normalized_score,
                        confidence_score=0.85,
                    )
                )

        db.commit()

        return {"status": "success", "message": "Trait scores calculated"}

    except Exception as e:

        db.rollback()

        return {"status": "error", "message": str(e)}

    finally:

        pass


# =========================================================
# COMPLETE ASSESSMENT
# =========================================================


def complete_assessment(db: Session, assessment_session_id: int):

    try:

        session = (
            db.query(AssessmentSession)
            .filter(AssessmentSession.id == assessment_session_id)
            .first()
        )

        if not session:

            return {"status": "error", "message": "Session not found"}

        session.session_status = "completed"

        db.commit()

        return {"status": "success", "message": "Assessment completed"}

    except Exception as e:

        db.rollback()

        return {"status": "error", "message": str(e)}

    finally:

        pass
