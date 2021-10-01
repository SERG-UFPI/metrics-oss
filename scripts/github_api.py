from datetime import datetime
from time import sleep

from requests import get
from settings.settings import AUTH, BASE_URL


def check_rate_limit(response):
    ratelimit_remaining = int(response.headers.get("X-Ratelimit-Remaining", 0))
    if ratelimit_remaining == 0:
        now = int(datetime.now().timestamp())
        ratelimit_time_reset = int(response.headers.get("X-RateLimit-Reset", 0))
        wait_seconds = (ratelimit_time_reset - now) + 1
        print(
            f"Waiting {wait_seconds} seconds or "
            f"{wait_seconds // 60} minutes to keep trying requests"
        )
        sleep(wait_seconds)
        return False
    return True


def make_request(path):
    url = f"{BASE_URL}/{path}"
    while True:
        response = get(url, headers=AUTH)
        if check_rate_limit(response):
            return response.json()
