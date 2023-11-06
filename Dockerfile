FROM cgr.dev/chainguard/python:latest-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --user

COPY . .

ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8000

EXPOSE 8000
ENTRYPOINT ["python", "-m", "flask", "run"]