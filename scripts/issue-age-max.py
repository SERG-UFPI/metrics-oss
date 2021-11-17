import os

from common import get_metric
from db import get_cloned_repos
from files import save_file
from tqdm import tqdm

FILENAME = f"{os.getcwd()}/scripts/issues-age-max.json"


def get_result(url: str) -> dict:
    body = {
        "aggs": {
            "5": {"avg": {"field": "time_open_days"}},
            "6": {
                "percentiles": {
                    "field": "time_open_days",
                    "percents": [50],
                    "keyed": False,
                }
            },
            "7": {"max": {"field": "time_open_days"}},
        },
        "size": 0,
        "highlight": {
            "pre_tags": ["@kibana-highlighted-field@"],
            "post_tags": ["@/kibana-highlighted-field@"],
            "fields": {"*": {}},
            "require_field_match": False,
            "fragment_size": 2147483647,
        },
        "_source": {"excludes": []},
        "stored_fields": ["*"],
        "script_fields": {
            "painless_delay": {
                "script": {
                    "source": "if (doc.containsKey('state')) {\n  if (doc['state'].value == 'closed') {\n     return Duration.between(LocalDateTime.ofInstant(Instant.ofEpochMilli(doc['grimoire_creation_date'].value.millis), ZoneId.of('Z')), LocalDateTime.ofInstant(Instant.ofEpochMilli(doc['closed_at'].value.millis), ZoneId.of('Z'))).toMinutes()/1440.0;\n  } else {\n     return Duration.between(LocalDateTime.ofInstant(Instant.ofEpochMilli(doc['grimoire_creation_date'].value.millis), ZoneId.of('Z')), LocalDateTime.ofInstant(Instant.ofEpochMilli(new Date().getTime()), ZoneId.of('Z'))).toMinutes()/1440.0;\n  }\n\n  \n} else {\n  return 0;\n}",
                    "lang": "painless",
                }
            }
        },
        "docvalue_fields": [
            {"field": "closed_at", "format": "date_time"},
            {"field": "created_at", "format": "date_time"},
            {"field": "grimoire_creation_date", "format": "date_time"},
            {"field": "merged_at", "format": "date_time"},
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
                    {
                        "query_string": {
                            "query": "pull_request:false",
                            "analyze_wildcard": True,
                            "default_field": "*",
                        }
                    },
                    {"match_phrase": {"repository": {"query": url}}},
                    {"match_phrase": {"repository": {"query": url}}},
                ],
                "filter": [],
                "should": [],
                "must_not": [],
            }
        },
    }
    result = get_metric(body, True)
    value = result.get("aggregations", {}).get("6", {}).get("values", [])[0].get("value", 0)
    return value


def generate_metric(repos: list) -> None:
    results = {}
    for repo in tqdm(repos):
        results[repo.full_name] = get_result(repo.html_url)
    save_file(results, FILENAME)


if __name__ == "__main__":
    repos = get_cloned_repos()
    generate_metric(repos)
