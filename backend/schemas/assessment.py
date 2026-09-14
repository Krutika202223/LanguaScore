from pydantic import BaseModel, Field, field_validator


class GrammarAnswer(BaseModel):
    question_id: str = Field(min_length=1, max_length=40)
    answer: str = Field(min_length=1, max_length=1)

    @field_validator("answer")
    @classmethod
    def answer_is_option(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in {"A", "B", "C", "D"}:
            raise ValueError("Answer must be A, B, C, or D")
        return normalized


class AssessmentRequest(BaseModel):
    language: str = Field(min_length=1, max_length=40)
    grammar_answers: list[GrammarAnswer] = Field(min_length=1, max_length=30)
    writing_response: str = Field(min_length=1, max_length=5000)

    @field_validator("language")
    @classmethod
    def normalize_language(cls, value: str) -> str:
        return value.strip().title()

    @field_validator("writing_response")
    @classmethod
    def normalize_writing(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized.split()) < 20:
            raise ValueError("Writing response must contain at least 20 words")
        return normalized


class AssessmentResponse(BaseModel):
    grammar_score: int = Field(ge=0, le=100)
    writing_score: int = Field(ge=0, le=100)
    overall_score: int = Field(ge=0, le=100)
    level: str
    recommendations: list[str]
    strengths: list[str]
    areas_to_improve: list[str]
    model_status: str
