import requests
from settings.settings import ELASTIC_URL


def get_metric(body: dict, github: bool) -> dict:
    index = "github" if github else "git"
    url = f"{ELASTIC_URL}/{index}/_search"
    response = requests.post(url, json=body)
    return response.json()
