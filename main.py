from sys import exit
from typing import List

import history
from printer import print_search_prompt, print_search_results, print_select_result_prompt
from search import search
from structs import SearchResult, SearchResults
from utils import try_parse_int, open_system_default_browser


class Main:
    def __init__(self):
        SearchResults = []
        self.search_results = SearchResults
        self.search_result_history = list(SearchResults)

    def start(self):
        print_search_prompt()

        while True:
            command = self.prompt_command()
            self.handle_command(command)
            print_select_result_prompt()

    def prompt_command(self):
        command = input()
        print()
        return command

    def is_valid_search_result_idx(self, idx: int) -> bool:
        if self.search_results is None:
            return False
        if 1 <= idx <= len(self.search_results.results):
            return True
        return False

    def handle_command(self, command):
        if command == "q" or command == "-q" or command == "quit" or command == "exit":  # quit
            exit(0)
            return

        idx = try_parse_int(command)
        if idx is not None:
            if not self.is_valid_search_result_idx(idx):
                print("Invalid index")
                print()
                return

            self.open_search_result(idx)
            exit(0)
            return

        if command == "-r":  # repeat last query
            last_results = history.get_last_query_results()
            if last_results is None:
                print("There is no last results to show.")
                print()
            else:
                self.search_results = last_results
                self.print_search_results()
            return

        if command.startswith("-a "):  # append to last query
            last_search_query = history.get_last_search_query()
            search_query = last_search_query + command[len("-a"):]
            print("Fetching search results for: \"%s\"" % search_query)
            print()

            self.fetch_search_results(search_query)
            self.print_search_results()
            return

        if command == "-b":  # go back one search result
            if len(self.search_result_history) == 0:
                print("Can't go back")
                print()
                return

            self.search_results = self.search_result_history.pop()
            print("Showing search results for: \"%s\"" % self.search_results.query)
            print()
            self.print_search_results()
            history.write_last_query(self.search_results)
            return

        self.fetch_search_results(command)
        self.print_search_results()

    def fetch_search_results(self, search_query: str):
        self.search_result_history.append(self.search_results)
        self.search_results = search(search_query)
        history.write_last_query(self.search_results)

    def print_search_results(self):
        visited_urls = history.get_visited_urls()
        print_search_results(self.search_results, visited_urls)

    def open_search_result(self, idx: int):
        selected_result = self.search_results.results[idx - 1]
        selected_url = selected_result.url
        open_system_default_browser(selected_url)
        history.add_visited_url(selected_url)
        history.add_visited_result(history.get_timestamp(), self.search_results.query, selected_url)


main = Main()
main.start()
