import os

from common import get_metric
from db import get_cloned_repos
from files import save_file
from tqdm import tqdm

FILENAME = f"{os.getcwd()}/scripts/median-time-to-first-response.json"


def get_result(url: str) -> dict:
    body = {
        "aggs": {
            "2": {
                "percentiles": {
                    "field": "time_to_first_attention",
                    "percents": [50],
                    "keyed": False,
                }
            }
        },
        "size": 0,
        "_source": {"excludes": []},
        "stored_fields": ["*"],
        "script_fields": {
            "data_source": {
                "script": {
                    "source": "if (doc['_index'].value.contains('-')) {\n    doc['_index'].value.substring(0, doc['_index'].value.indexOf(\"-\"))\n\n} else if (doc['_index'].value.contains('_')) {\n    if (doc['_index'].value.substring(0, doc['_index'].value.indexOf(\"_\")).equalsIgnoreCase(\"github\")) {\n       if (doc['pull_request'].value) {\n            \"github_pull_requests\"\n        } else {\n            \"github_issues\"\n        }\n\n    } else {\n        doc['_index'].value.substring(0, doc['_index'].value.indexOf(\"_\"))\n\n    }\n\n} else {\n    doc['_index'].value\n}",
                    "lang": "painless",
                }
            }
        },
        "docvalue_fields": [
            {"field": "closed_at", "format": "date_time"},
            {"field": "created_at", "format": "date_time"},
            {"field": "grimoire_creation_date", "format": "date_time"},
            {"field": "metadata__enriched_on", "format": "date_time"},
            {"field": "metadata__timestamp", "format": "date_time"},
            {"field": "metadata__updated_on", "format": "date_time"},
            {"field": "updated_at", "format": "date_time"},
        ],
        "query": {
            "bool": {
                "must": [
                    {"match_all": {}},
                    {"match_all": {}},
                    {"match_phrase": {"state": {"query": "closed"}}},
                    {"exists": {"field": "time_to_close_days"}},
                    {"exists": {"field": "time_to_first_attention"}},
                    {"match_phrase": {"repository": {"query": url}}},
                ],
                "filter": [],
                "should": [],
                "must_not": [{"match_phrase": {"author_bot": {"query": True}}}],
            }
        },
    }
    result = get_metric(body, True)
    values = result.get("aggregations", {}).get("2", {}).get("values", [])
    value = 0 if len(values) == 0 else values[0].get("value", 0)
    return value


def generate_metric(repos: list) -> None:
    results = {}
    for repo in tqdm(repos):
        results[repo.full_name] = get_result(repo.html_url)
    save_file(results, FILENAME)


if __name__ == "__main__":
    repos = get_cloned_repos()
    generate_metric(repos)
