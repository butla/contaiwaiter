FROM python:3.6-alpine

ENV PORT 8080
EXPOSE ${PORT}

WORKDIR /app

RUN pip install pipenv
ADD Pipfile.lock /app/
# this is only needed because of a bug in pipenv
ADD Pipfile /app/
RUN pipenv sync

ADD contaiwaiter /app/contaiwaiter

CMD ["pipenv", "run", "python", "-m", "contaiwaiter.status_app"]
