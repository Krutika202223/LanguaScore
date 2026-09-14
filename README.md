# LanguaScore

LanguaScore is a language proficiency assessment system, not a language-learning site. A user completes one English assessment containing grammar multiple-choice questions and one writing task. The backend scores only those submitted responses and returns grammar, writing, overall proficiency, CEFR level, strengths, and recommendations.

## Folder structure

```text
LanguaScore/
├── requirements.txt
├── backend/
│   ├── api/assessment.py
│   ├── api/health.py
│   ├── datasets/               # Training datasets, kept out of prediction
│   ├── models/                 # Place deployed joblib files here
│   ├── schemas/assessment.py
│   ├── services/
│   │   ├── assessment_service.py
│   │   ├── grammar_service.py
│   │   ├── model_loader.py
│   │   ├── recommendation_service.py
│   │   └── writing_service.py
│   ├── training/               # Kaggle/model preparation notes and scripts
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── assessment.html
│   ├── assessment.js
│   ├── index.html
│   ├── result.html
│   ├── result.js
│   └── styles.css
└── README.md
```

## Install and run

From the project root on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Open `frontend/index.html` directly in a browser, or serve the frontend with any static file server. The frontend calls the API at `http://127.0.0.1:8000/api`.

## API

Questions are available at `GET /api/assessment/questions`. Submit one assessment to `POST /api/assessment`:

```json
{
  "language": "English",
  "grammar_answers": [
    {"question_id": "q1", "answer": "B"},
    {"question_id": "q2", "answer": "B"}
  ],
  "writing_response": "I wake up early every morning and prepare breakfast before I begin my work. During the day, I focus on important tasks, speak with colleagues, and take short breaks. In the evening, I read a book, exercise, and plan the next day carefully."
}
```

The complete response has this shape:

```json
{
  "grammar_score": 50,
  "writing_score": 80,
  "overall_score": 64,
  "level": "B1 - Intermediate",
  "recommendations": ["Review tenses, articles and subject-verb agreement."],
  "strengths": ["Clear written communication"],
  "areas_to_improve": ["Core grammar accuracy"],
  "model_status": "deterministic response-based baseline"
}
```

## Scoring and ML handoff

The current implementation is intentionally transparent. Each assessment presents 10 randomly selected grammar questions from the 50-question server-owned bank, and grammar is the percentage of correct submitted answers against the server answer key. Writing is a deterministic feature score using vocabulary diversity, sentence length, sentence variety, punctuation, word length, and a soft length target; it is not based on word count alone. Overall proficiency is `55% grammar + 45% writing`.

CEFR mapping is implemented in `backend/services/assessment_service.py`:

| Score | Level |
| --- | --- |
| 0-29 | A1 - Beginner |
| 30-44 | A2 - Elementary |
| 45-64 | B1 - Intermediate |
| 65-79 | B2 - Upper Intermediate |
| 80-100 | C1 - Advanced |

Place Kaggle exports at:

```text
backend/models/grammar_category_model.joblib
backend/models/grammar_score_model.joblib
```

The Kaggle-trained models are available through `POST /api/assessment/kaggle`:

```json
{
  "sentence": "She go to school every day.",
  "target_category": "Tenses",
  "error_type": "verb agreement"
}
```

The response contains `grammar_category` and a `grammar_score` clamped to the
range 0-100. The existing `POST /api/assessment` flow remains available for
the browser assessment and uses its deterministic response-based scoring.

The assessment selects one writing task from a server-owned question bank for each server session. Responses must contain 100-150 words. The exact loading hook is `GrammarService.__init__` in `backend/services/grammar_service.py` and `WritingService.__init__` in `backend/services/writing_service.py`; both use `OptionalJoblibModel` from `backend/services/model_loader.py`. Keep preprocessing objects, such as a TF-IDF vectorizer or scaler, inside the exported sklearn pipeline so training and inference stay consistent.

Until those files exist, the API labels its output as `deterministic response-based baseline`.

## Database

No database is required for assessment or prediction. A PostgreSQL persistence layer can be added later for anonymous assessment records, but it must remain separate from the scoring services.
