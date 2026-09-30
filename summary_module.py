"""
EduGenie Summary Module
Summarizes lengthy educational passages into clear, structured, easy-to-revise notes.
"""

import logging
from typing import Dict, Any
from config import IS_DEMO_MODE, GEMINI_MODEL, get_gemini_client
from demo_generator import generate_demo_summary

logger = logging.getLogger("EduGenie.Summary")

def summarize_text(text: str) -> Dict[str, Any]:
    """
    Summarizes educational text into concise bullet points and takeaways.
    """
    cleaned_text = text.strip()
    if not cleaned_text:
        raise ValueError("Text to summarize cannot be empty.")

    if IS_DEMO_MODE:
        logger.info(f"[Demo Mode] Summarizing text of length {len(cleaned_text)}")
        summary = generate_demo_summary(cleaned_text)
        return {
            "summary": summary,
            "original_length": len(cleaned_text),
            "summary_length": len(summary),
            "mode": "demo",
            "model": "offline-deterministic"
        }

    client = get_gemini_client()
    if not client:
        logger.warning("[Fallback] Gemini client unavailable. Using offline summary.")
        summary = generate_demo_summary(cleaned_text)
        return {
            "summary": summary,
            "original_length": len(cleaned_text),
            "summary_length": len(summary),
            "mode": "fallback",
            "model": "offline-deterministic"
        }

    prompt = (
        "You are an expert educational study guide creator. "
        "Summarize the following passage into clear, high-impact study notes for students.\n\n"
        "Passage:\n"
        f"{cleaned_text}\n\n"
        "Guidelines:\n"
        "- Provide a brief 1-line overview\n"
        "- Provide 3-4 bullet points highlighting the most important key concepts and takeaways\n"
        "- Provide a concluding sentence on why this is significant\n"
        "- Use Markdown headings and bullet points."
    )

    try:
        if hasattr(client, "models") and hasattr(client.models, "generate_content"):
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            summary_text = response.text if hasattr(response, "text") else str(response)
        else:
            model = client.GenerativeModel(GEMINI_MODEL)
            response = model.generate_content(prompt)
            summary_text = response.text

        return {
            "summary": summary_text.strip(),
            "original_length": len(cleaned_text),
            "summary_length": len(summary_text.strip()),
            "mode": "live",
            "model": GEMINI_MODEL
        }
    except Exception as e:
        logger.error(f"Gemini API error during summarization: {e}. Falling back.")
        summary = generate_demo_summary(cleaned_text)
        return {
            "summary": summary,
            "original_length": len(cleaned_text),
            "summary_length": len(summary),
            "mode": "fallback",
            "model": "offline-deterministic",
            "fallback_notice": f"Live API unavailable ({str(e)[:50]}...). Switched to offline summary."
        }
