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
    grammar_answers: list[GrammarAnswer] = Field(min_length=10, max_length=10)
    writing_response: str = Field(min_length=1, max_length=5000)

    @field_validator("language")
    @classmethod
    def normalize_language(cls, value: str) -> str:
        return value.strip().title()

    @field_validator("writing_response")
    @classmethod
    def normalize_writing(cls, value: str) -> str:
        normalized = value.strip()
        word_count = len(normalized.split())
        if word_count < 100 or word_count > 150:
            raise ValueError("Writing response must contain between 100 and 150 words")
        return normalized


class KaggleAssessmentRequest(BaseModel):
    sentence: str = Field(min_length=1, max_length=5000)
    target_category: str = Field(min_length=1, max_length=100)
    error_type: str = Field(min_length=1, max_length=100)


class GrammarInput(BaseModel):
    sentence: str = Field(min_length=1, max_length=5000)

    @field_validator("sentence")
    @classmethod
    def normalize_sentence(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Sentence cannot be empty")
        return normalized


class KaggleAssessmentResponse(BaseModel):
    grammar_category: str
    grammar_score: float = Field(ge=0, le=100)


class AssessmentResponse(BaseModel):
    grammar_score: int = Field(ge=0, le=100)
    grammar_category: str
    writing_score: int = Field(ge=0, le=100)
    overall_score: int = Field(ge=0, le=100)
    level: str
    recommendations: list[str]
    strengths: list[str]
    areas_to_improve: list[str]
    model_status: str
