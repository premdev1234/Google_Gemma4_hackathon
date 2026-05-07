# =========================================================
# ASSESSMENT API ROUTES
# =========================================================

print("assessment.py loaded")

# =========================================================
# IMPORTS
# =========================================================

from fastapi import APIRouter
from pydantic import BaseModel

from typing import List, Dict, Any

from domain_discovery_system.assessment.assessment_orchestrator import (
    AssessmentOrchestrator,
)

# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"],
)

# =========================================================
# ORCHESTRATOR INSTANCE
# =========================================================

orchestrator = AssessmentOrchestrator()

# =========================================================
# REQUEST MODELS
# =========================================================


class UserResponse(BaseModel):

    question: str

    trait: str

    score: float


class BehaviorData(BaseModel):

    average_response_time: float

    answer_change_count: int

    inactivity_time: float

    tab_switch_count: int


class AssessmentRequest(BaseModel):

    traits: Dict[str, float]

    responses: List[UserResponse]

    behavior_data: BehaviorData


# =========================================================
# HEALTH CHECK
# =========================================================


@router.get("/health")
def health_check():

    return {
        "status": "success",
        "message": "Assessment API working",
    }


# =========================================================
# START ASSESSMENT
# =========================================================


@router.post("/start-assessment")
def start_assessment(
    request: AssessmentRequest,
):

    try:

        # ---------------------------------------------
        # CONVERT PYDANTIC OBJECTS
        # ---------------------------------------------

        responses = [response.model_dump() for response in request.responses]

        behavior_data = request.behavior_data.model_dump()

        # ---------------------------------------------
        # RUN ORCHESTRATOR
        # ---------------------------------------------

        result = orchestrator.process_user_response(
            traits=request.traits,
            responses=responses,
            behavior_data=behavior_data,
        )

        # ---------------------------------------------
        # RETURN RESULT
        # ---------------------------------------------

        return {
            "status": "success",
            "message": "Assessment completed",
            "data": result,
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }
