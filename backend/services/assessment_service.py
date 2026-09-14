from backend.schemas.assessment import AssessmentRequest, AssessmentResponse
from backend.services.grammar_service import QUESTION_BANK, GrammarService
from backend.services.recommendation_service import build_recommendations
from backend.services.writing_service import WritingService


def level_for_score(score: int) -> str:
    if score < 30:
        return "A1 - Beginner"
    if score < 45:
        return "A2 - Elementary"
    if score < 65:
        return "B1 - Intermediate"
    if score < 80:
        return "B2 - Upper Intermediate"
    return "C1 - Advanced"


class AssessmentService:
    def __init__(self) -> None:
        self.grammar = GrammarService()
        self.writing = WritingService()
        self.public_questions = [
            {key: value for key, value in question.items() if key != "answer"}
            for question in QUESTION_BANK
        ]

    def evaluate(self, payload: AssessmentRequest) -> AssessmentResponse:
        grammar_score, topic_scores = self.grammar.score(payload.grammar_answers)
        writing_score, _ = self.writing.score(payload.writing_response)
        overall_score = round(grammar_score * 0.55 + writing_score * 0.45)
        strengths, areas, recommendations = build_recommendations(grammar_score, writing_score, topic_scores)
        statuses = {self.grammar.model.status, self.writing.model.status}
        return AssessmentResponse(
            grammar_score=grammar_score,
            writing_score=writing_score,
            overall_score=overall_score,
            level=level_for_score(overall_score),
            recommendations=recommendations,
            strengths=strengths,
            areas_to_improve=areas,
            model_status="; ".join(sorted(statuses)),
        )
