from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.schemas.assessment import (
    AssessmentRequest,
    AssessmentResponse,
    KaggleAssessmentRequest,
    KaggleAssessmentResponse,
)
from backend.services.assessment_service import AssessmentService
from backend.services.model_loader import KaggleGrammarModels

router = APIRouter(prefix="/assessment", tags=["assessment"])
service = AssessmentService()
kaggle_models = KaggleGrammarModels(Path(__file__).parents[1] / "models")


@router.get("/questions")
def get_questions() -> dict[str, object]:
    return service.questions()


@router.post("", response_model=AssessmentResponse)
def submit_assessment(payload: AssessmentRequest) -> AssessmentResponse:
    if payload.language != "English":
        raise HTTPException(
            status_code=422,
            detail="English is the only functional assessment language right now.",
        )
    try:
        return service.evaluate(payload)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/kaggle", response_model=KaggleAssessmentResponse)
def submit_kaggle_assessment(payload: KaggleAssessmentRequest) -> KaggleAssessmentResponse:
    if not kaggle_models.available:
        raise HTTPException(
            status_code=503,
            detail=(
                "Kaggle models are unavailable. Place grammar_category_model.joblib "
                "and grammar_score_model.joblib in backend/models."
            ),
        )

    grammar_category = kaggle_models.category.model.predict([payload.sentence])[0]
    grammar_score = kaggle_models.score.model.predict(
        [[payload.target_category, payload.error_type]]
    )[0]
    grammar_score = max(0, min(100, float(grammar_score)))
    return KaggleAssessmentResponse(
        grammar_category=str(grammar_category),
        grammar_score=round(grammar_score, 2),
    )
