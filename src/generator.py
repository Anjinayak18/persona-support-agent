import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_response(query, persona, context_chunks):

    context = "\n\n".join(
        [
            f"Source: {c['source']}\n{c['text']}"
            for c in context_chunks
        ]
    )

    if persona == "Technical Expert":

        style = """
You are a Senior Support Engineer.

Provide:
- detailed explanation
- root cause analysis
- troubleshooting steps
- technical precision
"""

    elif persona == "Business Executive":

        style = """
You are a Client Success Director.

Provide:
- concise response
- operational impact
- resolution guidance

Avoid deep technical details.
"""

    else:

        style = """
You are an empathetic support specialist.

Begin with empathy.

Use:
- simple language
- reassuring tone
- actionable steps
"""

    prompt = f"""
{style}

IMPORTANT:
Use only information from context.

Context:
{context}

Question:
{query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text