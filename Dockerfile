FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY . .

# Install the project
RUN poetry install --no-interaction --no-ansi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 