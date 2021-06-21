from github_api import make_request

SEARCH_PATH = "search/repositories"

if __name__ == "__main__":
    while True:
        input_message = "Type your query string (example: language:java+stars:>=10000&sort=star&order=desc) or hit ENTER to exit:"
        query = input(input_message)
        if query == "" or query is None:
            print("Exiting")
            break
        path = f"{SEARCH_PATH}?q={query}"
        print(make_request(path))
