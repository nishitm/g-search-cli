from typing import Optional, Dict
from os import system


def try_parse_int(string: str) -> Optional[int]:
    try:
        string = string.strip()
        number = int(string)
        return number
    except ValueError:
        return None


def open_system_default_browser(url: str):
    url = url.replace("&", "^&")
    system("open " + url)


def try_parse_config_file(filename: str) -> dict:
    try:
        with open(filename) as file:
            lines = file.readlines()
    except OSError:
        lines = []

    config_dict: Dict[str, str] = {}
    for line in lines:
        line = line.rstrip()

        if line.startswith("#") or len(line) == 0:
            continue

        key, value = line.split("=", 1)
        config_dict[key] = value

    return config_dict
