"""
Webserver for Twilio callbacks
"""
from flask import (
    Flask,
    request,
)


app = Flask(__name__)


@app.route('/message', methods=['POST'])
def message():
    print(request.values)
    return 'Received'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
