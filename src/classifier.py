import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

PERSONAS = [
    "Technical Expert",
    "Frustrated User",
    "Business Executive"
]


def classify_persona(user_message: str):

    message = user_message.lower()

    # Frustrated User
    frustrated_words = [
        "nothing works",
        "tried everything",
        "urgent",
        "urgently",
        "broken",
        "frustrated",
        "angry",
        "hate",
        "terrible",
        "refund",
        "charged",
        "billing",
        "payment",
        "charge",
        "invoice",
        "complaint"
    ]

    if any(word in message for word in frustrated_words):
        return {
            "persona": "Frustrated User",
            "confidence": 0.95,
            "reasoning": "Frustration or billing issue detected"
        }

    # Technical Expert
    technical_words = [
        "api",
        "authentication",
        "token",
        "header",
        "headers",
        "database",
        "integration",
        "endpoint",
        "logs",
        "configuration",
        "config",
        "server",
        "http",
        "https",
        "error code",
        "401",
        "403",
        "500"
    ]

    if any(word in message for word in technical_words):
        return {
            "persona": "Technical Expert",
            "confidence": 0.95,
            "reasoning": "Technical terminology detected"
        }

    # Business Executive
    executive_words = [
        "business",
        "operations",
        "timeline",
        "executive",
        "impact",
        "roi",
        "revenue",
        "uptime",
        "productivity",
        "customers"
    ]

    if any(word in message for word in executive_words):
        return {
            "persona": "Business Executive",
            "confidence": 0.95,
            "reasoning": "Business context detected"
        }

    prompt = f"""
Classify the customer into exactly one persona.

Technical Expert:
- APIs
- logs
- configurations
- integrations
- code

Frustrated User:
- emotional language
- urgency
- complaints
- repeated failures

Business Executive:
- business impact
- operations
- timelines
- concise communication

Return valid JSON only.

{{
    "persona": "...",
    "confidence": 0.95,
    "reasoning": "..."
}}

Message:
{user_message}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown json wrappers if Gemini adds them
        text = text.replace("```json", "")
        text = text.replace("```", "").strip()

        result = json.loads(text)

        if result.get("persona") not in PERSONAS:
            raise Exception("Invalid persona")

        return result

    except Exception as e:
        print("CLASSIFIER ERROR:", e)

        return {
            "persona": "Frustrated User",
            "confidence": 0.50,
            "reasoning": "Fallback classification"
        }