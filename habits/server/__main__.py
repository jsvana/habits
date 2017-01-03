"""
Webserver for Twilio callbacks
"""

print(__package__)

from .. import config


from flask import (
    Flask,

    jsonify,
    request,
)


class InvalidUsageError(Exception):

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


app = Flask(__name__)


@app.errorhandler(InvalidUsageError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/message', methods=['POST'])
def message():
    sender = request.values.get('From')
    receiver = request.values.get('To')
    body = request.values.get('Body')
    if any([v is None for v in [sender, receiver, body]]):
        raise InvalidUsageError(
            'Malformed request',
            status_code=400,
        )

    sender_ok = sender == config.phone_numbers['user']
    receiver_ok = receiver == config.phone_numbers['twilio']
    if not sender_ok or not receiver_ok:
        raise InvalidUsageError(
            'Endpoint not accessible',
            status_code=403,
        )

    print(body)

    return 'Received'


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0')
