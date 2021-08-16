import os

from db import update_clone_info


def clone_repo(owner, repository, repo_id):
    path = "../tmp/{0}/{1}".format(owner, repository)

    if not os.path.exists(path):
        os.makedirs(path)

    command = "perceval git https://github.com/{0}/{1}.git --git-path {2}.git > {2}.json".format(
        owner, repository, path
    )

    error = ""

    try:
        os.system(command)
    except Exception as e:
        error = str(e)

    update_clone_info(repo_id, error)
