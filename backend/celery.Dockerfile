FROM python:3.12-alpine
# Set the working directory
WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

CMD ["poetry", "run", "celery", "-A", "quizme", "worker", "--loglevel=info", "--pool=solo"]
