# Habits

A small script to read from a user's Trello board containing things they'd like to get done in small spurts every day.

Each run will pick a random activity from the lists in `config.trello['todo_lists']` and text the user.

## Usage

Put 'er in a daily cron (probably to be run around the end of the workday):

`python -m habits`

## Motivation

I'm really bad at remembering to do things, and I also get bored of doing the same thing every day. So instead, I made this to choose something random for me to do each day. This is an experiment, and I have no idea if it'll work.

## Installation

    $ pip install -r requirements.txt

## License

[MIT](LICENSE)
