# Habits

`Habits` is a tool to remind you to get random things done in small parts over many days.

When setup in cron, the script will text you to do something from your lists. Then, after you've done something for that task, simply text the number back and it will comment on your Trello card with what you've done. That way, you can track what you've been doing over time.

`Habits` has two parts:

- A small script to read from a user's Trello board containing things they'd like to get done in small spurts every day.

- A Flask server for Twilio callbacks

Each run of the script will pick a random activity from the lists in `config.trello['todo_lists']` and text the user.

## Usage

### Script

Put 'er in a daily cron (probably to be run around the end of the workday):

`python -m habits.cron`

### Server

Add your URL into the Twilio SMS callbacks (`https://your-cool-domain.fake/messages`) and then run:

`python -m habits.server`

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
