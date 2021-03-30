ARG upperroom_version=latest

FROM python:3.9-slim AS compile-image
RUN apt-get -y update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libpq-dev zlib1g-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install poetry=="1.1.4" wheel
COPY . /django/
WORKDIR /django 
ENV POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1
RUN poetry install --no-dev --no-root
RUN poetry build --format wheel


FROM debian:buster-slim as font-image
RUN sed -i '/^deb http:\/\/deb.debian.org\/debian .* main$/ s/$/ contrib/' /etc/apt/sources.list
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends \
    ca-certificates \
    netbase \
    ttf-mscorefonts-installer
WORKDIR /usr/local/share/fonts
RUN wget -qO - https://github.com/mozilla/Fira/archive/4.106.tar.gz | tar -xvzf - Fira-4.106/otf --strip-components=2


FROM docker.pkg.github.com/thepointchurch/upperroom/upperroom:$upperroom_version AS build-image
USER root
COPY --from=compile-image /django/dist/*.whl /django/
COPY --from=font-image /usr/share/fonts/truetype/msttcorefonts /usr/local/share/fonts /usr/local/share/fonts/
RUN /django/.venv/bin/pip install /django/*.whl && rm -f /django/*.whl
RUN ln -s upperroom /django/.venv/bin/thepoint && ln -s upperroom-sendrosteremails /django/.venv/bin/thepoint-sendrosteremails

USER django:django

ARG version
ARG build_date

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.version="$version"
LABEL org.label-schema.build-date="$build_date"
LABEL org.label-schema.url="https://github.com/thepointchurch/thepoint"
LABEL org.label-schema.description="The Point Church Website"
