import os

from db import update_clone_info
from settings.settings import GITHUB_OAUTH_TOKEN


def clone_repo(owner, repository, repo_id):
    path = "./tmp/{0}/{1}".format(owner, repository)

    if not os.path.exists(path):
        os.makedirs(path)

    command_git = (
        f"perceval git https://github.com/{owner}/{repository}.git "
        f"--git-path {path}.git > {path}-git.json"
    )
    command_github = (
        f"perceval github {owner} {repository} -o "
        f"{path}-github.json -t {GITHUB_OAUTH_TOKEN}"
    )

    error = ""

    try:
        os.system(command_git)
        os.system(command_github)
    except Exception as e:
        error = str(e)

    update_clone_info(repo_id, error)
