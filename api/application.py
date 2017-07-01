# coding=utf-8
"""
webhook for api.ai, semantic search project SS2017
"""

import json
import os
import sys
from datetime import datetime

from flask import Flask, request, __version__, render_template, jsonify


application = Flask(__name__, static_folder='web/static', template_folder='web/templates')
PORT = int(os.getenv('PORT', '8087'))


#### WEB ###
@application.route('/')
def index():
    return render_template('chat.html')

### End WEB ###

### API ###

@application.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    fake_request = json.dumps(req)

    response = retrieve_data(fake_request)

    r = make_response(response)
    r.headers['Content-Type'] = 'application/json'
    #return r

    return ('', 200)

### END API ###

### UTIL ###

def retrieve_data(req):
    tmp = {}

    res = generate_response(tmp)
    return res

def generate_response(speech):
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }

### END UTIL ###

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=int(PORT), threaded=True, debug=True)
