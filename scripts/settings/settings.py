from dotenv import load_dotenv

load_dotenv()

import os

keys = [os.getenv("GITHUB_OAUTH_TOKEN"), os.getenv("BASE_URL")]
GITHUB_OAUTH_TOKEN, BASE_URL = keys
if not all(keys):
    msg = f"Missing key\nGITHUB_OAUTH_TOKEN: {GITHUB_OAUTH_TOKEN}\nBASE_URL: {BASE_URL}"
    raise Exception(msg)
AUTH = {"Authorization": f"token {GITHUB_OAUTH_TOKEN}"}
