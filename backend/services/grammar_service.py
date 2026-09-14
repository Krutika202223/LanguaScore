from pathlib import Path

from backend.schemas.assessment import GrammarAnswer
from backend.services.model_loader import OptionalJoblibModel


QUESTION_BANK = [
    {"id": "q1", "topic": "Tenses", "prompt": "She ___ to school every day.", "options": {"A": "go", "B": "goes", "C": "going", "D": "gone"}, "answer": "B"},
    {"id": "q2", "topic": "Articles", "prompt": "I saw ___ interesting documentary last night.", "options": {"A": "a", "B": "an", "C": "the", "D": "no article"}, "answer": "B"},
    {"id": "q3", "topic": "Prepositions", "prompt": "The meeting starts ___ nine o'clock.", "options": {"A": "in", "B": "on", "C": "at", "D": "by"}, "answer": "C"},
    {"id": "q4", "topic": "Agreement", "prompt": "The list of items ___ on the desk.", "options": {"A": "are", "B": "were", "C": "be", "D": "is"}, "answer": "D"},
    {"id": "q5", "topic": "Pronouns", "prompt": "Maria and ___ finished the project.", "options": {"A": "me", "B": "I", "C": "my", "D": "mine"}, "answer": "B"},
    {"id": "q6", "topic": "Modals", "prompt": "You ___ wear a seat belt while driving.", "options": {"A": "should", "B": "might", "C": "would", "D": "could"}, "answer": "A"},
    {"id": "q7", "topic": "Conjunctions", "prompt": "I stayed home ___ it was raining.", "options": {"A": "unless", "B": "because", "C": "although", "D": "so that"}, "answer": "B"},
    {"id": "q8", "topic": "Conditionals", "prompt": "If I had more time, I ___ another language.", "options": {"A": "learn", "B": "will learn", "C": "would learn", "D": "learned"}, "answer": "C"},
    {"id": "q9", "topic": "Sentence structure", "prompt": "Choose the correctly punctuated sentence.", "options": {"A": "After dinner we went for a walk.", "B": "After dinner, we went for a walk.", "C": "After, dinner we went for a walk.", "D": "After dinner we, went for a walk."}, "answer": "B"},
    {"id": "q10", "topic": "Tenses", "prompt": "They ___ the report before the deadline yesterday.", "options": {"A": "finish", "B": "have finished", "C": "had finished", "D": "finishing"}, "answer": "C"},
]


class GrammarService:
    def __init__(self) -> None:
        models_path = Path(__file__).parents[1] / "models"
        self.category_model = OptionalJoblibModel(models_path / "grammar_category_model.joblib")
        self.score_model = OptionalJoblibModel(models_path / "grammar_score_model.joblib")
        self.model = self.category_model

    @property
    def kaggle_models_available(self) -> bool:
        return self.category_model.available and self.score_model.available

    def _model_score(self, answers: list[GrammarAnswer]) -> int:
        answer_map = {item.question_id: item.answer for item in answers}
        category_predictions = []
        score_inputs = []
        for question in QUESTION_BANK:
            answer = answer_map.get(question["id"], "")
            sentence = question["prompt"].replace("___", question["options"].get(answer, ""))
            category_predictions.append(self.category_model.model.predict([sentence])[0])
            score_inputs.append([question["topic"], "correct" if answer == question["answer"] else "incorrect"])

        scores = self.score_model.model.predict(score_inputs)
        return round(max(0, min(100, sum(float(score) for score in scores) / len(scores))))

    def score(self, answers: list[GrammarAnswer]) -> tuple[int, dict[str, int]]:
        answer_map = {item.question_id: item.answer for item in answers}
        topic_totals: dict[str, int] = {}
        topic_correct: dict[str, int] = {}
        correct = 0
        for question in QUESTION_BANK:
            topic = question["topic"]
            topic_totals[topic] = topic_totals.get(topic, 0) + 1
            if answer_map.get(question["id"]) == question["answer"]:
                correct += 1
                topic_correct[topic] = topic_correct.get(topic, 0) + 1
        score = self._model_score(answers) if self.kaggle_models_available else round(correct / len(QUESTION_BANK) * 100)
        topic_scores = {topic: round(topic_correct.get(topic, 0) / total * 100) for topic, total in topic_totals.items()}
        return score, topic_scores
