FROM python:3.8-buster

ARG sentry_dsn
ARG spotify_client_id
ARG spotify_client_secret
ARG spotify_redirect_uri

ENV SENTRY_DSN=$sentry_dsn
ENV SPOTIFY_CLIENT_ID=$spotify_client_id
ENV SPOTIFY_CLIENT_SECRET=$spotify_client_secret
ENV SPOTIFY_REDIRECT_URI=$spotify_redirect_uri
ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN groupadd -r reco && useradd -r -m -g reco reco

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./data/items.ann /app/data/items.ann
COPY ./data/meta.pkl /app/data/meta.pkl
RUN mkdir -p /app/data && chown -R reco:reco /app/data

USER reco
WORKDIR /app/src
EXPOSE 8080

COPY ./src /app/src

ENTRYPOINT ["python", "api.py"]
