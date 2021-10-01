import subprocess

import requests
import tqdm
from db import get_all_repos_given_clone_info, update_clone_info
from settings.settings import ELASTIC_URL, GITHUB_OAUTH_TOKEN


def enrich_repo(owner: str, repository: str) -> None:
    # Produce git and git_raw indexes from git repo
    subprocess.run(
        [
            "p2o.py",
            "--enrich",
            "--index",
            "git_raw",
            "--index-enrich",
            "git",
            "-e",
            ELASTIC_URL,
            "--no_inc",
            "--debug",
            "git",
            f"https://github.com/{owner}/{repository}",
        ]
    )

    # Produce github and github_raw indexes from GitHub issues and prs
    subprocess.run(
        [
            "p2o.py",
            "--enrich",
            "--index",
            "github_raw",
            "--index-enrich",
            "github",
            "-e",
            ELASTIC_URL,
            "--no_inc",
            "--debug",
            "github",
            owner,
            repository,
            "-t",
            GITHUB_OAUTH_TOKEN,
            "--sleep-for-rate",
        ]
    )


def verify_elasticsearch() -> bool:
    try:
        requests.get(ELASTIC_URL)
    except requests.exceptions.ConnectionError:
        print(f"Elasticsearch is not running with the URL {ELASTIC_URL}")
        return False
    return True


if __name__ == "__main__":
    """
    Script that will enrich the repos
    saved in the database
    1 - We need to query all repos that weren't enrich one month ago
    2 - Verify if there is a elasticsearch instance running
    3 - Use the func to enrich them and save to elasticsearch
    """
    running_es = verify_elasticsearch()
    if running_es:
        repos = get_all_repos_given_clone_info()
        print("Enrich some repos..")
        for repo in tqdm(repos):
            owner, repository = repo.full_name.split("/")
            enrich_repo(owner, repository)
            update_clone_info(repo.id)
