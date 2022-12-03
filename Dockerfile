FROM python:3.11

WORKDIR /usr/src/statsistics_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry 
RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-root

COPY . ./

CMD cd app/db/ && \
    poetry run alembic upgrade head && \
    cd ../../ && \
    poetry run uvicorn --host=0.0.0.0 app.main:app