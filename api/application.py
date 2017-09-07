# coding=utf-8
"""
webhook for api.ai, semantic search project SS2017
"""

import json
import os
import sys

import request_handling

from datetime import datetime

from flask import Flask, request, __version__, render_template, jsonify, make_response

import logging

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

    response = find_lvl(req)

    res = make_response(json.dumps(response))
    res.headers["Content-Type"] = "application/json"

    return res

### END API ###

### UTIL ###

def find_lvl(req):
    """
    find relevant lvl of tree
    """

    result = req["result"]
    intent = result["metadata"]["intentName"]

    if intent == "berlina.topic.only":
        res = request_handling.topic_only(result)
    elif intent == "berlina.objective.only":
        res = request_handling.objective_only(result)
    elif intent == "berlina.topic.objective":
        res = request_handling.topic_objective(result)
    elif intent == "berlina.service.selection":
        res = request_handling.select_detail(result)
    elif intent == "berlina.detail.selection":
        res = request_handling.return_detail(result)
    else:
        res = request_handling.fallback(result)

    return res

### END UTIL ###

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(PORT), threaded=True, debug=True,
                                                            use_reloader=False)
