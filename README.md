# Training workspace

Use this directory for Kaggle-export preparation and model-training scripts. Training is intentionally separate from the FastAPI prediction services.

Recommended exports:

- `backend/models/grammar_model.joblib`
- `backend/models/writing_model.joblib`

Keep preprocessing objects inside the exported scikit-learn pipelines so inference uses the same transformations as training.