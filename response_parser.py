from typing import List, Optional, NamedTuple
import re
import html

from structs import SearchResult, SearchResults


RESULT_START_MARKER = '<div class="rc">'
LINK_START_MARKER = '<a'
LINK_END_MARKER = '>'
TITLE_START_MARKER = '<h3'
TITLE_END_MARKER = '</h3>'
DESCRIPTION_START_MARKER = '<span class="st">'
DESCRIPTION_END_MARKER = '</span><'
TAG_START = "<"
TAG_END = ">"
HREF_START = 'href="'
HREF_END = '"'


def parse(response_html: str) -> List[SearchResult]:
    matcher = Matcher(response_html)
    results: List[SearchResult] = []
    while matcher.next(RESULT_START_MARKER):
        matcher.next(LINK_START_MARKER)
        matcher.next(HREF_START)
        url = matcher.match_until(HREF_END)
        matcher.next(LINK_END_MARKER)

        matcher.next(TITLE_START_MARKER)
        matcher.next(TAG_END)
        title = matcher.match_until(TITLE_END_MARKER)

        matcher.next(DESCRIPTION_START_MARKER)
        description = matcher.match_until(DESCRIPTION_END_MARKER)
        description = strip_html(description)
        description = html.unescape(description)

        results.append(SearchResult(title, url, description))
    return results


class Matcher:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def next(self, pattern: str) -> bool:
        try:
            pattern_index = self.text.index(pattern, self.pos)
            self.pos = pattern_index + len(pattern)
            return True
        except ValueError:
            return False

    def match_until(self, pattern: str) -> str:
        pattern_index = self.text.index(pattern, self.pos)
        prev_pos = self.pos
        self.pos = pattern_index
        return self.text[prev_pos:pattern_index]


def strip_html(text: str) -> str:
    return re.sub(r"<[^<]+?>", "", text)
