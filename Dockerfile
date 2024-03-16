ARG upperroom_version=latest

FROM python:3.11-alpine AS compile-image
RUN apk add --no-cache \
         build-base \
         libffi-dev
RUN pip install --root-user-action=ignore --upgrade pip setuptools && \
    pip install --root-user-action=ignore "poetry~=1.8" wheel
COPY . /django/
WORKDIR /django
ENV POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1
RUN poetry install --no-root \
    && poetry build --format wheel


FROM python:3.11-alpine AS font-image
RUN apk add --no-cache msttcorefonts-installer \
    && update-ms-fonts
RUN wget -qO - https://github.com/mozilla/Fira/archive/4.106.tar.gz | tar -C /usr/share/fonts -xvzf - Fira-4.106/otf --strip-components=2 \
    && fc-cache -f


FROM ghcr.io/thepointchurch/upperroom/upperroom:$upperroom_version AS build-image
COPY --from=font-image /usr/share/fonts /usr/share/fonts/
COPY --from=compile-image /django/dist/*.whl /django/
RUN /django/.venv/bin/pip install --root-user-action=ignore /django/*.whl && rm -f /django/*.whl

USER django:django

ARG version
ARG build_date

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.version="$version"
LABEL org.label-schema.build-date="$build_date"
LABEL org.label-schema.url="https://github.com/thepointchurch/thepoint"
LABEL org.label-schema.description="The Point Church Website"
