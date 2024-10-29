import os
import tempfile
from pathlib import Path

# Project structure
# -----------------
APP_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = APP_DIR.parent.absolute()
TEMP_DIR = Path(tempfile.gettempdir())

# Environment variables
# ---------------------
DEV = os.environ.get("DEV", False)
SERVER_LOC = os.environ.get("SERVER_LOC", "http://localhost:8000")

print(SERVER_LOC)

# Common page configurations
# --------------------------
ABOUT = """
### Streamlit UI

Please report any bugs or issues on
[Github](https://github.com/hayabhay/fastapi-streamlit-starter/issues). Thanks!
"""


def get_page_config(page_title_prefix="", layout="wide"):
    return {
        "page_title": f"{page_title_prefix} FastAPI Streamlit Starter",
        "page_icon": "🔀",
        "layout": layout,
        "initial_sidebar_state": "expanded",
        "menu_items": {
            "Get Help": "https://twitter.com/hayabhay",
            "Report a bug": "https://github.com/hayabhay/fastapi-streamlit-starter/issues",
            "About": ABOUT,
        },
    }


def init_session(session_state, reset: bool = False):
    """Site wide function to intialize session state variables if they don't exist."""
    # Session states
    # --------------------------------
    if "server_loc" not in session_state or reset:
        session_state.SERVER_LOC = SERVER_LOC
