import random
from pathlib import Path

from backend.schemas.assessment import AssessmentRequest, AssessmentResponse
from backend.services.grammar_service import QUESTION_BANK, GrammarService
from backend.services.language_question_banks import LANGUAGE_QUESTION_BANKS, LANGUAGE_WRITING_PROMPTS
from backend.services.recommendation_service import build_recommendations
from backend.services.writing_service import WritingService
from backend.services.model_loader import KaggleGrammarModels


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
        self.kaggle_grammar = KaggleGrammarModels(
            Path(__file__).parents[1] / "models"
        )

    def questions(self, language: str = "English") -> dict[str, object]:
        selected_questions = self.grammar.select_questions(language)
        writing_question = random.choice(WRITING_QUESTION_BANK)
        if language in LANGUAGE_WRITING_PROMPTS:
            writing_question = {
                "id": f"writing_{language.lower()}_prompt",
                "topic": "Writing",
                "prompt": random.choice(LANGUAGE_WRITING_PROMPTS[language]),
            }
        return {
            "language": language,
            "questions": [
                {key: value for key, value in question.items() if key != "answer"}
                for question in selected_questions
            ],
            "writing_question": writing_question,
        }

    def evaluate(self, payload: AssessmentRequest) -> AssessmentResponse:
        quiz_grammar_score, topic_scores = self.grammar.score(payload.grammar_answers, payload.language)
        writing_score, _ = self.writing.score(payload.writing_response)
        grammar_category = "Model unavailable"
        grammar_score = quiz_grammar_score
        if self.kaggle_grammar.available:
            grammar_category, model_grammar_score = self.kaggle_grammar.predict_sentence(
                payload.writing_response
            )
            grammar_score = round((quiz_grammar_score + model_grammar_score) / 2)
        overall_score = round(grammar_score * 0.55 + writing_score * 0.45)
        strengths, areas, recommendations = build_recommendations(grammar_score, writing_score, topic_scores)
        statuses = {
            self.grammar.model.status,
            self.writing.model.status,
            self.kaggle_grammar.category.status,
            self.kaggle_grammar.score.status,
        }
        return AssessmentResponse(
            grammar_score=grammar_score,
            grammar_category=grammar_category,
            writing_score=writing_score,
            overall_score=overall_score,
            level=level_for_score(overall_score),
            recommendations=recommendations,
            strengths=strengths,
            areas_to_improve=areas,
            model_status="; ".join(sorted(statuses)),
        )
