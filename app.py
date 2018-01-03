import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


import requests
from bs4 import BeautifulSoup
from fsm import get_title

API_TOKEN = '514314352:AAEN0Wkkl47XUjjrDpj1w7N17G7Bf2ZnT0A'
WEBHOOK_URL = 'https://f3e440df.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'initial',
        'start',
        'user',
        'beauty',
        'photo',
        'one',
        'chat',
        'bath'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'initial',
            'dest': 'start',
            'conditions': 'is_going_to_start'
        },
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'beauty',
            'conditions': 'is_going_to_beauty'
        },
        {
            'trigger': 'advance',
            'source': 'beauty',
            'dest': 'photo',
            'conditions': 'is_going_to_photo'
        },
        {
            'trigger': 'advance',
            'source': 'beauty',
            'dest': 'one',
            'conditions': 'is_going_to_one'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'chat',
            'conditions': 'is_going_to_chat'
        },
        {
            'trigger': 'advance',
            'source': 'chat',
            'dest': 'bath',
            'conditions': 'is_going_to_bath'
        },
        {
            'trigger': 'go_back',
            'source': [
                'photo',
                'one',
                'bath'
            ],
            'dest': 'user'
        }
    ],
    initial='initial',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
