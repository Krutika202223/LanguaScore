from pathlib import Path

import random

from backend.schemas.assessment import GrammarAnswer
from backend.services.model_loader import OptionalJoblibModel


QUESTION_BANK = [
    {"id": "q1", "topic": "Tenses", "prompt": "She ___ her homework every evening.", "options": {"A": "do", "B": "does", "C": "doing", "D": "done"}, "answer": "B"},
    {"id": "q2", "topic": "Tenses", "prompt": "They ___ to Mumbai last weekend.", "options": {"A": "travel", "B": "travels", "C": "travelled", "D": "travelling"}, "answer": "C"},
    {"id": "q3", "topic": "Tenses", "prompt": "I ___ this book three times.", "options": {"A": "read", "B": "have read", "C": "am reading", "D": "reads"}, "answer": "B"},
    {"id": "q4", "topic": "Tenses", "prompt": "When we arrived, the movie ___.", "options": {"A": "starts", "B": "started", "C": "had started", "D": "starting"}, "answer": "C"},
    {"id": "q5", "topic": "Tenses", "prompt": "He ___ dinner when I called him.", "options": {"A": "has", "B": "had", "C": "was having", "D": "have"}, "answer": "C"},
    {"id": "q6", "topic": "Tenses", "prompt": "By next year, she ___ her degree.", "options": {"A": "completes", "B": "completed", "C": "will have completed", "D": "completing"}, "answer": "C"},
    {"id": "q7", "topic": "Tenses", "prompt": "We ___ for two hours before the bus arrived.", "options": {"A": "waited", "B": "had been waiting", "C": "wait", "D": "are waiting"}, "answer": "B"},
    {"id": "q8", "topic": "Tenses", "prompt": "My brother ___ football every Sunday.", "options": {"A": "play", "B": "plays", "C": "played", "D": "playing"}, "answer": "B"},
    {"id": "q9", "topic": "Articles", "prompt": "She wants to become ___ engineer.", "options": {"A": "a", "B": "an", "C": "the", "D": "no article"}, "answer": "B"},
    {"id": "q10", "topic": "Articles", "prompt": "I bought ___ new laptop yesterday.", "options": {"A": "a", "B": "an", "C": "the", "D": "no article"}, "answer": "A"},
    {"id": "q11", "topic": "Articles", "prompt": "___ sun rises in the east.", "options": {"A": "A", "B": "An", "C": "The", "D": "No article"}, "answer": "C"},
    {"id": "q12", "topic": "Articles", "prompt": "He is ___ honest person.", "options": {"A": "a", "B": "an", "C": "the", "D": "no article"}, "answer": "B"},
    {"id": "q13", "topic": "Articles", "prompt": "We visited ___ museum near our college.", "options": {"A": "a", "B": "an", "C": "the", "D": "no article"}, "answer": "A"},
    {"id": "q14", "topic": "Articles", "prompt": "She plays ___ piano very well.", "options": {"A": "a", "B": "an", "C": "the", "D": "no article"}, "answer": "C"},
    {"id": "q15", "topic": "Prepositions", "prompt": "The books are ___ the table.", "options": {"A": "in", "B": "on", "C": "at", "D": "by"}, "answer": "B"},
    {"id": "q16", "topic": "Prepositions", "prompt": "I will meet you ___ Monday.", "options": {"A": "in", "B": "at", "C": "on", "D": "by"}, "answer": "C"},
    {"id": "q17", "topic": "Prepositions", "prompt": "She arrived ___ the airport at 6 PM.", "options": {"A": "in", "B": "at", "C": "on", "D": "by"}, "answer": "B"},
    {"id": "q18", "topic": "Prepositions", "prompt": "He has lived here ___ 2020.", "options": {"A": "for", "B": "since", "C": "from", "D": "by"}, "answer": "B"},
    {"id": "q19", "topic": "Prepositions", "prompt": "The children are playing ___ the garden.", "options": {"A": "on", "B": "at", "C": "in", "D": "by"}, "answer": "C"},
    {"id": "q20", "topic": "Prepositions", "prompt": "We waited ___ the bus for thirty minutes.", "options": {"A": "for", "B": "since", "C": "from", "D": "with"}, "answer": "A"},
    {"id": "q21", "topic": "Subject-Verb Agreement", "prompt": "The students ___ ready for the examination.", "options": {"A": "is", "B": "are", "C": "was", "D": "be"}, "answer": "B"},
    {"id": "q22", "topic": "Subject-Verb Agreement", "prompt": "My friend ___ in Pune.", "options": {"A": "live", "B": "living", "C": "lives", "D": "are living"}, "answer": "C"},
    {"id": "q23", "topic": "Subject-Verb Agreement", "prompt": "The list of names ___ on the desk.", "options": {"A": "are", "B": "were", "C": "is", "D": "be"}, "answer": "C"},
    {"id": "q24", "topic": "Subject-Verb Agreement", "prompt": "Neither the teacher nor the students ___ absent.", "options": {"A": "is", "B": "was", "C": "are", "D": "has"}, "answer": "C"},
    {"id": "q25", "topic": "Subject-Verb Agreement", "prompt": "Mathematics ___ my favorite subject.", "options": {"A": "are", "B": "were", "C": "is", "D": "have"}, "answer": "C"},
    {"id": "q26", "topic": "Subject-Verb Agreement", "prompt": "Each of the players ___ a uniform.", "options": {"A": "have", "B": "has", "C": "having", "D": "are having"}, "answer": "B"},
    {"id": "q27", "topic": "Pronouns", "prompt": "Rahul and ___ went to the library.", "options": {"A": "me", "B": "I", "C": "my", "D": "mine"}, "answer": "B"},
    {"id": "q28", "topic": "Pronouns", "prompt": "This book belongs to Sarah. It is ___.", "options": {"A": "her", "B": "hers", "C": "she", "D": "herself"}, "answer": "B"},
    {"id": "q29", "topic": "Pronouns", "prompt": "The teacher asked John and ___ to stay back.", "options": {"A": "I", "B": "he", "C": "me", "D": "we"}, "answer": "C"},
    {"id": "q30", "topic": "Pronouns", "prompt": "Priya prepared the presentation by ___.", "options": {"A": "herself", "B": "her", "C": "hers", "D": "she"}, "answer": "A"},
    {"id": "q31", "topic": "Pronouns", "prompt": "___ are going to attend the meeting.", "options": {"A": "Them", "B": "Their", "C": "They", "D": "Theirs"}, "answer": "C"},
    {"id": "q32", "topic": "Modals", "prompt": "You ___ complete your assignment before Friday.", "options": {"A": "must", "B": "might", "C": "could", "D": "would"}, "answer": "A"},
    {"id": "q33", "topic": "Modals", "prompt": "___ I borrow your pen?", "options": {"A": "Must", "B": "May", "C": "Should", "D": "Would"}, "answer": "B"},
    {"id": "q34", "topic": "Modals", "prompt": "You ___ see a doctor if you feel sick.", "options": {"A": "should", "B": "might", "C": "can", "D": "would"}, "answer": "A"},
    {"id": "q35", "topic": "Modals", "prompt": "It ___ rain tomorrow.", "options": {"A": "must", "B": "might", "C": "should", "D": "ought"}, "answer": "B"},
    {"id": "q36", "topic": "Modals", "prompt": "When I was younger, I ___ swim very fast.", "options": {"A": "can", "B": "could", "C": "must", "D": "should"}, "answer": "B"},
    {"id": "q37", "topic": "Conjunctions", "prompt": "I stayed at home ___ I was feeling sick.", "options": {"A": "but", "B": "because", "C": "or", "D": "unless"}, "answer": "B"},
    {"id": "q38", "topic": "Conjunctions", "prompt": "She studied hard, ___ she passed the examination.", "options": {"A": "so", "B": "but", "C": "although", "D": "unless"}, "answer": "A"},
    {"id": "q39", "topic": "Conjunctions", "prompt": "I wanted to go outside, ___ it was raining.", "options": {"A": "because", "B": "but", "C": "so", "D": "and"}, "answer": "B"},
    {"id": "q40", "topic": "Conjunctions", "prompt": "You can have tea ___ coffee.", "options": {"A": "but", "B": "because", "C": "or", "D": "although"}, "answer": "C"},
    {"id": "q41", "topic": "Conjunctions", "prompt": "___ he was tired, he continued working.", "options": {"A": "Because", "B": "Although", "C": "So", "D": "And"}, "answer": "B"},
    {"id": "q42", "topic": "Conditionals", "prompt": "If it rains, we ___ at home.", "options": {"A": "stay", "B": "stayed", "C": "will stay", "D": "would stay"}, "answer": "C"},
    {"id": "q43", "topic": "Conditionals", "prompt": "If I had more money, I ___ a new laptop.", "options": {"A": "buy", "B": "will buy", "C": "would buy", "D": "bought"}, "answer": "C"},
    {"id": "q44", "topic": "Conditionals", "prompt": "If you heat water to 100°C, it ___.", "options": {"A": "boiled", "B": "boils", "C": "will boil", "D": "would boil"}, "answer": "B"},
    {"id": "q45", "topic": "Conditionals", "prompt": "If she studies hard, she ___ the exam.", "options": {"A": "passed", "B": "would pass", "C": "will pass", "D": "passing"}, "answer": "C"},
    {"id": "q46", "topic": "Conditionals", "prompt": "If I had known about the meeting, I ___ attended it.", "options": {"A": "will have", "B": "would have", "C": "would", "D": "had"}, "answer": "B"},
    {"id": "q47", "topic": "Sentence Structure & Punctuation", "prompt": "Choose the correctly punctuated sentence.", "options": {"A": "After school we went home.", "B": "After school, we went home.", "C": "After, school we went home.", "D": "After school we, went home."}, "answer": "B"},
    {"id": "q48", "topic": "Sentence Structure & Punctuation", "prompt": "Choose the correct sentence.", "options": {"A": "She don't like coffee.", "B": "She doesn't likes coffee.", "C": "She doesn't like coffee.", "D": "She not like coffee."}, "answer": "C"},
    {"id": "q49", "topic": "Sentence Structure & Punctuation", "prompt": "Choose the correctly structured sentence.", "options": {"A": "Because was raining, we stayed home.", "B": "Because it was raining, we stayed home.", "C": "Because raining it was, we stayed home.", "D": "It because was raining, we stayed home."}, "answer": "B"},
    {"id": "q50", "topic": "Sentence Structure & Punctuation", "prompt": "Choose the correct sentence.", "options": {"A": "I went to college, and I attended the lecture.", "B": "I went college and attended, the lecture.", "C": "I went to college and, attended the lecture.", "D": "I went to college and attended the, lecture."}, "answer": "A"},
]


class GrammarService:
    def __init__(self) -> None:
        self.model = OptionalJoblibModel(Path(__file__).parents[1] / "models" / "grammar_model.joblib")

    def select_questions(self, count: int = 10) -> list[dict[str, object]]:
        return random.sample(QUESTION_BANK, count)

    def score(self, answers: list[GrammarAnswer]) -> tuple[int, dict[str, int]]:
        answer_map = {item.question_id: item.answer for item in answers}
        selected_questions = [question for question in QUESTION_BANK if question["id"] in answer_map]
        if len(selected_questions) != len(answers):
            raise ValueError("Assessment contains an unknown or duplicate grammar question")
        topic_totals: dict[str, int] = {}
        topic_correct: dict[str, int] = {}
        correct = 0
        for question in selected_questions:
            topic = question["topic"]
            topic_totals[topic] = topic_totals.get(topic, 0) + 1
            if answer_map.get(question["id"]) == question["answer"]:
                correct += 1
                topic_correct[topic] = topic_correct.get(topic, 0) + 1
        score = round(correct / len(selected_questions) * 100)
        topic_scores = {topic: round(topic_correct.get(topic, 0) / total * 100) for topic, total in topic_totals.items()}
        return score, topic_scores
