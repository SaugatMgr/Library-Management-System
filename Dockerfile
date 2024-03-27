FROM python:3.11.2-slim-bullseye

RUN apt-get update && \
    apt-get install -y make && \
    rm -rf /var/lib/apt/lists/*

ENV DJANGO_SETTINGS_MODULE core.LibraryMgmtSys.local

ENV PIP_DISABLE_PIP_VERSION_CHECK 1

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1

WORKDIR /LibraryManagementSystem

ENV POETRY_VERSION = 1.7.1

RUN pip install "poetry==$POETRY_VERSION"

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "core.manage", "runserver", "0.0.0.0:8000"]
