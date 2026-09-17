from pathlib import Path
from typing import Any


class OptionalJoblibModel:
    """Loads a deployed Kaggle pipeline when one has been placed in models/."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.model: Any = None
        self.status = "deterministic response-based baseline"
        if path.exists():
            import joblib

            try:
                self.model = joblib.load(path)
            except (ImportError, OSError, ValueError):
                self.status = f"joblib model unavailable: {path.name}"
            else:
                self.status = f"joblib model loaded: {path.name}"

    @property
    def available(self) -> bool:
        return self.model is not None


class KaggleGrammarModels:
    def __init__(self, models_path: Path) -> None:
        self.category = OptionalJoblibModel(models_path / "grammar_category_model.joblib")
        self.score = OptionalJoblibModel(models_path / "grammar_score_model.joblib")

    @property
    def available(self) -> bool:
        return self.category.available and self.score.available

    def predict_sentence(self, sentence: str) -> tuple[str, float]:
        if not self.available:
            raise RuntimeError("Kaggle grammar models are unavailable")

        category = self.category.model.predict([sentence])[0]
        score = self.score.model.predict([sentence])[0]
        percentage = max(0, min(100, float(score) * 100))
        return str(category), round(percentage, 2)
