ARG upperroom_version=latest

FROM docker.pkg.github.com/thepointchurch/upperroom/upperroom:$upperroom_version AS install-image
COPY . /django/
WORKDIR /django 
ENV POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1
RUN poetry install --no-dev --no-root
RUN poetry build --format wheel && .venv/bin/pip install dist/*.whl


FROM docker.pkg.github.com/thepointchurch/upperroom/upperroom:$upperroom_version AS font-image
RUN sed -i '/^deb http:\/\/deb.debian.org\/debian .* main$/ s/$/ contrib/' /etc/apt/sources.list
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends \
    ca-certificates \
    netbase \
    ttf-mscorefonts-installer
WORKDIR /usr/local/share/fonts
RUN wget -qO - https://github.com/mozilla/Fira/archive/4.106.tar.gz | tar -xvzf - Fira-4.106/otf --strip-components=2


FROM docker.pkg.github.com/thepointchurch/upperroom/upperroom:$upperroom_version AS build-image
COPY --from=install-image /django/dist/*.whl /django/thepoint.whl
COPY --from=font-image /usr/share/fonts/truetype/msttcorefonts /usr/local/share/fonts /usr/local/share/fonts/
RUN /django/.venv/bin/pip install /django/thepoint.whl && rm -f /django/thepoint.whl

ARG version
ARG build_date

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.version="$version"
LABEL org.label-schema.build-date="$build_date"
LABEL org.label-schema.url="https://github.com/thepointchurch/thepoint"
LABEL org.label-schema.description="The Point Church Website"
