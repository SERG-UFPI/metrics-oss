import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from settings.settings import ELASTIC_URL

from db import get_cloned_repos
from files import save_file
from tqdm import tqdm


FILENAME = f"{os.getcwd()}/scripts/truck-factor.json"

files_modified_by_author = {}
author_modified_by_files = {}

es = Elasticsearch(ELASTIC_URL)

def process_response(response):

    author = response['_source']['data']['Author']
    if author not in files_modified_by_author.keys():
        files_modified_by_author[author] = set()

    for file in response['_source']['data']['files']:
        file_name = file['file']

        if file_name not in author_modified_by_files.keys():
            author_modified_by_files[file_name] = set()

        author_modified_by_files[file_name].add(author)
        files_modified_by_author[author].add(file_name)


def get_number_of_commits_by_author(url: str):
    files_modified_by_author.clear()
    author_modified_by_files.clear()


    query = {"query": {"match_phrase": {"origin": {"query": url}}}}

    for hit in scan(es, index="git_raw", query=query):
        process_response(hit)


def get_result(url: str) -> dict:
    get_number_of_commits_by_author(url)

    sum = len(author_modified_by_files)

    cnt_author = []

    for author in files_modified_by_author:
        cnt_author.append((author, len(files_modified_by_author[author])))

    cnt_author.sort(key=lambda tup: tup[1], reverse=True)

    curr_sum = 0
    truck_factor = 0

    for (author, _) in cnt_author:
        truck_factor += 1
        
        for file in files_modified_by_author[author]:
            author_modified_by_files[file].remove(author)

            if (len(author_modified_by_files[file]) == 0):
                curr_sum += 1

            if (curr_sum > sum / 2.0):
                return truck_factor
        
    return 0


def generate_metric(repos: list) -> None:
    results = {}
    for repo in tqdm(repos):
        results[repo.full_name] = get_result(repo.html_url)
    save_file(results, FILENAME)


if __name__ == "__main__":
    repos = get_cloned_repos()
    generate_metric(repos)
