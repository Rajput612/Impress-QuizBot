# Quiz bot
This is a basic version of an interactive quiz bot that engages users in quizzes, evaluates their responses, and provides a final score based on their answers. In this we use Django channels websocket communication, redis as message broker, and Django sessions for temporary data storage.


Steps to run the project with Docker

1. Install Docker and Docker Compose (https://docs.docker.com/compose/install/)
2. Docker should be running
3. In the project root run `docker-compose build` and `docker-compose up`
4. Go to `localhost` to view the chatbot


Steps to run the project without Docker

1. Install required packages by running `pip install -r requirements.txt`
2. Install and run postgresql, and change the `DATABASES` config in `settings.py`, if required.
3. Install and run redis, and update the `CHANNEL_LAYERS` config in `settings.py`, if required.
4. In the project root run `python manage.py runserver`
5. Go to `127.0.0.1:8000` to view the chatbot

Steps to run the tests

1. Install pytest by running pip install pytest, if not already installed.
2. To run tests:
   1. If using Docker:
      . Run docker exec -it quiz-bot-web-1 pytest core/tests.py. 
   2. Without Docker:
      . Run pytest core/tests.py in the project root.
            All test cases are located in the core app.
