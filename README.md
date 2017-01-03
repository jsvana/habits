# Habits

A small script to read from a user's Trello board containing things they'd like to get done in small spurts every day.

Each run will pick a random activity from the lists in `config.trello['todo_lists']` and text the user.

## Usage

Put 'er in a daily cron (probably to be run around the end of the workday):

`python -m habits`

## Motivation

I'm really bad at remembering to do things, and I also get bored of doing the same thing every day. So instead, I made this to choose something random for me to do each day. This is an experiment, and I have no idea if it'll work.

## Installation

```shell
# Install dependencies
$ pip install -r requirements.txt

# Setup your config (Twilio/Trello keys, etc)
$ cp habits/config.py.example habits/config.py
$ $EDITOR habits/config.py
```

## License

[MIT](LICENSE)
