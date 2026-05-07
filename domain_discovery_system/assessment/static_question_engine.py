# domain_discovery_system/assessment_engine/static_question_engine.py

from sqlalchemy.orm import Session

from domain_discovery_system.database.models import (
    StaticQuestion,
    StaticQuestionOption,
)

# =========================================================
# GET ALL ACTIVE QUESTIONS
# =========================================================


def get_all_active_questions(db: Session):

    questions = db.query(StaticQuestion).filter(StaticQuestion.is_active == True).all()

    final_questions = []

    for question in questions:

        options = (
            db.query(StaticQuestionOption)
            .filter(StaticQuestionOption.question_id == question.id)
            .order_by(StaticQuestionOption.option_order)
            .all()
        )

        final_questions.append(
            {
                "id": question.id,
                "question_text": question.question_text,
                "question_format": question.question_format,
                "difficulty_level": question.difficulty_level,
                "estimated_time_seconds": (question.estimated_time_seconds),
                "options": [
                    {
                        "id": option.id,
                        "option_text": option.option_text,
                        "option_score": option.option_score,
                    }
                    for option in options
                ],
            }
        )

    return final_questions


# =========================================================
# GET QUESTIONS BY TRAIT
# =========================================================


def get_questions_by_trait(db: Session, trait_id: int):

    questions = (
        db.query(StaticQuestion)
        .filter(StaticQuestion.trait_id == trait_id, StaticQuestion.is_active == True)
        .all()
    )

    return questions


# =========================================================
# GET SINGLE QUESTION
# =========================================================


def get_question_by_id(db: Session, question_id: int):

    question = db.query(StaticQuestion).filter(StaticQuestion.id == question_id).first()

    if not question:
        return None

    options = (
        db.query(StaticQuestionOption)
        .filter(StaticQuestionOption.question_id == question.id)
        .all()
    )

    return {
        "id": question.id,
        "question_text": question.question_text,
        "question_format": question.question_format,
        "options": [
            {
                "id": option.id,
                "option_text": option.option_text,
                "option_score": option.option_score,
            }
            for option in options
        ],
    }
