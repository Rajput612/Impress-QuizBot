# Quiz bot
This is a basic version of an interactive quiz bot that engages users in quizzes, evaluates their responses, and provides a final score based on their answers. In this we use Django channels websocket communication, redis as message broker, and Django sessions for temporary data storage.

## Code Quality Tools

### Black Code Formatter
The project uses Black for consistent code formatting. Black is an uncompromising code formatter that automatically formats your Python code to conform to the Black code style.

To format your code:
1. Install Black: `pip install black`
2. Run formatter: `black .`

### Pre-commit Hooks
We use pre-commit hooks to ensure code quality before each commit.

To set up pre-commit:
1. Install pre-commit: `pip install pre-commit`
2. Install the git hooks: `pre-commit install`
3. The hooks will now run automatically on every commit

Pre-commit configuration includes:
- Black code formatting
- Trailing whitespace removal
- End of file fixing
- YAML syntax checking
- Large file checking

## Running the Project

### With Docker

1. Install Docker and Docker Compose (https://docs.docker.com/compose/install/)
2. Docker should be running
3. In the project root run `docker-compose build` and `docker-compose up`
4. Go to `localhost` to view the chatbot

### Without Docker

1. Install required packages by running `pip install -r requirements.txt`
2. Install and run postgresql, and change the `DATABASES` config in `settings.py`, if required
3. Install and run redis, and update the `CHANNEL_LAYERS` config in `settings.py`, if required
4. In the project root run `python manage.py runserver`
5. Go to `127.0.0.1:8000` to view the chatbot

## Running Tests

1. Install pytest by running `pip install pytest`, if not already installed
2. To run tests:
   - If using Docker:
     - Run `docker exec -it quiz-bot-web-1 pytest core/tests.py`
   - Without Docker:
     - Run `pytest core/tests.py` in the project root

All test cases are located in the core app.
