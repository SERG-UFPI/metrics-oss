from files import save_file, read_from_file
from github_api import make_request
from tqdm import tqdm

PATH = 'search/repositories?q=awesome+'
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
PER_PAGE = 100

def get_total_count(language):
    path_with_query = PATH + language
    
    data = make_request(path_with_query)
    return data['total_count']

def get_number_of_pages(language):
    total_count = get_total_count(language)
    pages = (total_count // PER_PAGE) + 1
    return pages

def get_repositories(language):
    pages = get_number_of_pages(lang)
    lang_data = []
    for page in (1, pages):
        path_with_query = PATH + language
        url = f"{path_with_query}&per_page={PER_PAGE}&page={page}"
        data = make_request(url)
        if not data.get('items'):
            pass
        else:
            lang_data += data.get('items')
    return lang_data

if __name__ == "__main__":
    for lang in tqdm(LANGUAGES):
        print(lang)
        filename = f"langs-json/{lang}.json"
        saved_data = read_from_file(filename)
        if not saved_data:
            lang_data = get_repositories(lang)
            save_file(lang_data, filename)
        else:
            pass
