from db import get_all_repositories
from files import save_file


def generate_file():
    repos = get_all_repositories()
    git = {"git": []}
    github_issues = {"github:issue": []}
    github_pull = {"github:pull": []}
    for r in repos:
        git["git"].append(r.url)
        github_issues["github:issue"].append(r.url)
        github_pull["github:pull"].append(r.url)

    projects = {"Metrics": {**git, **github_issues, **github_pull}}
    save_file(projects, "project.json")
