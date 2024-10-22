import os
import pathlib

from dotenv import dotenv_values

# Set the directory structure
APP_DIR = pathlib.Path(__file__).parent.absolute()
PROJECT_DIR = APP_DIR.parent

# Check if the app is in production. Default is False.
MODE = os.environ.get("MODE", "dev").lower()

# If in development mode, load the .env file as an ENV variable
if MODE == "dev":
    from loguru import logger

    # Load the .env file directly
    ENV = dotenv_values(PROJECT_DIR / ".env")

    # Set the logger
    logger.add(PROJECT_DIR / "logs" / "app.log", rotation="10 MB", retention="2 days")

    LOGGER = logger

# Else load it from secrets manager. This is for GCP & can be replaced as needed.
elif MODE == "prod":
    from io import StringIO

    from google.cloud import logging, secretmanager

    # First load the secrets from secrets manager
    client = secretmanager.SecretManagerServiceClient()
    # Project id must be passed through as an ENV variable
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    if not project_id:
        raise ValueError("Please set the GOOGLE_CLOUD_PROJECT as an ENV variable.")
    # Mame of the secret in secrets manager and should be set as an ENV variable
    env_filename = os.environ.get("ENV_FILENAME")
    if not env_filename:
        raise ValueError("Please set the ENV_FILENAME as an ENV variable.")

    # The full path to the secrets file
    name = f"projects/{project_id}/secrets/{env_filename}/versions/latest"
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode("UTF-8")
    # Load secrets by treating it as a file stream and passing it to dotenv_values
    ENV = dotenv_values(stream=StringIO(payload))

    # Set the logging client
    logging_client = logging.Client()
    # Set the logger
    LOGGER = logging_client.logger("app")

    # Set the log level
    LOGGER.set_log_filter("INFO")
