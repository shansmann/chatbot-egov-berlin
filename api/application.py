# coding=utf-8
"""
webhook for api.ai, semantic search project SS2017
"""
from pprint import pprint
import json
import os
import sys
from datetime import datetime
import logging

from flask import Flask, request, __version__, render_template, jsonify, make_response

from message_parser import MessageParser
from message import Message


logging.basicConfig(level=logging.INFO)
application = Flask(__name__, static_folder="web/static", template_folder="web/templates")
PORT = int(os.getenv("PORT", "8085"))

#### WEB ###
@application.route("/")
def index():
    return render_template("index.html")

### End WEB ###

### API ###

@application.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("received message: {}".format(req))

    msg = MessageParser().parse_message_event(req)
    msg.set_state()
    print("state set to: {}".format(msg.get_state()))

    res = msg.handle_message()
    print("returning msg: {}".format(res))
    
    response = make_response(json.dumps(res))
    response.headers["Content-Type"] = "application/json"
    return response

### END API ###

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(PORT), threaded=True, debug=True,
                                                            use_reloader=False)
