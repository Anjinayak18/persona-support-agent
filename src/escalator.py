import json

from src.config import CONFIDENCE_THRESHOLD, SENSITIVE_KEYWORDS


def should_escalate(query, retrieved_chunks):
    query_lower = query.lower()

    for keyword in SENSITIVE_KEYWORDS:
        if keyword in query_lower:
            return True

    if not retrieved_chunks:
        return True

    best_score = max(
    item["score"]
    for item in retrieved_chunks
)

    print("BEST SCORE:", best_score)

    if best_score < -0.50:
        return True

    return False


def generate_handoff(
    persona,
    query,
    retrieved_chunks,
    history=None
):
    return json.dumps(
        {
            "persona": persona,
            "issue": query,
            "conversation_history": history or [],
            "documents_used": [
                item["source"] for item in retrieved_chunks
            ],
            "attempted_steps": [
                "Knowledge retrieval",
                "AI generated response"
            ],
            "recommendation": "Human support review required"
        },
        indent=4
    )