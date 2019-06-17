FROM python:3.7-alpine

ENV PORT 8080
EXPOSE ${PORT}

WORKDIR /app

RUN pip install poetry
ADD poetry.lock /app/
ADD pyproject.toml /app/

# app in a virtualenv separate from the global context with poetry
RUN python -m venv /dependencies/venv
RUN source /dependencies/venv/bin/activate \
    && poetry install --no-dev

ADD contaiwaiter /app/contaiwaiter

CMD ["/dependencies/venv/bin/python", "-m", "contaiwaiter.status_app"]
