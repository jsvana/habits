"""
Quick tool to pull from a Trello board and text the user a reminder
every day. Meant to be run in cron.
"""
import argparse
import datetime
import random
import sys


from twilio.rest import TwilioRestClient
from .. import (
    config,
    db,
    trello,
)


def send_message(client, text):
    """
    Sends a text via the Twilio API
    """
    message = client.messages.create(
        body=text,
        to=config.phone_numbers['user'],
        from_=config.phone_numbers['twilio'],
    )
    return message.sid


def init_db():
    db.Activity.create_table()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--no-text',
        action='store_true',
        help='Do not send a text message with the daily activity',
    )
    return parser.parse_args()


def today_activity():
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    return db.Activity.get_one(create_date=today)


def main():
    args = parse_args()

    init_db()

    board = trello.Board.get(config.trello['board_id'])
    possible_activities = []
    for list_name in config.trello['todo_lists']:
        lst = board.list(list_name)
        for _, card in lst.cards.items():
            possible_activities.append(card.name)

    activity = random.choice(possible_activities)
    message = "Today's activity: " + activity

    if args.no_text:
        print(message)
        return True

    client = TwilioRestClient(
        config.twilio['account_sid'],
        config.twilio['auth_token'],
    )
    send_message(client, message)

    return True



if __name__ == "__main__":
    sys.exit(0 if main() else 1)
