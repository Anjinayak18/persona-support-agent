import streamlit as st

from src.classifier import classify_persona
from src.rag_pipeline import RAGPipeline
from src.generator import generate_response
from src.escalator import (
    should_escalate,
    generate_handoff
)

st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    layout="wide"
)

st.title("🤖 Persona Adaptive Support Agent")

query = st.text_area(
    "Customer Message"
)

if st.button("Submit"):

    if query.strip():

        rag = RAGPipeline()

        persona_result = classify_persona(
            query
        )

        persona = persona_result[
            "persona"
        ]

        retrieved = rag.retrieve(
            query
        )

        st.subheader(
            "Detected Persona"
        )

        st.write(persona)
        st.write(persona_result)
        print("PERSONA RESULT:", persona_result)

        st.subheader(
            "Retrieved Sources"
        )

        for item in retrieved:

            st.write(
                f"{item['source']} | score={item['score']}"
            )

        escalate = should_escalate(
            query,
            retrieved
        )

        st.subheader(
            "Escalation Status"
        )

        if escalate:

            st.error(
                "Escalated To Human Agent"
            )

            handoff = generate_handoff(
                persona,
                query,
                retrieved
            )

            st.subheader(
                "Handoff Summary"
            )

            st.code(
                handoff,
                language="json"
            )

        else:

            answer = generate_response(
                query,
                persona,
                retrieved
            )

            st.subheader(
                "Response"
            )

            st.write(answer)