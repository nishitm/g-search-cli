from typing import NamedTuple, List


class SearchResult(NamedTuple):
    title: str
    url: str
    description: str


class SearchResults(NamedTuple):
    query: str
    url: str
    results: List[SearchResult]
