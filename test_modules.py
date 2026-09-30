"""
Unit Tests for EduGenie AI and Fallback Modules
Verifies individual core logic and parsing.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz, validate_quiz_data, clean_json_block
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from demo_generator import generate_demo_qa, generate_demo_explanation, generate_demo_quiz, generate_demo_summary, generate_demo_learning_path

def test_qna_module_direct():
    res = answer_question("What is photosynthesis?")
    assert "question" in res
    assert "answer" in res
    assert "glucose" in res["answer"].lower() or "sunlight" in res["answer"].lower()

def test_qna_module_empty_raises():
    with pytest.raises(ValueError):
        answer_question("   ")

def test_explanation_module_direct_gemini():
    res = explain_topic("quantum computing", backend="gemini")
    assert "topic" in res
    assert "explanation" in res
    assert "Qubit" in res["explanation"] or "quantum" in res["explanation"].lower()

def test_explanation_module_direct_local():
    res = explain_topic("binary search algorithm", backend="local")
    assert res["backend"] == "local"
    assert "explanation" in res

def test_explanation_module_empty_raises():
    with pytest.raises(ValueError):
        explain_topic("")

def test_quiz_module_direct():
    res = generate_quiz("Pythagoras theorem")
    assert "quiz" in res
    assert len(res["quiz"]) == 3
    for item in res["quiz"]:
        assert len(item["options"]) == 4
        assert item["answer"] in item["options"]

def test_quiz_module_empty_raises():
    with pytest.raises(ValueError):
        generate_quiz("  ")

def test_quiz_schema_validator_valid():
    valid_data = [
        {"question": "Q1", "options": ["A", "B", "C", "D"], "answer": "B"},
        {"question": "Q2", "options": ["A", "B", "C", "D"], "answer": "C"},
        {"question": "Q3", "options": ["A", "B", "C", "D"], "answer": "A"}
    ]
    assert validate_quiz_data(valid_data) is True

def test_quiz_schema_validator_invalid_count():
    invalid_data = [
        {"question": "Q1", "options": ["A", "B", "C", "D"], "answer": "B"},
        {"question": "Q2", "options": ["A", "B", "C", "D"], "answer": "C"}
    ]
    assert validate_quiz_data(invalid_data) is False

def test_quiz_schema_validator_invalid_options_count():
    invalid_data = [
        {"question": "Q1", "options": ["A", "B", "C"], "answer": "B"},
        {"question": "Q2", "options": ["A", "B", "C", "D"], "answer": "C"},
        {"question": "Q3", "options": ["A", "B", "C", "D"], "answer": "A"}
    ]
    assert validate_quiz_data(invalid_data) is False

def test_quiz_schema_validator_answer_mismatch():
    invalid_data = [
        {"question": "Q1", "options": ["A", "B", "C", "D"], "answer": "Z"},
        {"question": "Q2", "options": ["A", "B", "C", "D"], "answer": "C"},
        {"question": "Q3", "options": ["A", "B", "C", "D"], "answer": "A"}
    ]
    assert validate_quiz_data(invalid_data) is False

def test_quiz_clean_json_block():
    markdown_json = "```json\n[{\"question\": \"Test?\", \"options\": [\"1\", \"2\", \"3\", \"4\"], \"answer\": \"1\"}]\n```"
    cleaned = clean_json_block(markdown_json)
    assert cleaned.startswith("[")
    assert cleaned.endswith("]")

def test_summary_module_direct():
    text = "The quick brown fox jumps over the lazy dog. Education empowers students to solve real problems."
    res = summarize_text(text)
    assert "summary" in res
    assert res["original_length"] == len(text)

def test_summary_module_empty_raises():
    with pytest.raises(ValueError):
        summarize_text(" ")

def test_learning_path_module_direct():
    res = get_learning_recommendations("SQL")
    assert res["topic"] == "SQL"
    assert "Stage 1" in res["recommendations"]

def test_learning_path_module_empty_raises():
    with pytest.raises(ValueError):
        get_learning_recommendations("")
