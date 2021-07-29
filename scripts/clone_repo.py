import os

def clone_repo(onwer, repository):
    path = "../tmp/{0}/{1}".format(onwer, repository)

    if not os.path.exists(path):
        os.makedirs(path)

    command = "perceval git https://github.com/{0}/{1}.git --git-path {2}.git > {2}.json".format(onwer, repository, path)

    os.system(command)


if __name__ == "__main__":
    clone_repo("eduardocesb", "algoritmos")
    clone_repo("luchiago", "tse-awesome-project")