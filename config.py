from typing import Dict

import utils


# You may override any of the following configs by creating a "config.env" file on this same folder.
# The file should follow the .env file pattern, that is, each line is a "KEY=VALUE" pair. Anything
# before the first equals symbol on a line is treated as the KEY and anything after the equals symbol
# (inclunding another equals symbol) is treated as a VALUE, until a new line. Trailing whitespace,
# empty lines and lines starting with "#" are all discarded.
config_dict = utils.try_parse_config_file("config.env")


# This is passed as an HTTP Header on requests to Google. The user agent needs to be Firefox because
# the result parsing relies on the presence of h3 html tags for the title of each result, which (I think)
# only happens when the User Agent is Firefox. (Certainly it doesn't happen in Chrome.)
USER_AGENT = config_dict.get("USER_AGENT",
                             "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0")

# This is passed as an HTTP Header on requests to Google. By default, Google tries to infer your preferred
# language through your IP Address. If you want to override that, you can pass your preferred languages
# through this header. The syntax follows this standard:
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language
ACCEPT_LANGUAGE = config_dict.get("ACCEPT_LANGUAGE", "")

# This is passed as an HTTP Header on requests to Google. You may want to access Google on your Firefox
# browser and get your unique user cookie to pass along with your requests here, so your preferences
# (such as language) apply to searches made here as well. You may want to use a cookie from a private
# Firefox session.
COOKIE = config_dict.get("COOKIE", "")

# On my screen, 8 results are just perfect, but you may want to customize the maximum amount of search
# results for your own preference. Note that the maximum possible is 10, since Google only shows at most
# 10 results on the first results page.
MAX_SEARCH_RESULTS = int(config_dict.get("MAX_SEARCH_RESULTS", "8"))

# Saving the visited URLs allows this tool to show the visited search results as red links. These URLs
# are only saved locally on your machine. If you don't want that, set it to "false".
SAVE_VISITED_URLS = config_dict.get("SAVE_VISITED_URLS", "true") == "true"

# Saving the last query and its search results allows you to redo the last query without fetching the
# results from Google. This is only saved locally on your machine. If you don't want that, set it to "false".
SAVE_LAST_QUERY = config_dict.get("SAVE_LAST_QUERY", "true") == "true"

# Save the visited search results, with timestamp, query and visited url, on a local text file. Each
# line of the text file is a JSON object. You may parse this file to draw insights about your own searches.
# If you don't want that, set it to "false".
SAVE_VISITED_RESULTS = config_dict.get("SAVE_VISITED_RESULTS", "true") == "true"
