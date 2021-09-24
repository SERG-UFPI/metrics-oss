import requests


def get_median():

    body = {
        "aggs": {
            "2": {
                "terms": {
                    "field": "github_repo",
                    "size": 50000,
                    "order": {"_key": "desc"},
                },
                "aggs": {
                    "1": {
                        "percentiles": {
                            "script": {
                                "source": "if (doc.containsKey('state')) {\n  if (doc['state'].value == 'closed') {\n     return Duration.between(LocalDateTime.ofInstant(Instant.ofEpochMilli(doc['grimoire_creation_date'].value.millis), ZoneId.of('Z')), LocalDateTime.ofInstant(Instant.ofEpochMilli(doc['closed_at'].value.millis), ZoneId.of('Z'))).toMinutes()/1440.0;\n  } else {\n     return Duration.between(LocalDateTime.ofInstant(Instant.ofEpochMilli(doc['grimoire_creation_date'].value.millis), ZoneId.of('Z')), LocalDateTime.ofInstant(Instant.ofEpochMilli(new Date().getTime()), ZoneId.of('Z'))).toMinutes()/1440.0;\n  }\n\n  \n} else {\n  return 0;\n}",
                                "lang": "painless",
                            },
                            "percents": [50],
                            "keyed": False,
                        }
                    }
                },
            }
        },
        "size": 0,
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
                    {"match_phrase": {"pull_request": {"query": False}}},
                    {"match_phrase": {"state": {"query": "closed"}}},
                    {
                        "range": {
                            "grimoire_creation_date": {
                                "gte": 1474082996002,
                                "lte": 1631849396002,
                                "format": "epoch_millis",
                            }
                        }
                    },
                    {"match_phrase": {"pull_request": {"query": False}}},
                    {"match_phrase": {"state": {"query": "closed"}}},
                ],
                "filter": [],
                "should": [],
                "must_not": [],
            }
        },
    }

    url = "http://localhost:9200/git/_search"

    response = requests.post(url, json=body)

    print(response.json())
