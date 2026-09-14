def build_recommendations(grammar_score: int, writing_score: int, topic_scores: dict[str, int]) -> tuple[list[str], list[str], list[str]]:
    strengths: list[str] = []
    areas: list[str] = []
    recommendations: list[str] = []

    if grammar_score >= 75:
        strengths.append("Good understanding of core grammar patterns")
    else:
        areas.append("Core grammar accuracy")
        recommendations.append("Review tenses, articles and subject-verb agreement.")
    if writing_score >= 75:
        strengths.append("Clear written communication")
    else:
        areas.append("Written language control")
        recommendations.append("Practice short paragraphs with varied sentence structures.")
    weak_topics = [topic for topic, score in topic_scores.items() if score < 75]
    if weak_topics:
        areas.append(", ".join(weak_topics))
        recommendations.append(f"Focus on {', '.join(topic.lower() for topic in weak_topics)}.")
    if grammar_score >= 75 and writing_score < 75:
        recommendations.append("Your grammar is stronger than your writing; work on vocabulary range and coherence.")
    if grammar_score >= 75 and writing_score >= 75:
        recommendations.append("Extend your range with advanced vocabulary and complex sentence structures.")
    return strengths, areas, list(dict.fromkeys(recommendations))
