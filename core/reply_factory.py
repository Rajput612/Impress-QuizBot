from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    """
    Generates responses for the bot based on user input and session state.
    """
    bot_responses = []

    # Fetch the current question ID from the session
    current_question_id = session.get("current_question_id")

    # If there's no current question, this means the quiz hasn't started yet
    if current_question_id is None:
        # Start the quiz with greeting and first question
        bot_responses.append(BOT_WELCOME_MESSAGE)
        current_question_id = 0  # Start from the first question
        first_question = PYTHON_QUESTION_LIST[current_question_id]
        question_text = first_question["question_text"]
        options = "\n".join([f"{idx + 1}. {option}" for idx, option in enumerate(first_question["options"])])
        bot_responses.append(f"{question_text}\n\nOptions:\n{options}")

        # Initialize session state for the quiz
        session["current_question_id"] = current_question_id  # Keep it as the current question
        session["user_answers"] = []  # Initialize the list of answers for the quiz

    else:
        # Once the quiz has started, record the current answer
        success, error = record_current_answer(message, current_question_id, session)

        if not success:
            # If the answer is invalid, show options again
            bot_responses.append(error)
            current_question = PYTHON_QUESTION_LIST[current_question_id]
            options = "\n".join([f"{idx + 1}. {option}" for idx, option in enumerate(current_question["options"])])
            bot_responses.append(f"Please choose from: \n{options}")
            return bot_responses  # Return early to allow the user to correct the answer

        # If the answer is valid, get the next question
        next_question, next_question_id = get_next_question(current_question_id)

        if next_question:
            bot_responses.append(next_question)
            session["current_question_id"] = next_question_id  # Update to the next question
        else:
            # If no more questions, generate the final response
            final_response = generate_final_response(session)
            bot_responses.append(final_response)

            # Clear session after quiz completion
            session.pop("current_question_id", None)
            session.pop("user_answers", None)

    # Save the session if it supports saving (e.g., Django session)
    if hasattr(session, "save"):
        session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    """
    Validates and stores the answer for the current question in the Django session.
    """
    if current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question ID."

    # Retrieve the correct question based on the current ID
    question = PYTHON_QUESTION_LIST[current_question_id]
    correct_answer = question["answer"]

    # Check if the answer is valid
    if answer not in question["options"]:
        return False, f"Invalid response. Please choose from {question['options']}."

    # Store the user's answer in the session
    user_answers = session.get("user_answers", [])
    user_answers.append({"question_id": current_question_id, "answer": answer, "correct": answer == correct_answer})
    session["user_answers"] = user_answers

    return True, ""


def get_next_question(current_question_id):
    """
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    """
    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        question = PYTHON_QUESTION_LIST[next_question_id]
        question_text = question["question_text"]
        options = "\n".join([f"{idx + 1}. {option}" for idx, option in enumerate(question["options"])])
        return f"{question_text}\n\nOptions:\n{options}", next_question_id

    # If no more questions, return None
    return None, None


def generate_final_response(session):
    user_answers = session.get("user_answers", [])
    correct_count = sum(1 for ans in user_answers if ans["correct"])
    total_questions = len(user_answers)  # Use answered questions count instead of full list length
    score_message = f"Quiz completed! You scored {correct_count}/{total_questions}."
    bot_responses = [score_message, "Would you like to restart the quiz? (yes/no)"]
    return "\n".join(bot_responses)
