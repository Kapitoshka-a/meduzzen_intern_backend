FROM python:3.11.7-slim

RUN mkdir /fastapi_app
WORKDIR /fastapi_app

COPY pyproject.toml .
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

ENV PYTHONPATH=/fastapi_app

EXPOSE 8000

RUN chmod a+x docker/*.sh