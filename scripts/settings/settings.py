import os

from dotenv import load_dotenv

load_dotenv()


keys = [
    os.getenv("GITHUB_OAUTH_TOKEN"),
    os.getenv("BASE_URL"),
    os.getenv("ELASTIC_URL"),
    os.getenv("HOME_PATH"),
]
GITHUB_OAUTH_TOKEN, BASE_URL, ELASTIC_URL, HOME_PATH = keys
if not all(keys):
    msg = (
        f"Missing key\n"
        f"GITHUB_OAUTH_TOKEN: {GITHUB_OAUTH_TOKEN}\n"
        f"BASE_URL: {BASE_URL}\n"
        f"ELASTIC_URL: {ELASTIC_URL}\n"
        F"HOME_PATH: {HOME_PATH}\n"
    )
    raise Exception(msg)

TOKENS = GITHUB_OAUTH_TOKEN.split(",")
AUTH = {"Authorization": f"token {TOKENS[0]}"}
