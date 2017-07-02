# coding=utf-8
"""
webhook for api.ai, semantic search project SS2017
"""

import json
import os
import sys

from firebase import firebase

from datetime import datetime

from flask import Flask, request, __version__, render_template, jsonify, make_response

import logging

logging.basicConfig(level=logging.INFO)
application = Flask(__name__, static_folder='web/static', template_folder='web/templates')
PORT = int(os.getenv('PORT', '8087'))
firebase = firebase.FirebaseApplication('https://berlinabot.firebaseio.com', None)

#### WEB ###
@application.route('/')
def index():
    return render_template('index.html')

### End WEB ###

### API ###

@application.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    response = retrieve_data(req)

    res = make_response(json.dumps(response),
                             200,
                             {'Content-Type': 'application/json'})
    return res

    #return ('', 200)

### END API ###

### UTIL ###

def retrieve_data(req):

    result = req['result']

    topic = result['parameters']['topic']
    objective = result['parameters']['objective']
    res = ''

    if not topic:
        logging.info('topic not present')
        speech = "Ich hab ihre Anfrage leider nicht verstanden."
        res = generate_text_response(speech)
        return res

    if objective:
        logging.info('objective present')

        url = '/tree/{t}/{o}'.format(t = topic, o = objective)
        result = firebase.get(url, None)
    else:
        logging.info('objective not present')

        url = '/tree/{t}'.format(t = topic)
        result = firebase.get(url, None)


    if len(result) > 1:
        logging.info('multiple services found.')
        # generate list response
        speech = ", ".join(result)
        res = generate_text_response(speech)
    else:
        logging.info('service found.')
        service = result[0]
        speech = "Sie interessieren sich für " + service['name']
        res = generate_text_response(speech)


    return res

def generate_text_response(speech, data={}):
    return {
        "speech": speech,
        "displayText": speech,
        "data": data,
        "contextOut": [],
        "source": "api"
    }

### END UTIL ###

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=int(PORT), threaded=True, debug=True,
                                                            use_reloader=False)
