FROM python:3.11.7-slim

WORKDIR /app

COPY pyproject.toml /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]