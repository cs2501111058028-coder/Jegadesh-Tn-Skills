"""
Edge Cases and AI Failure Fallback Tests for EduGenie
Verifies graceful degradation when live APIs fail or produce unexpected output.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import qna
import explanation_module
import quiz_module
import summary_module
import learning_path
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_qna_ai_failure_fallback():
    """Simulate Gemini API exception during QnA and verify fallback response."""
    with patch("qna.IS_DEMO_MODE", False):
        with patch("qna.get_gemini_client") as mock_client:
            mock_inst = MagicMock()
            mock_inst.models.generate_content.side_effect = Exception("Rate limit quota exceeded (429)")
            mock_client.return_value = mock_inst

            res = qna.answer_question("Which is the largest ocean?")
            assert res["mode"] == "fallback"
            assert "Pacific" in res["answer"]
            assert "fallback_notice" in res

def test_quiz_ai_failure_invalid_json_fallback():
    """Simulate Gemini API returning non-JSON garbage during quiz generation."""
    with patch("quiz_module.IS_DEMO_MODE", False):
        with patch("quiz_module.get_gemini_client") as mock_client:
            mock_inst = MagicMock()
            mock_resp = MagicMock()
            mock_resp.text = "I am an AI and I cannot generate JSON right now."
            mock_inst.models.generate_content.return_value = mock_resp
            mock_client.return_value = mock_inst

            res = quiz_module.generate_quiz("Pythagoras theorem")
            assert res["mode"] == "fallback"
            assert len(res["quiz"]) == 3
            assert "fallback_notice" in res

def test_explanation_ai_failure_fallback():
    """Simulate Gemini API timeout during explanation."""
    with patch("explanation_module.IS_DEMO_MODE", False):
        with patch("explanation_module.get_gemini_client") as mock_client:
            mock_inst = MagicMock()
            mock_inst.models.generate_content.side_effect = TimeoutError("Request timed out")
            mock_client.return_value = mock_inst

            res = explanation_module.explain_topic("quantum computing", backend="gemini")
            assert res["mode"] == "fallback"
            assert "Qubit" in res["explanation"] or "quantum" in res["explanation"].lower()
            assert "fallback_notice" in res

def test_summarize_ai_failure_fallback():
    """Simulate Gemini API connection error during summarization."""
    with patch("summary_module.IS_DEMO_MODE", False):
        with patch("summary_module.get_gemini_client") as mock_client:
            mock_inst = MagicMock()
            mock_inst.models.generate_content.side_effect = ConnectionError("Network unreachable")
            mock_client.return_value = mock_inst

            res = summary_module.summarize_text("Industrial Revolution text here that is sufficiently long.")
            assert res["mode"] == "fallback"
            assert "summary" in res
            assert "fallback_notice" in res

def test_very_long_input_handling():
    """Test handling of large inputs without crashing."""
    large_passage = "In the history of science, education and technology advanced rapidly. " * 200
    res = client.post("/summarize", json={"text": large_passage})
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data

def test_special_characters_input():
    """Test queries with emojis and unicode characters."""
    response = client.get("/qa?question=What is 🚀 rocket science & E = mc²?")
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
