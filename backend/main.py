from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

# Support both `uvicorn main:app` from backend/ and `uvicorn backend.main:app`
# from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.api.assessment import router as assessment_router
from backend.api.health import router as health_router

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"


def load_optional_model(path: Path):
    try:
        return joblib.load(path)
    except (FileNotFoundError, ImportError, OSError, ValueError):
        return None


app = FastAPI(
    title="LanguaScore API",
    description="AI-powered language assessment backend",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(assessment_router, prefix="/api")
app.include_router(health_router, prefix="/api")

grammar_category_model = load_optional_model(
    MODELS_DIR / "grammar_category_model.joblib"
)
grammar_score_model = load_optional_model(
    MODELS_DIR / "grammar_score_model.joblib"
)


class GrammarInput(BaseModel):
    sentence: str


@app.get("/")
def home():
    return {
        "message": "LanguaScore API is running"
    }


@app.post("/predict-grammar")
def predict_grammar(data: GrammarInput):
    if grammar_category_model is None or grammar_score_model is None:
        return {
            "error": "Model files are missing. Place grammar_category_model.joblib and grammar_score_model.joblib in C:/Users/DELL/Downloads/Create/models/"
        }

    sentence = data.sentence.strip()

    if not sentence:
        return {
            "error": "Sentence cannot be empty"
        }

    predicted_category = grammar_category_model.predict([sentence])[0]
    predicted_score = grammar_score_model.predict([sentence])[0]
    predicted_score = float(predicted_score) * 100
    predicted_score = np.clip(predicted_score, 0, 100)

    return {
        "sentence": sentence,
        "grammar_category": str(predicted_category),
        "grammar_score": round(float(predicted_score), 2)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)