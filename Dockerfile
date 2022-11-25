ARG upperroom_version=latest

FROM python:3.11-slim AS compile-image
USER root
RUN apt-get -y update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libpq-dev zlib1g-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/pip install --upgrade pip && \
    /usr/local/bin/pip install poetry=="1.2.2" wheel
COPY . /django/
WORKDIR /django
ENV POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1
RUN /usr/local/bin/poetry install --no-root \
    && /usr/local/bin/poetry build --format wheel


FROM python:3.11-slim AS font-image
USER root
RUN sed -i '/^deb http:\/\/deb.debian.org\/debian .* main$/ s/$/ contrib/' /etc/apt/sources.list \
    && apt-get -y update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        netbase \
        ttf-mscorefonts-installer
RUN mkdir /usr/local/share/fonts \
    && wget -qO - https://github.com/mozilla/Fira/archive/4.106.tar.gz | tar -xvzf - Fira-4.106/otf --strip-components=2 -C /usr/local/share/fonts


FROM ghcr.io/thepointchurch/upperroom/upperroom:$upperroom_version AS build-image
USER root
COPY --from=font-image /usr/share/fonts/truetype/msttcorefonts /usr/local/share/fonts /usr/local/share/fonts/
COPY --from=compile-image /django/dist/*.whl /django/
RUN /django/.venv/bin/pip install /django/*.whl && rm -f /django/*.whl

USER django:django

ARG version
ARG build_date

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.version="$version"
LABEL org.label-schema.build-date="$build_date"
LABEL org.label-schema.url="https://github.com/thepointchurch/thepoint"
LABEL org.label-schema.description="The Point Church Website"
