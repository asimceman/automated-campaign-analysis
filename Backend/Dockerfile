FROM python:3.13-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
 && poetry install --no-root

COPY . /app
COPY alembic alembic/
COPY alembic.ini ./

ENV PYTHONPATH=/app

CMD ["python", "-m", "app"]