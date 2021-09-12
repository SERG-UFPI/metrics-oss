import requests
from interfaces import Author


def get_author_metrics():

    body = {
        "aggs": {
            "2": {
                "terms": {
                    "field": "author_name",
                    "size": 20,
                    "order": {"_count": "desc"},
                },
                "aggs": {
                    "3": {
                        "cardinality": {"field": "project", "precision_threshold": 3000}
                    },
                    "4": {"sum": {"field": "lines_added"}},
                    "5": {"sum": {"field": "lines_removed"}},
                    "6": {"avg": {"field": "files"}},
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
                            "analyze_wildcard": True,
                            "default_field": "*",
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
                    {
                        "range": {
                            "grimoire_creation_date": {
                                "gte": 1314667977510,
                                "lte": 1630287177510,
                                "format": "epoch_millis",
                            }
                        }
                    },
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

    url = "http://localhost:9200/git/_search"

    response = requests.post(url, json=body)

    authors = []

    for data in response.json()["aggregations"]["2"]["buckets"]:
        name = data["key"]
        commits = data["doc_count"]
        projects = data["3"]["value"]
        added_lines = int(data["4"]["value"])
        removed_lines = int(data["5"]["value"])
        avg_files = data["6"]["value"]

        author = Author(name, commits, projects, added_lines, removed_lines, avg_files)

        authors.append(author)

    return authors
