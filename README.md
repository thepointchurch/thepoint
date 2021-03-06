![Release](https://github.com/thepointchurch/thepoint/workflows/Release/badge.svg)
![Docker Image](https://github.com/thepointchurch/thepoint/workflows/Docker%20Image/badge.svg)

# The Point Church Website #

This is a Django project for The Point Church's website.

## Development

To set up a development environment:

1. [Install poetry](https://python-poetry.org/docs/#installation)

2. Clone the `testing` repository:

    ```
    git clone -branch testing https://github.com/thepointchurch/thepoint.git
    cd thepoint
    ```

3. Set up the poetry environment:

    ```
    poetry install -E aws -E cache -E pgsql -E google
    poetry run pre-commit install
    poetry shell
    ```

4. Export config variables:

    ```
    export DEBUG='True'
    export DATABASE_URL='sqlite:///thepoint.sqlite3'
    export SECRET_KEY='12345678'
    export DJANGO_SETTINGS_MODULE=thepoint.settings
    ```

    or place them in a an environment file at `thepoint/.env`:

    ```
    cat >thepoint/.env <<DEV_ENV
    DEBUG='True'
    DATABASE_URL='sqlite:///thepoint.sqlite3'
    SECRET_KEY='12345678'
    DJANGO_SETTINGS_MODULE=thepoint.settings
    DEV_ENV
    ```

5. Start a test server:

    ```
    thepoint runserver
    ```
