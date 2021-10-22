import logging
import os
import subprocess

import requests
from db import (
    get_all_repos_given_clone_info,
    get_all_repos_without_clone_info,
    update_clone_info,
)
from settings.settings import ELASTIC_URL, HOME_PATH, TOKENS
from tqdm import tqdm

# Strings that represent any error in the debug info of
# the execution of p2o.py and we need to replace
# the github token
EXCEPTIONS_KEYS = ["IntegrityError", "ArchiveError"]
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


def move_archive():
    destination_path = "./.perceval/"
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    logging.info("Archiving here due to disk space")
    command = f"cp -r {HOME_PATH}/* {destination_path} && rm -rf {HOME_PATH}"
    os.system(command)


def enrich_git(owner: str, repository: str) -> str:
    # Produce git and git_raw indexes from git repo
    logging.info(f"Enriching repo with Git {owner}/{repository}")
    result = subprocess.run(
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
        capture_output=True,
        text=True,
    )
    log = result.stdout + result.stderr
    print(log)
    logging.info(f"Finished Git for {owner}/{repository}")
    return log if any(error in log for error in ERROR_KEYS) else ""


def enrich_github(owner: str, repository: str, token: str) -> str:
    # Produce github and github_raw indexes from GitHub issues and prs
    repeat = 0
    logging.info(f"Enriching repo with Github {owner}/{repository}")
    while True:
        logging.info(f"Using token {token} to retrieve info from {owner}/{repository}")
        logging.info(f"In loop for {owner}/{repository} {repeat} times")
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
                "--sleep-for-rate",
            ],
            capture_output=True,
            text=True,
        )
        log = result.stdout + result.stderr
        print(log)
        if not any(error in log for error in EXCEPTIONS_KEYS):
            logging.info(f"Finished Github for {owner}/{repository}")
            break
    return log if any(error in log for error in ERROR_KEYS) else ""


def enrich_repo(owner: str, repository: str, token: str) -> None:
    try:
        error_git = enrich_git(owner=owner, repository=repository)
        error_github = enrich_github(owner=owner, repository=repository, token=token)
        full_error = error_git + error_github
        if full_error != "":
            logging.info(f"Error for {owner}/{repository}")
            logging.info(full_error)
        move_archive()
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
        tokens = TOKENS
        for repo in tqdm(repos):
            owner, repository = repo.full_name.split("/")
            token = tokens.pop(0)
            tokens.append(token)
            error = enrich_repo(owner, repository, token)
            update_clone_info(repo.id, error=error)
