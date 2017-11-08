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

from sqlalchemy import Column, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, request, __version__, render_template, jsonify, make_response

from db import Base, Topic, Detail
from message_parser import MessageParser
from message import Message
import config



logging.basicConfig(level=logging.INFO)
application = Flask(__name__, static_folder="web/static", template_folder="web/templates")
PORT = int(os.getenv("PORT", "8668"))

#### WEB ###
@application.route("/")
def index():
    return render_template("app.html")

### End WEB ###

### API ###

@application.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("received message: {}".format(req))

    # parse message
    msg = MessageParser().parse_message_event(req)
    # set state dependent on parameters
    msg.set_state()
    print("state set to: {}".format(msg.get_state()))
    # handle message dependent on state
    res = msg.handle_message()
    print("returning msg: {}".format(res))

    response = make_response(json.dumps(res))
    response.headers["Content-Type"] = "application/json"
    return response

# return topic counters from db
@application.route('/topic', methods=['GET'])
def get_topic_results():
    engine = create_engine(config.DATABASE_PATH)
    Base.metadata.bind = engine
    session = scoped_session(sessionmaker(bind=engine))
    all_topics = session.query(Topic.topic, func.count(Topic.topic)).group_by(Topic.topic).all()
    session.close()
    print("sending data: ", jsonify(all_topics).data)
    return jsonify(all_topics)

# return detail counters from db
@application.route('/detail', methods=['GET'])
def get_detail_results():
    engine = create_engine(config.DATABASE_PATH)
    Base.metadata.bind = engine
    session = scoped_session(sessionmaker(bind=engine))
    all_details = session.query(Detail.detail, func.count(Detail.detail)).group_by(Detail.detail).all()
    session.close()
    print("sending data: ", jsonify(all_details).data)
    return jsonify(all_details)

### END API ###

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(PORT), threaded=True, debug=True,
                                                            use_reloader=False)
