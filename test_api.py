"""
Tests for EduGenie FastAPI Endpoints
Verifies routes, input validation, and HTTP responses.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

def test_health_check():
    """Verify /health returns healthy status and metadata."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "EduGenie"
    assert "mode" in data
    assert "default_model" in data

def test_root_html_renders():
    """Verify GET / returns HTML interface."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "EduGenie" in response.text
    assert "Smart Question & Answer" in response.text
    assert "Concept Explainer" in response.text
    assert "Passage Summarizer" in response.text
    assert "Interactive Quiz Generator" in response.text
    assert "Personalized Learning Roadmap" in response.text

def test_qa_scenario_largest_ocean():
    """Scenario 1: Ask 'Which is the largest ocean?'."""
    response = client.get("/qa?question=Which is the largest ocean?")
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Which is the largest ocean?"
    assert "Pacific" in data["answer"]

def test_qa_empty_query():
    """Verify /qa with empty string returns 400."""
    response = client.get("/qa?question=")
    assert response.status_code in [400, 422]

def test_qa_missing_param():
    """Verify /qa without question query param returns 422."""
    response = client.get("/qa")
    assert response.status_code == 422

def test_explain_quantum_computing():
    """Scenario 2: Explain 'quantum computing'."""
    response = client.post("/explain", json={"topic": "quantum computing", "backend": "gemini"})
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "quantum computing"
    assert "Qubit" in data["explanation"] or "quantum" in data["explanation"].lower()

def test_explain_binary_search_local_backend():
    """Scenario 2: Explain 'binary search algorithm' with local backend."""
    response = client.post("/explain", json={"topic": "binary search algorithm", "backend": "local"})
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "binary search algorithm"
    assert data["backend"] == "local"
    assert "Binary Search" in data["explanation"] or "sorted" in data["explanation"].lower()

def test_explain_empty_topic():
    """Verify /explain with empty topic returns 422 or 400."""
    response = client.post("/explain", json={"topic": "   ", "backend": "gemini"})
    assert response.status_code in [400, 422]

def test_summarize_industrial_revolution():
    """Scenario 3: Summarize long Industrial Revolution paragraph."""
    sample_text = (
        "The Industrial Revolution began in Great Britain in the late 18th century and quickly transformed human society "
        "from an agrarian handicraft economy to one dominated by industry and machine manufacturing. Technological innovations "
        "such as James Watt's improved steam engine and the Spinning Jenny dramatically increased textile production efficiency."
    )
    response = client.post("/summarize", json={"text": sample_text})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert len(data["summary"]) > 20

def test_summarize_short_text():
    """Verify /summarize with text under 5 characters returns 422 or 400."""
    response = client.post("/summarize", json={"text": "Hi"})
    assert response.status_code in [400, 422]

def test_quiz_pythagoras_theorem():
    """Scenario 4: Generate quiz on 'Pythagoras theorem'."""
    response = client.post("/quiz", json={"topic": "Pythagoras theorem"})
    assert response.status_code == 200
    data = response.json()
    assert "quiz" in data
    assert len(data["quiz"]) == 3
    for q in data["quiz"]:
        assert "question" in q
        assert len(q["options"]) == 4
        assert q["answer"] in q["options"]

def test_quiz_with_text_field():
    """Verify /quiz works with 'text' field instead of 'topic'."""
    response = client.post("/quiz", json={"text": "Photosynthesis process in green plants"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["quiz"]) == 3

def test_quiz_empty_input():
    """Verify /quiz with empty json returns 400 or 422."""
    response = client.post("/quiz", json={})
    assert response.status_code in [400, 422]

def test_learning_path_sql():
    """Scenario 5: Learning path for 'SQL'."""
    response = client.get("/learn/recommendations?topic=SQL")
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "SQL"
    assert "Stage 1" in data["recommendations"] or "Roadmap" in data["recommendations"]

def test_learning_path_empty_topic():
    """Verify /learn/recommendations with empty topic returns 400 or 422."""
    response = client.get("/learn/recommendations?topic=")
    assert response.status_code in [400, 422]
