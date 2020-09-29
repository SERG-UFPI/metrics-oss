from datetime import datetime
from time import sleep

from requests import get

from settings.settings import AUTH, BASE_URL


def check_rate_limit(response):
    ratelimit_remaining = response.headers.get('X-Ratelimit-Remaining')
    if ratelimit_remaining == 0:
        ratelimit_reset = response.headers.get('X-Ratelimit-Reset')
        now = int(datetime.now().timestamp())
        wait_seconds = (ratelimit_remaining - now) + 1
        sleep(wait_seconds)
        return False
    return True
        

def make_request(path):
    url = f"{BASE_URL}/{PATH}"
    while True:
        response = get(url, headers=AUTH)
        if check_rate_limit(response):
            return response.json()
