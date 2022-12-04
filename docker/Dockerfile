FROM python:3.11

WORKDIR /usr/src/statsistics_api

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry 
RUN poetry install --without dev --no-root

COPY . ./

CMD make migrate-up