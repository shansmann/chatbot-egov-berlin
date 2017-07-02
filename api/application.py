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
PORT = int(os.getenv('PORT', '8085'))
firebase = firebase.FirebaseApplication('https://berlinabot.firebaseio.com', None)

#### WEB ###
@application.route('/')
def index():
    return render_template('index.html')

### End WEB ###

### API ###

@application.route('/webhook', methods=['POST'])
def webhook():
    print(type(request))

    req = request.get_json(silent=True, force=True)

    print(type(req))

    response = retrieve_data(req)
    #print(response)

    #response = generate_text_response('req recieved.')

    res = make_response(json.dumps(response))
    res.headers['Content-Type'] = 'application/json'

    return res

    #return ('', 200)

### END API ###

### UTIL ###

def retrieve_data(req):

    result = req['result']
    intent = result['metadata']['intentName']

    if intent == "topic.objective":
        # show services
        topic = result['parameters']['topic']
        objective = result['parameters']['objective']

        # retrieve data
        url = '/tree/{t}/{o}'.format(t = topic, o = objective)
        result = firebase.get(url, None)

        # check result for multiple services
        try:
            if len(result) > 1:
                names = [x["name"] for x in result]
                speech = "; ".join(names)
                res = generate_text_response(speech)
            else:
                speech = result[0]["name"]
                res = generate_text_response(speech)
        except:
            res = generate_text_response("error accessing topic" + topic + "; objective: " + objective)

        # generate response
        #res = generate_text_response("topic: " + topic + ";objective: " + objective)
        return res

    elif intent == "topic.only":
        # find objective
        topic = result['parameters']['topic']

        if not topic:
            res = generate_text_response("no topic present.")
            return res

        # retrieve data
        url = '/tree/{t}'.format(t = topic)
        result = firebase.get(url, None)

        # access result
        try:
            objectives = list(result.keys())
            speech = "; ".join(objectives)
            res = generate_text_response(speech)
        except:
            res = generate_text_response("error accessing topic " + topic)

        return res

    else:
        # neither topic nor objective recognized
        res = generate_text_response('error in request.')
        return res


    """
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

    if result:
        if len(result) > 1:
            logging.info('multiple services/objectives found.')
            # generate list response

            if type(result) == type([]):
                # multiple services
                names = [x["name"] for x in result]
                speech = "; ".join(names)
            else:
                # multiple objectives
                names = list(result.keys())
                speech = "; ".join(names)

            res = generate_text_response(speech)
        else:
            logging.info('service found.')
            service = result[0]
            speech = "Sie interessieren sich für " + service['name']
            res = generate_text_response(speech)
    else:
        res = generate_text_response('nothing found in database.')

    return res
    """

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
