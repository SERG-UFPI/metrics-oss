import os

from common import get_metric
from db import get_cloned_repos
from files import save_file
from tqdm import tqdm

FILENAME = f"{os.getcwd()}/scripts/contributors.json"


def get_result(url: str) -> dict:
    body = {
        "aggs": {"1": {"cardinality": {"field": "author_uuid"}}},
        "size": 0,
        "_source": {"excludes": []},
        "stored_fields": ["*"],
        "script_fields": {
            "data_source": {
                "script": {
                    "source": "if (doc['_index'].value.contains('-')) {\n    doc['_index'].value.substring(0, doc['_index'].value.indexOf(\"-\"))\n\n} else if (doc['_index'].value.contains('_')) {\n    if (doc['_index'].value.substring(0, doc['_index'].value.indexOf(\"_\")).equalsIgnoreCase(\"github\")) {\n       if (doc['pull_request'].value) {\n            \"github_pull_requests\"\n        } else {\n            \"github_issues\"\n        }\n\n    } else {\n        doc['_index'].value.substring(0, doc['_index'].value.indexOf(\"_\"))\n\n    }\n\n} else {\n    doc['_index'].value\n}",
                    "lang": "painless",
                }
            },
            "painless_unique_id": {
                "script": {
                    "source": "if (doc['_index'].value.startsWith('git_')) {\n    doc['hash'].value\n} else {\n    doc['uuid'].value\n}",
                    "lang": "painless",
                }
            },
            "painless_closed_at": {
                "script": {
                    "source": "if (doc['_index'].value.startsWith('github')) {\n    if (!doc['closed_at'].empty) {\n        doc['closed_at'].value\n    }\n\n} else if (doc['_index'].value.startsWith('gerrit')) {\n    if (!doc['closed'].empty) {\n        doc['closed'].value\n    }\n\n} else if (doc['_index'].value.startsWith('gitlab')) {\n    if (!doc['closed_at'].empty) {\n        doc['closed_at'].value\n    }\n\n} else if (doc['_index'].value.startsWith('jira')) {\n    if (!doc['resolution_date'].empty) {\n        doc['resolution_date'].value\n    }\n}",
                    "lang": "painless",
                }
            },
        },
        "docvalue_fields": [
            {"field": "author_date", "format": "date_time"},
            {"field": "changeddate_date", "format": "date_time"},
            {"field": "closed", "format": "date_time"},
            {"field": "closed_at", "format": "date_time"},
            {"field": "comment_updated_at", "format": "date_time"},
            {"field": "commit_date", "format": "date_time"},
            {"field": "created_at", "format": "date_time"},
            {"field": "creation_date", "format": "date_time"},
            {"field": "date", "format": "date_time"},
            {"field": "delta_ts", "format": "date_time"},
            {"field": "demography_max_date", "format": "date_time"},
            {"field": "demography_min_date", "format": "date_time"},
            {"field": "grimoire_creation_date", "format": "date_time"},
            {"field": "issue_closed_at", "format": "date_time"},
            {"field": "issue_created_at", "format": "date_time"},
            {"field": "issue_updated_at", "format": "date_time"},
            {"field": "merged_at", "format": "date_time"},
            {"field": "metadata__enriched_on", "format": "date_time"},
            {"field": "metadata__timestamp", "format": "date_time"},
            {"field": "metadata__updated_on", "format": "date_time"},
            {"field": "opened", "format": "date_time"},
            {"field": "question_last_activity_at", "format": "date_time"},
            {"field": "solved_at", "format": "date_time"},
            {"field": "updated_at", "format": "date_time"},
            {"field": "utc_author", "format": "date_time"},
            {"field": "utc_commit", "format": "date_time"},
        ],
        "query": {
            "bool": {
                "must": [
                    {"match_all": {}},
                    {"match_all": {}},
                    {"match_phrase": {"repository": {"query": url}}},
                    {
                        "script": {
                            "script": {
                                "source": "boolean compare(Supplier s, def v) {return s.get() == v;}compare(() -> { if (doc['_index'].value.contains('-')) {\n    doc['_index'].value.substring(0, doc['_index'].value.indexOf(\"-\"))\n\n} else if (doc['_index'].value.contains('_')) {\n    if (doc['_index'].value.substring(0, doc['_index'].value.indexOf(\"_\")).equalsIgnoreCase(\"github\")) {\n       if (doc['pull_request'].value) {\n            \"github_pull_requests\"\n        } else {\n            \"github_issues\"\n        }\n\n    } else {\n        doc['_index'].value.substring(0, doc['_index'].value.indexOf(\"_\"))\n\n    }\n\n} else {\n    doc['_index'].value\n} }, params.value);",
                                "lang": "painless",
                                "params": {"value": "github"},
                            }
                        }
                    },
                ],
                "filter": [],
                "should": [],
                "must_not": [{"match_phrase": {"author_bot": {"query": True}}}],
            }
        },
    }
    result = get_metric(body, True)
    value = result.get("aggregations", {}).get("1", {}).get("value", 0)
    return value


def generate_metric(repos: list) -> None:
    results = {}
    for repo in tqdm(repos):
        results[repo.full_name] = get_result(repo.html_url)
    save_file(results, FILENAME)


if __name__ == "__main__":
    repos = get_cloned_repos()
    generate_metric(repos)
