# 1
FROM python:3.11-slim as deps

ARG POETRY_VERSION=1.8.4

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml

RUN pip install "poetry==${POETRY_VERSION}" \
    && poetry config warnings.export false \
    && poetry install --no-root \
    && poetry export --without-hashes --format=requirements.txt > /app/requirements.txt


# 2
FROM python:3.11-slim

WORKDIR /app

COPY ./spbd /app/spbd
COPY ./storage /app/storage
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY --from=deps /app/requirements.txt /app/requirements.txt

RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && find ./spbd | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf \
    && pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "/app/spbd/main.py", "--port", "80"]
