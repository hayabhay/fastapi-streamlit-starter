import os
import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict

# Set the directory structure
APP_DIR = pathlib.Path(__file__).parent.absolute()
PROJECT_DIR = APP_DIR.parent

class Settings(BaseSettings):
    myenv: str = "dev"

    model_config = SettingsConfigDict(env_file='.env')


# TODO: Check if this actually works properly before using it

# # Check if the app is in production. Default is False.
# MODE = os.environ.get("MODE", "dev").lower()
# # If in prod mode, set up the logging client
# if MODE == "prod":
#     from google.cloud import logging
#     # Set the logging client
#     logging_client = logging.Client()
#     # Initialize the logger
#     logging_client.setup_logging()
