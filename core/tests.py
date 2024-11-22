import pytest
from unittest.mock import MagicMock
from .reply_factory import generate_bot_responses, generate_final_response
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


@pytest.fixture
def session():
    """Mock session for testing."""
    return {}


def test_quiz_start(session):
    """Test starting the quiz."""
    response = generate_bot_responses("", session)
    assert BOT_WELCOME_MESSAGE in response[0]
    assert PYTHON_QUESTION_LIST[0]["question_text"] in response[1]


def test_valid_answer(session):
    """Test providing a valid answer and moving to the next question."""
    session["current_question_id"] = 0
    session["user_answers"] = []

    message = "7"  # Correct answer for the first question
    response = generate_bot_responses(message, session)

    # Validate the second question is returned
    assert PYTHON_QUESTION_LIST[1]["question_text"] in response[0]


def test_invalid_answer(session):
    """Test providing an invalid answer and receiving an error message."""
    session["current_question_id"] = 0
    session["user_answers"] = []

    message = "invalid_choice"
    response = generate_bot_responses(message, session)

    # Validate the error message and options
    assert "Invalid response. Please choose from" in response[0]
    assert "7" in response[1]  # Options for the first question


def test_quiz_completion(session):
    """Test the quiz completion flow and final score generation."""
    session["current_question_id"] = len(PYTHON_QUESTION_LIST) - 1
    session["user_answers"] = [
        {"question_id": idx, "answer": question["answer"], "correct": True}
        for idx, question in enumerate(PYTHON_QUESTION_LIST[:-1])
    ]

    message = PYTHON_QUESTION_LIST[-1]["answer"]  # Correct answer for the last question
    response = generate_bot_responses(message, session)

    # Validate the quiz completion message
    assert "Quiz completed!" in response[0]
    assert f"You scored {len(PYTHON_QUESTION_LIST)}/{len(PYTHON_QUESTION_LIST)}." in response[0]


def test_generate_final_response(session):
    """Test generating the final response with a calculated score."""
    session["user_answers"] = [
        {"question_id": 0, "answer": "7", "correct": True},
        {"question_id": 1, "answer": "1var", "correct": False},
        {"question_id": 2, "answer": "Returns the number of items in a list", "correct": True},
    ]

    final_response = generate_final_response(session)

    # Validate the final response score
    assert "Quiz completed! You scored 2/3." in final_response
