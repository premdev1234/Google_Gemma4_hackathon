# domain_discovery_system/api/routes/static_question.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from domain_discovery_system.database.connection import get_db

from domain_discovery_system.assessment.static_question_engine import (
    get_all_active_questions,
    get_questions_by_trait,
    get_question_by_id,
)

router = APIRouter(prefix="/questions", tags=["Static Questions"])


# =========================================================
# GET ALL ACTIVE QUESTIONS
# =========================================================


@router.get("/")
def fetch_all_questions(db: Session = Depends(get_db)):

    questions = get_all_active_questions(db)

    return {
        "status": "success",
        "total_questions": len(questions),
        "data": questions,
    }


# =========================================================
# GET SINGLE QUESTION
# =========================================================


@router.get("/{question_id}")
def fetch_question_by_id(question_id: int, db: Session = Depends(get_db)):

    question = get_question_by_id(
        db=db,
        question_id=question_id,
    )

    if not question:

        return {
            "status": "error",
            "message": "Question not found",
        }

    return {
        "status": "success",
        "data": question,
    }


# =========================================================
# GET QUESTIONS BY TRAIT
# =========================================================


@router.get("/trait/{trait_id}")
def fetch_questions_by_trait(trait_id: int, db: Session = Depends(get_db)):

    questions = get_questions_by_trait(
        db=db,
        trait_id=trait_id,
    )

    return {
        "status": "success",
        "total_questions": len(questions),
        "data": questions,
    }
