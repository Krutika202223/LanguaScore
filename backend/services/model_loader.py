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

            self.model = joblib.load(path)
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
