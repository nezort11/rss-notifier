# RSS updates notifier

RSS updates notifier program and bot that send information about updates to RSS source.

I will use it primarily for getting Upwork job updates:

- check for updates every minute
- send short information about new job (price, title)
- information persistance (file/json serialization)
- periodic execution (timer, scheduler)
- bot update subscribers

Display most important information:

- title
- badged
- tags
- level

RSS configuration:

- query string
- max price
- level
- update period

## Roadmap

These are the tasks that need to be solved when building such program:

- [x] Construct RSS source function

- [x] Get the RSS file

- [x] Parse RSS/XML file to determine new entries

- [x] Check for new entries/jobs

- [x] Implement bot subscribers list

- [x] Broadcast updates to subscribers

- [x] Convenient configuration interface via bot

- [ ] Add Sentry error logging

## Tags

rss, feed, notifier, updates, news, parser, listener, scraper, upwork, jobs, poller, broadcast.
