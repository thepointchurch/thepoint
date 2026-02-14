ARG upperroom_version=latest

FROM python:3.13-alpine AS compile-image
RUN apk add --no-cache \
         build-base \
         linux-headers
COPY --from=ghcr.io/astral-sh/uv:0.10.2-python3.13-alpine /usr/local/bin/uv /usr/local/bin/uvx /bin/
COPY . /django/
WORKDIR /django
ENV PYTHONDONTWRITEBYTECODE=1 \
    UV_NO_DEV=1
RUN uv build --wheel \
    && uv sync --frozen --extra aws --extra cache --extra pgsql \

FROM python:3.13-alpine AS font-image
RUN apk add --no-cache msttcorefonts-installer fontconfig \
    && update-ms-fonts
RUN wget -qO - https://github.com/mozilla/Fira/archive/4.106.tar.gz | tar -C /usr/share/fonts -xvzf - Fira-4.106/otf --strip-components=2 \
    && fc-cache -f


FROM ghcr.io/thepointchurch/upperroom/upperroom:$upperroom_version AS build-image
COPY --from=font-image /usr/share/fonts /usr/share/fonts/
COPY --from=compile-image /django/dist/*.whl /django/
USER root
RUN uv pip install /django/*.whl && rm -f /django/*.whl

USER django:django

ARG version
ARG build_date

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.version="$version"
LABEL org.label-schema.build-date="$build_date"
LABEL org.label-schema.url="https://github.com/thepointchurch/thepoint"
LABEL org.label-schema.description="The Point Church Website"
