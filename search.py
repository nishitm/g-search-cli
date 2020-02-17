from urllib.request import Request, urlopen
from urllib.parse import quote_plus

import config
from response_parser import parse
from structs import SearchResult, SearchResults


SEARCH_QUERY_URL_FORMAT = "https://www.google.com/search?q=%s"


def search(query: str, max_results: int = config.MAX_SEARCH_RESULTS) -> SearchResults:
    encoded_query = quote_plus(query)
    query_url = SEARCH_QUERY_URL_FORMAT % (encoded_query)
    headers = {
        "User-Agent": config.USER_AGENT,
        "Accept-Language": config.ACCEPT_LANGUAGE,
        "Cookie": config.COOKIE,
    }
    request = Request(query_url, headers=headers)
    response = urlopen(request)
    response_bytes = response.read()
    response_html = response_bytes.decode("utf8")

    results = parse(response_html)[:max_results]

    return SearchResults(query=query, url=query_url, results=results)
