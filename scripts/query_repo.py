from clone_repo import clone_repo as clone
from db import add_repos_to_db
from github_api import make_request

PER_PAGE = 100
LIMIT_OF_SEARCH = 10
SEARCH_PATH = "search/repositories"


def get_number_of_pages(path):
    data = make_request(path)
    total_count = data.get("total_count", 0)
    pages = (total_count // PER_PAGE) + 1 if total_count >= 100 else 2
    return pages if pages <= LIMIT_OF_SEARCH else LIMIT_OF_SEARCH + 1


def query_repos(query: str):
    path = f"{SEARCH_PATH}?q={query}"
    pages = get_number_of_pages(path)
    lang_query = []
    for page in range(1, pages + 1):
        url = f"{path}&per_page={PER_PAGE}&page={page}"
        data = make_request(url)
        lang_query += data.get("items", [])
    return lang_query


if __name__ == "__main__":
    while True:
        input_message = "Type your query string (example: language:java+stars:>=10000&sort=star&order=desc) or hit ENTER to exit:"
        query = input(input_message)
        if query == "" or query is None:
            print("Exiting")
            break
        result = query_repos(query)
        print("Saving results...")
        add_repos_to_db(result)
        print("Results saved into database...")
        print("Cloning the repos...")
        for repo in result:
            repo_id = repo.get("id")
            owner, repo = repo.get("full_name").split("/")
            print(f"Cloning the repo {owner}/{repo}")
            clone(owner, repo, repo_id)
