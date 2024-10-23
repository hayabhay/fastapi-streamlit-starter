import os
import pathlib

from dotenv import dotenv_values

# Set the directory structure
APP_DIR = pathlib.Path(__file__).parent.absolute()
PROJECT_DIR = APP_DIR.parent

# Check if the app is in production. Default is False.
MODE = os.environ.get("MODE", "dev").lower()

# If in prod mode, load env from secrets manager.
# This is for GCP & can be replaced as needed.
if MODE == "prod":
    # Since deployment is GCR, the .env file with secrets is directly
    # mounted as a volume within the container.
    ENV = dotenv_values("/.env")

    from google.cloud import logging
    # Set the logging client
    logging_client = logging.Client()
    # Initialize the logger
    logging_client.setup_logging()

# Else, its in dev mode. Load the .env file as an ENV variable
else:
    # Load the .env file directly
    ENV = dotenv_values(PROJECT_DIR / ".env")
