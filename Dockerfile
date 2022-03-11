# syntax=docker/dockerfile:1
FROM python:3

ENV PATH="/root/.local/bin:/root/.poetry/bin:${PATH}" \
    SHELL="/bin/bash" \
    PYTHONUNBUFFERED=1
WORKDIR /code
COPY pyproject.toml poetry.lock /code/
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - && \
	poetry config virtualenvs.create false && \
	poetry config virtualenvs.in-project false && \
	poetry install

COPY . /code/
