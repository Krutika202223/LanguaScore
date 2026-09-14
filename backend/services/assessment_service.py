import random

from backend.schemas.assessment import AssessmentRequest, AssessmentResponse
from backend.services.grammar_service import QUESTION_BANK, GrammarService
from backend.services.recommendation_service import build_recommendations
from backend.services.writing_service import WritingService


WRITING_QUESTION_BANK = [
    {
        "id": "writing_daily_routine",
        "topic": "Daily Routine",
        "prompt": "Write 100-150 words about your daily routine. Include details about what you do, when you do it, and how you feel about it.",
    },
    {
        "id": "writing_college_life",
        "topic": "College Life",
        "prompt": "Write 100-150 words about your college life, including your classes, friends, and activities.",
    },
    {
        "id": "writing_hobbies",
        "topic": "Hobbies",
        "prompt": "Write 100-150 words about your favorite hobbies and explain why you enjoy them.",
    },
    {
        "id": "writing_memorable_experience",
        "topic": "Memorable Experience",
        "prompt": "Write 100-150 words about a memorable experience in your life.",
    },
    {
        "id": "writing_future_goals",
        "topic": "Future Goals",
        "prompt": "Write 100-150 words about your future goals and how you plan to achieve them.",
    },
    {
        "id": "writing_technology",
        "topic": "Technology",
        "prompt": "Write 100-150 words about how technology affects your daily life.",
    },
    {
        "id": "writing_favorite_place",
        "topic": "A Place You Like",
        "prompt": "Write 100-150 words about a place you enjoy visiting and explain why you like it.",
    },
]


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

    def questions(self) -> dict[str, object]:
        selected_questions = self.grammar.select_questions()
        return {
            "language": "English",
            "questions": [
                {key: value for key, value in question.items() if key != "answer"}
                for question in selected_questions
            ],
            "writing_question": random.choice(WRITING_QUESTION_BANK),
        }

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
