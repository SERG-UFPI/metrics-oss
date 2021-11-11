import os

from common import get_metric
from db import get_cloned_repos
from files import save_file
from tqdm import tqdm

FILENAME = f"{os.getcwd()}/scripts/code-changes-lines-added.json"


def get_result(url: str) -> dict:
    body = {
        "aggs": {
            "2": {
                "terms": {"field": "repo_name", "size": 50, "order": {"1": "desc"}},
                "aggs": {
                    "1": {
                        "cardinality": {"field": "hash", "precision_threshold": 10000}
                    },
                    "3": {
                        "cardinality": {
                            "field": "author_uuid",
                            "precision_threshold": 3000,
                        }
                    },
                    "4": {
                        "cardinality": {
                            "field": "author_org_name",
                            "precision_threshold": 3000,
                        }
                    },
                    "5": {"avg": {"field": "lines_changed"}},
                    "6": {"avg": {"field": "files"}},
                    "7": {"sum": {"field": "lines_added"}},
                    "8": {"sum": {"field": "lines_removed"}},
                },
            }
        },
        "size": 0,
        "_source": {"excludes": []},
        "stored_fields": ["*"],
        "script_fields": {
            "painless_inverted_lines_removed_git": {
                "script": {
                    "source": "return doc['lines_removed'].value * -1",
                    "lang": "painless",
                }
            }
        },
        "docvalue_fields": [
            {"field": "author_date", "format": "date_time"},
            {"field": "commit_date", "format": "date_time"},
            {"field": "demography_max_date", "format": "date_time"},
            {"field": "demography_min_date", "format": "date_time"},
            {"field": "grimoire_creation_date", "format": "date_time"},
            {"field": "metadata__enriched_on", "format": "date_time"},
            {"field": "metadata__timestamp", "format": "date_time"},
            {"field": "metadata__updated_on", "format": "date_time"},
            {"field": "utc_author", "format": "date_time"},
            {"field": "utc_commit", "format": "date_time"},
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "default_field": "*",
                            "analyze_wildcard": True,
                            "query": "*",
                        }
                    },
                    {
                        "query_string": {
                            "query": "*",
                            "analyze_wildcard": True,
                            "default_field": "*",
                        }
                    },
                    {"match_phrase": {"repo_name": {"query": url}}},
                ],
                "filter": [],
                "should": [],
                "must_not": [
                    {"match_phrase": {"files": {"query": "0"}}},
                    {"match_phrase": {"author_bot": {"query": True}}},
                ],
            }
        },
    }
    result = get_metric(body, False)
    buckets = result.get("aggregations", {}).get("2", {}).get("buckets", [])
    value = 0 if len(buckets) == 0 else buckets[0].get("7", {}).get("value", 0)
    return value


def generate_metric(repos: list) -> None:
    results = {}
    for repo in tqdm(repos):
        results[repo.full_name] = get_result(repo.html_url)
    save_file(results, FILENAME)


if __name__ == "__main__":
    repos = get_cloned_repos()
    generate_metric(repos)
