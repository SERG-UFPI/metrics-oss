from analyze import analyze
from files import read_from_file, save_file
from github_api import make_request

PATH = "search/repositories?q=awesome+"
LANGUAGES = [
    "Javascript",
    "Python",
    "Java",
    "C#",
    "PHP",
    "Typescript",
    "C++",
    "C",
    "Go",
    "Kotlin",
    "Ruby",
    "Assembly",
    "Swift",
    "R",
    "Rust",
    "Objective-C",
    "Dart",
    "Scala",
    "Perl",
    "Haskell",
    "Julia",
]

TOPIC_SEARCH = {"C#": "csharp", "C++": "cpp", "C": "c", "R": "r"}

PER_PAGE = 100
LIMIT_OF_SEARCH = 10


def get_total_count(language):
    data = make_request(language)
    return data["total_count"]


def get_number_of_pages(language):
    total_count = get_total_count(language)
    pages = (total_count // PER_PAGE) + 1 if total_count >= 100 else 2
    return pages if pages <= LIMIT_OF_SEARCH else LIMIT_OF_SEARCH + 1


def add_topic(url, language):
    if TOPIC_SEARCH.get(language):
        topic = TOPIC_SEARCH.get(language)
        url = url + f"+topic:{topic}"
    return url


def get_repositories(language):
    path_with_query = PATH + language
    path_with_query = add_topic(path_with_query, language)
    pages = get_number_of_pages(path_with_query)
    lang_data = []
    for page in range(1, pages):
        url = f"{path_with_query}&per_page={PER_PAGE}&page={page}"
        data = make_request(url)
        lang_data += data.get("items", [])
    return lang_data


if __name__ == "__main__":
    for lang in LANGUAGES:
        filename = f"langs-json/{lang}.json"
        data = read_from_file(filename)
        if not data:
            data = get_repositories(lang)
            save_file(data, filename)
        analyze(lang, data)
