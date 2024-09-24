FROM python:3.10.6-slim-bullseye 

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=1 \
	POETRY_VIRTUALENVS_CREATE=1 \
	POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./
RUN touch readme.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY tomato_stream tomato_stream
COPY .env gcloud_credentials.json ./

RUN poetry install --without dev

CMD poetry run python3 tomato_stream/crawler.py
