import colorama
from colorama import Fore

from structs import SearchResult, SearchResults

colorama.init(autoreset=True)

G_LOGO = f"{Fore.LIGHTBLUE_EX}G{Fore.RED}o{Fore.YELLOW}o{Fore.LIGHTBLUE_EX}g{Fore.GREEN}l{Fore.RED}e{Fore.RESET}"


def print_search_results(results: SearchResults, visited_urls: set = set()):
    for i, v in enumerate(results.results):
        result: SearchResult = v

        title_color = Fore.LIGHTBLUE_EX if result.url not in visited_urls else Fore.RED
        print(f"{Fore.GREEN}{i + 1}) {title_color}{result.title}")

        print(f"{Fore.LIGHTBLACK_EX}{result.url}")

        if result.description is not None and len(result.description) > 0:
            print(result.description)
        print()

    if len(results.results) == 0:
        print("There is no results to show. Try another query.")
        print()


def print_search_prompt():
    print(f"{G_LOGO} Search: ", end="")


def print_select_result_prompt():
    print(f"Open a web result: {Fore.GREEN}(number) ", end="")
