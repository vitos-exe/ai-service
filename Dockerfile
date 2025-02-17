FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
LABEL authors="vitalii.chernysh"

COPY /ai_service /app/ai_service
COPY pyproject.toml /app/pyproject.toml
COPY /models /app/models
COPY lyrics.csv /app/lyrics.csv

WORKDIR /app

RUN uv sync --no-dev

ENV FLASK_APP=ai_service
ENV FLASK_RUN_HOST=0.0.0.0
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

ENTRYPOINT ["flask", "run"]
