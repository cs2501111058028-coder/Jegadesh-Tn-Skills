"""
EduGenie QnA Module
Handles smart, concise question answering for students and learners.
"""

import logging
from typing import Dict, Any
from config import IS_DEMO_MODE, GEMINI_MODEL, get_gemini_client
from demo_generator import generate_demo_qa

logger = logging.getLogger("EduGenie.QnA")

def answer_question(question: str) -> Dict[str, Any]:
    """
    Answers an educational question concisely and accurately.
    Uses Gemini in live mode or deterministic offline generator in demo/fallback mode.
    """
    cleaned_question = question.strip()
    if not cleaned_question:
        raise ValueError("Question cannot be empty.")

    if IS_DEMO_MODE:
        logger.info(f"[Demo Mode] Answering question: '{cleaned_question}'")
        answer = generate_demo_qa(cleaned_question)
        return {
            "question": cleaned_question,
            "answer": answer,
            "mode": "demo",
            "model": "offline-deterministic"
        }

    client = get_gemini_client()
    if not client:
        logger.warning("[Fallback] Gemini client unavailable. Using offline generator.")
        answer = generate_demo_qa(cleaned_question)
        return {
            "question": cleaned_question,
            "answer": answer,
            "mode": "fallback",
            "model": "offline-deterministic"
        }

    prompt = (
        "You are an expert educational tutor for students. "
        "Provide a smart, concise, and highly accurate answer to the following question. "
        "Keep the explanation clear and educational (2 to 4 sentences).\n\n"
        f"Question: {cleaned_question}"
    )

    try:
        # Check if client has models.generate_content (google-genai) or GenerativeModel (legacy)
        if hasattr(client, "models") and hasattr(client.models, "generate_content"):
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            answer_text = response.text if hasattr(response, "text") else str(response)
        else:
            model = client.GenerativeModel(GEMINI_MODEL)
            response = model.generate_content(prompt)
            answer_text = response.text

        return {
            "question": cleaned_question,
            "answer": answer_text.strip(),
            "mode": "live",
            "model": GEMINI_MODEL
        }
    except Exception as e:
        logger.error(f"Gemini API error during QnA: {e}. Falling back to deterministic generator.")
        answer = generate_demo_qa(cleaned_question)
        return {
            "question": cleaned_question,
            "answer": answer,
            "mode": "fallback",
            "model": "offline-deterministic",
            "fallback_notice": f"Live API unavailable ({str(e)[:50]}...). Switched to offline response."
        }
