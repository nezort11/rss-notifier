# RSS updates notifier

## Getting started using

First clone the repo onto your server:

```sh
git clone https://github.com/Egor4ik325/rss-notifier
cd rss-notifier
```

Create and edit `config.toml` in `src/` folder (based on `config.toml.example`).
Customize non-secret setting such as query and update check interval.

Also `src/entries.json` file must exists (can be empty).

Upwork: To get `securityToken`, `userUid` and `orgUid` go the Upwork, search for any jobs, look for RSS link,
get these settings from RSS link query params.

Telegram bot: Go to @BotFather and create new bot, paste token under `[bot].token` in `config.toml`.

Sentry: To get information when something goes wrong with the notifier, go to https://sentry.io and create a new project, paste key inside config file under `[sentry].key`.

After all of that build an Docker image and run a container:

```sh
# 'docker-compose' for V1 / 'docker compose' for V2
docker compose build
docker compose up -d
```

## Desc

RSS updates notifier program and bot that send information about updates to RSS source.

I will use it primarily for getting Upwork job updates:

- check for updates every minute
- send short information about new job (price, title)
- information persistance (file/json serialization)
- periodic execution (timer, scheduler)
- bot update subscribers

Display most important information:

- title
- budget
- category
- skills

## Roadmap

These are the tasks that need to be solved when building such program:

- [x] Construct RSS source function

- [x] Get the RSS file

- [x] Parse RSS/XML file to determine new entries

- [x] Check for new entries/jobs

- [x] Implement bot subscribers list

- [x] Broadcast updates to subscribers

- [x] Convenient configuration interface via bot

- [x] Add Sentry error logging

## Tags

rss, feed, notifier, updates, news, parser, listener, scraper, upwork, jobs, poller, broadcast, jobs.
