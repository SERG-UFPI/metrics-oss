import logging
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
RETRY_KEYS = ["raise", "exception", "exceptions", "RetryError"]
ERROR_KEYS = ["Error", "error", "fatal"]

# This counter is to select which token will be used at the time
# The maximum number is the size of the list of tokens
use_token_counter = 0

datetime_format = "%d-%b-%y %H:%M:%S"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s::%(levelname)s::%(message)s",
    filename="enrich_repos.log",
    datefmt=datetime_format,
)


def get_token(next_token: bool = False) -> str:
    if next_token:
        global use_token_counter
        if use_token_counter < len(GITHUB_OAUTH_TOKEN):
            use_token_counter += 1
        if use_token_counter >= len(GITHUB_OAUTH_TOKEN):
            use_token_counter = 0
    return TOKENS[use_token_counter]


def enrich_git(owner: str, repository: str) -> str:
    # Produce git and git_raw indexes from git repo
    logging.info(f"Enriching repo with Git {owner}/{repository}")
    result = subprocess.check_output(
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
        ],
    )
    log = result.decode("utf-8")
    return log if any(error in log for error in ERROR_KEYS) else ""


def enrich_github(owner: str, repository: str) -> str:
    # Produce github and github_raw indexes from GitHub issues and prs
    # Do not use '--sleep-for-rate' in this case because we want to see the error
    next_token = False
    logging.info(f"Enriching repo with Github {owner}/{repository}")
    while True:
        token = get_token(next_token=next_token)
        logging.info(f"Using token {token} to retrieve info from {owner}/{repository}")
        result = subprocess.check_output(
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
        )
        log = result.decode("utf-8")
        if any(error in log for error in RETRY_KEYS):
            next_token = True
        else:
            break
    return log if any(error in log for error in ERROR_KEYS) else ""


def enrich_repo(owner: str, repository: str) -> None:
    try:
        error_git = enrich_git(owner=owner, repository=repository)
        error_github = enrich_github(owner=owner, repository=repository)
        full_error = error_git + error_github
        if full_error != "":
            logging.info(f"Error for {owner}/{repository}")
            logging.info(full_error)
        return full_error
    except Exception as e:
        logging.info(f"Error {e}")
        return str(e)


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
