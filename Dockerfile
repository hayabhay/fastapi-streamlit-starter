# NOTE: This is likely suboptimal, but it works for now. I'm sure there are better ways to do this.
# TODO: Refactor this to be more efficient, secure, and clean.
# Source: https://github.com/orgs/python-poetry/discussions/1879#discussioncomment-216865
# --------------------------------------------------------------------------------
# ------------------ Base image - used to build the application ------------------
# --------------------------------------------------------------------------------
FROM python:3.12.7-slim-bookworm AS python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    # make poetry install to this location
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# --------------------------------------------------------------------------------
# --------- Build image - to build deps + create our virtual environment ---------
# --------------------------------------------------------------------------------
FROM python-base AS builder-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -


# NOTE: "We want to cache our requirements and only reinstall them when
# pyproject.toml or poetry.lock files change. Otherwise builds will be slow."
# (https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker)
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN --mount=type=cache,target=/root/.cache \
    poetry install

# --------------------------------------------------------------------------------
# ------------ Development image - used during development / testing -------------
# --------------------------------------------------------------------------------
FROM python-base AS dev
WORKDIR $PYSETUP_PATH
ENV MODE=dev
# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev

# Copy the rest of the application & set it up
COPY ./api /app/api
COPY ./ui /app/ui

# Copy a script to start both services
COPY dev.sh /app/dev.sh
RUN chmod +x /app/dev.sh

EXPOSE 8000
EXPOSE 8501

# Run main.py when the container launches
WORKDIR /app
CMD ["./dev.sh"]

# --------------------------------------------------------------------------------
# ------------ UI Only image - used mainly for staging server --------------------
# --------------------------------------------------------------------------------
FROM python-base AS ui
WORKDIR $PYSETUP_PATH
ENV MODE=dev

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev,gcp

# Copy the rest of the application & set it up
COPY ./ui /app/ui

# Run main.py when the container launches
WORKDIR /app

CMD ["sh", "-c", "streamlit run ui/01_🏠_Home.py --server.port {PORT:-8501}"]


# --------------------------------------------------------------------------------
# ---------------- Production image - Fast API only --------------------
# --------------------------------------------------------------------------------
FROM python-base AS prod
WORKDIR $PYSETUP_PATH
ENV MODE=prod
ENV ENV_FILENAME=
# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=prod

COPY ./api /app/api
WORKDIR /app/api

# Default port set to 8000
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000}"]
