FROM python:3.10.7-slim-bullseye AS builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /opt


COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip \
  && pip install "poetry==1.2.2"
RUN poetry config virtualenvs.in-project true \ 
  && poetry install --only=main --no-interaction

# --

FROM python:3.10.7-slim-bullseye 

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


COPY --from=builder /opt/.venv/ /opt/.venv/

ENV PATH=/opt/.venv/bin:$PATH

COPY ./compose/local/fastapi/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/fastapi/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/fastapi/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/fastapi/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/fastapi/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


WORKDIR /app

ENTRYPOINT ["/entrypoint"] 

