from clone_repo import clone_repo
from db import add_repos_to_db
from github_api import make_request
from tqdm import tqdm

PER_PAGE = 100
LIMIT_OF_SEARCH = 10  # Limit of pagination
SEARCH_PATH = "search/repositories"


def get_number_of_pages(path):
    data = make_request(path)
    total_count = data.get("total_count", 0)
    pages = (total_count // PER_PAGE) + 1 if total_count >= 100 else 2
    return pages if pages <= LIMIT_OF_SEARCH else LIMIT_OF_SEARCH + 1


def query_repos(query: str, limit: int):
    path = f"{SEARCH_PATH}?q={query}"
    if limit <= PER_PAGE and limit != 0:
        pages = 1
        per_page = limit
    else:
        pages = get_number_of_pages(path)
        per_page = PER_PAGE
    lang_query = []
    for page in tqdm(range(1, pages + 1)):
        url = f"{path}&per_page={per_page}&page={page}"
        data = make_request(url)
        lang_query += data.get("items", [])
        if len(lang_query) == limit:
            break
    return lang_query


def clone_with_perceval(results: list) -> None:
    for result in tqdm(results):
        owner, repository = result.get("full_name", "").split("/")
        id = result.get("id")
        clone_repo(owner, repository, id)


if __name__ == "__main__":
    while True:
        input_message = "Type your query string (example: language:java+stars:>=10000&sort=star&order=desc) or hit ENTER to exit: "
        query = input(input_message)
        if query == "" or query is None:
            print("Exiting")
            break
        limit = input("(Optional) Add an integer number limit of repositories: ")
        limit = int(limit) if limit != "" else 0
        result = query_repos(query, limit)
        print("Saving the results...")
        add_repos_to_db(result)
        print("Results saved into database...")
        # print("Cloning the repos with Perceval...")
        # clone_with_perceval(result)
        # print("Finished cloning with perceval...")
