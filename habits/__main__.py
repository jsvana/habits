"""
Quick tool to pull from a Trello board and text the user a reminder
every day. Meant to be run in cron.
"""
import random
import sys


from twilio.rest import TwilioRestClient
from . import (
    config,
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


def main():
    board = trello.Board.get(config.trello['board_id'])
    possible_activities = []
    for list_name in config.trello['todo_lists']:
        lst = board.list(list_name)
        for _, card in lst.cards.items():
            possible_activities.append(card.name)

    activity = random.choice(possible_activities)

    client = TwilioRestClient(
        config.twilio['account_sid'],
        config.twilio['auth_token'],
    )
    send_message(
        client,
        "Today's activity: " + activity,
    )

    return True



if __name__ == "__main__":
    sys.exit(0 if main() else 1)
