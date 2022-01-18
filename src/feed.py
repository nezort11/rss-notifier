import json
from json.decoder import JSONDecodeError
from pprint import pprint
from typing import Generator
from urllib.parse import unquote, urlencode

import feedparser
import requests
import toml

from job import JobEntry

UPWORK_FEED_URL = "https://www.upwork.com/ab/feed/jobs/rss"

c = toml.load("config.toml")


def construct_feed_url():
    params = urlencode(c["feed"])
    return f"{UPWORK_FEED_URL}?{params}"


def check_updates(feed: dict) -> Generator[dict, None, None]:
    with open("entries.json", "r+") as entries_file:
        # Entry ids (urls) are stored in decoded form
        try:
            entries = json.load(entries_file)
        except JSONDecodeError:
            entries = []

        for entry in feed["entries"]:
            url = unquote(entry["id"])
            if url not in entries:
                # Do action on update
                yield entry
                # print(url)
                entries.insert(0, url)

        entries_file.seek(0)
        json.dump(entries, entries_file, indent=2)
        entries_file.truncate()


def poll_feed():
    """Poll RSS feed and yield updates."""
    feed_url = construct_feed_url()
    try:
        response = requests.get(feed_url)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
    except Exception as e:
        # If anything bad happended while retrieving feed, reraise exception
        raise e

    yield from check_updates(feed)


if __name__ == "__main__":
    for update in poll_feed():
        print(JobEntry(update))
