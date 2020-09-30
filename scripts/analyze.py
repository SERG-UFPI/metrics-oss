TOPIC_SEARCH = {
    "C#": "csharp",
    "C++": "cpp",
}


def convert_word(word):
    keywords = [word.lower(), word.capitalize(), word.upper()]
    if word in TOPIC_SEARCH.keys():
        topic = TOPIC_SEARCH[word]
        keywords += [topic.lower(), topic.capitalize(), topic.upper()]
    return keywords


def check(repo, lang):
    awesome_word = "awesome"
    keywords_awesome = convert_word(awesome_word)
    keywords_lang = convert_word(lang)
    name = repo.get("name") if repo.get("name") else ""
    description = repo.get("description") if repo.get("description") else ""

    in_name_awesome = any(key in name for key in keywords_awesome)
    in_description_awesome = any(key in description for key in keywords_awesome)
    if not in_description_awesome and not in_description_awesome:
        return False

    in_name_lang = any(key in name for key in keywords_lang)
    in_description_lang = any(key in description for key in keywords_lang)
    return in_name_lang or in_description_lang


def reports(results):
    print("*" * 50)
    print(f"Language: {results['lang']}")
    print(f"Number of repos before triage: {results['before_triage']}")
    print(f"Number of repos after triage: {results['after_triage']}")
    print(f"Total of stars: {results['stars']}")
    print(f"Total of issues: {results['issues']}")
    print(f"Total of forks: {results['forks']}")
    print(f"Total of forks: {results['watchers']}")
    print("*" * 50)


def analyze(lang, repos):
    results = {
        "lang": lang,
        "before_triage": len(repos),
        "stars": 0,
        "issues": 0,
        "forks": 0,
        "watchers": 0,
    }

    repos_dicts = []

    for repo in repos:
        if check(repo, lang):
            r = {
                "full_name": repo["full_name"],
                "stars": repo["stargazers_count"],
                "issues": repo["open_issues_count"],
                "forks": repo["forks_count"],
                "watchers": repo["watchers_count"],
            }
            results["stars"] += repo["stargazers_count"]
            results["issues"] += repo["open_issues_count"]
            results["forks"] += repo["forks_count"]
            results["watchers"] += repo["watchers_count"]

            repos_dicts.append(r)

    results.update({"after_triage": len(repos_dicts)})

    reports(results)
