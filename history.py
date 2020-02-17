import json
from datetime import datetime
from typing import Optional, Set

import config
from structs import SearchResult, SearchResults


def get_timestamp() -> str:
    return datetime.utcnow().isoformat()


def get_visited_urls() -> set:
    history_urls: Set[str] = set()

    if not config.SAVE_VISITED_URLS:
        return history_urls

    try:
        with open("visited_urls.txt") as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip()
                history_urls.add(line)
        return history_urls
    except OSError:
        return set()


def add_visited_url(url: str):
    if not config.SAVE_VISITED_URLS:
        return

    with open("visited_urls.txt", "a") as file:
        file.write(url)
        file.write("\n")


def write_last_query(search_results: SearchResults):
    if not config.SAVE_LAST_QUERY:
        return

    try:
        with open("last_search.txt", "w") as file:
            root = search_results._asdict()
            root["results"] = [r._asdict() for r in search_results.results]
            json.dump(root, file, indent=2)
    except OSError:
        pass


def add_visited_result(timestamp: str, search_query: str, visited_url: str):
    if not config.SAVE_VISITED_RESULTS:
        return

    with open("history.txt", "a") as file:
        entry = {
            "timestamp": timestamp,
            "search_query": search_query,
            "visited_url": visited_url,
        }
        file.write(json.dumps(entry))
        file.write("\n")


def get_last_search_query() -> str:
    if not config.SAVE_LAST_QUERY:
        return ""

    try:
        with open("last_search.txt") as file:
            root = json.load(file)
        return root["query"]
    except OSError:
        return ""


def get_last_query_results() -> Optional[SearchResults]:
    if not config.SAVE_LAST_QUERY:
        return None

    try:
        with open("last_search.txt") as file:
            root = json.load(file)

        return SearchResults(
            query=root["query"],
            url=root["url"],
            results=[SearchResult(**item) for item in root["results"]],
        )
    except OSError:
        return None
