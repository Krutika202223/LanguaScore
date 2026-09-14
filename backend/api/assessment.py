from fastapi import APIRouter, HTTPException

from backend.schemas.assessment import AssessmentRequest, AssessmentResponse
from backend.services.assessment_service import AssessmentService

router = APIRouter(prefix="/assessment", tags=["assessment"])
service = AssessmentService()


@router.get("/questions")
def get_questions() -> dict[str, object]:
    return {"language": "English", "questions": service.public_questions}


@router.post("", response_model=AssessmentResponse)
def submit_assessment(payload: AssessmentRequest) -> AssessmentResponse:
    if payload.language != "English":
        raise HTTPException(
            status_code=422,
            detail="English is the only functional assessment language right now.",
        )
    return service.evaluate(payload)
