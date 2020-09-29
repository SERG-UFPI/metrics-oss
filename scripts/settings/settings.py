from dotenv import load_dotenv

load_dotenv()

import os

GITHUB_OAUTH_TOKEN = os.getenv("GITHUB_OAUTH_TOKEN")
AUTH = {"Authorization": f"token {GITHUB_OAUTH_TOKEN}"}
BASE_URL = os.getenv("BASE_URL")
