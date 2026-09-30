"""
EduGenie Learning Path Module
Generates structured milestone-based study roadmaps from beginner to advanced.
"""

import logging
from typing import Dict, Any
from config import IS_DEMO_MODE, GEMINI_MODEL, get_gemini_client
from demo_generator import generate_demo_learning_path

logger = logging.getLogger("EduGenie.LearningPath")

def get_learning_recommendations(topic: str) -> Dict[str, Any]:
    """
    Generates structured, step-by-step learning recommendations and resources for any academic topic.
    """
    cleaned_topic = topic.strip()
    if not cleaned_topic:
        raise ValueError("Topic for learning recommendations cannot be empty.")

    if IS_DEMO_MODE:
        logger.info(f"[Demo Mode] Generating learning path for topic: '{cleaned_topic}'")
        roadmap = generate_demo_learning_path(cleaned_topic)
        return {
            "topic": cleaned_topic,
            "recommendations": roadmap,
            "mode": "demo",
            "model": "offline-deterministic"
        }

    client = get_gemini_client()
    if not client:
        logger.warning("[Fallback] Gemini client unavailable. Using offline learning path.")
        roadmap = generate_demo_learning_path(cleaned_topic)
        return {
            "topic": cleaned_topic,
            "recommendations": roadmap,
            "mode": "fallback",
            "model": "offline-deterministic"
        }

    prompt = (
        f"You are a master educational curriculum architect. Create a comprehensive, structured learning roadmap for '{cleaned_topic}'.\n\n"
        "Format requirements:\n"
        "1. Stage 1: Beginner Fundamentals (Core concepts, estimated hours/weeks, free tutorials/interactive resources)\n"
        "2. Stage 2: Intermediate Application (Hands-on practice, key techniques, project exercises)\n"
        "3. Stage 3: Advanced Mastery (Architecture, performance, complex scenarios, capstone project)\n"
        "4. Recommended reading, tools, and milestone objectives.\n"
        "Use rich Markdown with emoji indicators for each stage."
    )

    try:
        if hasattr(client, "models") and hasattr(client.models, "generate_content"):
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            recommendations_text = response.text if hasattr(response, "text") else str(response)
        else:
            model = client.GenerativeModel(GEMINI_MODEL)
            response = model.generate_content(prompt)
            recommendations_text = response.text

        return {
            "topic": cleaned_topic,
            "recommendations": recommendations_text.strip(),
            "mode": "live",
            "model": GEMINI_MODEL
        }
    except Exception as e:
        logger.error(f"Gemini API error during learning path generation: {e}. Falling back.")
        roadmap = generate_demo_learning_path(cleaned_topic)
        return {
            "topic": cleaned_topic,
            "recommendations": roadmap,
            "mode": "fallback",
            "model": "offline-deterministic",
            "fallback_notice": f"Live API unavailable ({str(e)[:50]}...). Switched to offline roadmap."
        }
