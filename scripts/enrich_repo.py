import subprocess

import requests
from db import (
    get_all_repos_given_clone_info,
    get_all_repos_without_clone_info,
    update_clone_info,
)
from settings.settings import ELASTIC_URL, GITHUB_OAUTH_TOKEN, TOKENS
from tqdm import tqdm

# Strings that represent any error in the debug info of
# the execution of p2o.py and we need to replace
# the github token
ERROR_KEYS = ["raise", "exception", "exceptions", "RetryError"]

# This counter is to select which token will be used at the time
# The maximum number is the size of the list of tokens
use_token_counter = 0


def get_token(next_token: bool = False) -> str:
    if next_token:
        global use_token_counter
        if use_token_counter < len(GITHUB_OAUTH_TOKEN):
            use_token_counter += 1
    return TOKENS[use_token_counter]


def enrich_git(owner: str, repository: str) -> None:
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


def enrich_github(owner: str, repository: str) -> None:
    # Produce github and github_raw indexes from GitHub issues and prs
    # Do not use '--sleep-for-rate' in this case because we want to see the error
    next_token = False
    while True:
        token = get_token(next_token=next_token)
        result = subprocess.run(
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
                token,
            ],
            capture_output=True,
        )
        log = result.stderr.decode("utf-8")
        if any(error in log for error in ERROR_KEYS):
            next_token = True
        else:
            break


def enrich_repo(owner: str, repository: str) -> None:
    try:
        enrich_git(owner=owner, repository=repository)
        enrich_github(owner=owner, repository=repository)
    except Exception as e:
        return str(e)
    return ""


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
        repos = get_all_repos_given_clone_info() + get_all_repos_without_clone_info()
        print("Enrich some repos..")
        for repo in tqdm(repos):
            owner, repository = repo.full_name.split("/")
            error = enrich_repo(owner, repository)
            update_clone_info(repo.id, error=error)
