import re
from collections import Counter
from pathlib import Path

from backend.services.model_loader import OptionalJoblibModel


class WritingService:
    def __init__(self) -> None:
        self.model = OptionalJoblibModel(Path(__file__).parents[1] / "models" / "writing_model.joblib")

    def score(self, text: str) -> tuple[int, dict[str, float]]:
        sentences = [part.strip() for part in re.split(r"[.!?]+", text) if part.strip()]
        words = re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)?", text.lower())
        unique_ratio = len(set(words)) / len(words) if words else 0
        average_sentence_length = len(words) / len(sentences) if sentences else 0
        sentence_starts = [sentence.split()[0].lower() for sentence in sentences if sentence.split()]
        repeated_starts = len(sentence_starts) - len(set(sentence_starts))
        sentence_variety = max(0, 1 - repeated_starts / max(1, len(sentence_starts)))
        punctuation = len(re.findall(r"[,;:]", text))
        word_length = sum(len(word) for word in words) / len(words) if words else 0
        length_fit = min(1, len(words) / 100) if len(words) < 100 else max(0.6, 1 - (len(words) - 150) / 250)

        score = (
            25 * length_fit
            + 25 * min(unique_ratio / 0.65, 1)
            + 20 * min(average_sentence_length / 18, 1)
            + 15 * sentence_variety
            + 10 * min(punctuation / max(1, len(sentences)), 1)
            + 5 * min(word_length / 6, 1)
        )
        return round(max(0, min(100, score))), {
            "word_count": float(len(words)),
            "sentence_count": float(len(sentences)),
            "vocabulary_diversity": round(unique_ratio, 3),
            "average_sentence_length": round(average_sentence_length, 1),
        }
