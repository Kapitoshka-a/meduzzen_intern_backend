FROM python:3.11.7-slim

WORKDIR /fastapi_app

COPY pyproject.toml .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

EXPOSE 8000

RUN chmod a+x docker/*.sh