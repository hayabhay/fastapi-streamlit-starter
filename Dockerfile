# --------------------------------------------------------------------------------
# ------------------ Base image - used to build the application ------------------
# --------------------------------------------------------------------------------
FROM python:3.12.5-slim-bookworm AS base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential

COPY ./requirements.txt /requirements.txt
COPY ./requirements-dev.txt /requirements-dev.txt

# Install core dependencies using pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

# --------------------------------------------------------------------------------
# ------------ Development image - used during development / testing -------------
# --------------------------------------------------------------------------------
FROM base AS dev
ENV MODE=dev

# Install dev dependencies
RUN pip install --no-cache-dir -r /requirements-dev.txt

# Set path to the application
ENV PYTHONPATH="/app/api:/app/ui"

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
FROM base AS ui
ENV MODE=dev

# Install dev dependencies
RUN pip install --no-cache-dir -r /requirements-dev.txt

# Copy the rest of the application & set it up
COPY ./ui /app/ui

# Run main.py when the container launches
WORKDIR /app

CMD ["sh", "-c", "streamlit run ui/01_🏠_Home.py --server.port {PORT:-8501}"]


# --------------------------------------------------------------------------------
# ---------------- Production image - Fast API only --------------------
# --------------------------------------------------------------------------------
FROM base AS api
ENV MODE=prod
ENV ENV_FILENAME=

COPY ./api /app/api
WORKDIR /app/api

# Default port set to 8000
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000}"]
