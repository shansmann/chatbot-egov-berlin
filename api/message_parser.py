"""
message parser, creates message out of request
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime

import config
from message import Message
from db import Base, Topic, Detail

class MessageParser:
    def parse_message_event(self, req):
        # get intent
        intent = req.get("result").get("metadata").get("intentName")

        if intent == "berlina.topic.only":
            topic = req.get("result").get("parameters").get("new_topics")

            message = Message(intent, topic)

            # save topic to db
            engine = create_engine(config.DATABASE_PATH)
            Base.metadata.bind = engine
            session = scoped_session(sessionmaker(bind=engine))
            new_topic = Topic(ts=datetime.utcnow(), topic = topic)
            session.add(new_topic)
            session.commit()
            session.close()

        elif intent == "berlina.objective.only":
            relevant_context = next(item for item in req.get("result").get("contexts") if item["name"] == "topic-recognized")
            topic = relevant_context.get("parameters").get("new_topics")
            objective = req.get("result").get("parameters").get("obj_wo_syn")

            message = Message(intent, topic, objective)

        elif intent == "berlina.service.selection":
            relevant_topic_context = next(item for item in req.get("result").get("contexts") if item["name"] == "topic-recognized")
            relevant_objective_context = next(item for item in req.get("result").get("contexts") if item["name"] == "objective-recognized")
            relevant_service_context = next(item for item in req.get("result").get("contexts") if item["name"] == "service-recognized")

            topic = relevant_topic_context["parameters"]["new_topics"]
            objective = relevant_objective_context["parameters"]["obj_wo_syn"]
            service = relevant_service_context["parameters"]["service"]

            message = Message(intent, topic, objective, service)

        elif intent == "berlina.detail.selection":
            relevant_topic_context = next(item for item in req.get("result").get("contexts") if item["name"] == "topic-recognized")
            relevant_objective_context = next(item for item in req.get("result").get("contexts") if item["name"] == "objective-recognized")
            relevant_service_context = next(item for item in req.get("result").get("contexts") if item["name"] == "service-recognized")

            topic = relevant_topic_context["parameters"]["new_topics"]
            objective = relevant_objective_context["parameters"]["obj_wo_syn"]
            service = relevant_service_context["parameters"]["service"]
            detail = req.get("result").get("parameters").get("detail")

            message = Message(intent, topic, objective, service, detail)

            engine = create_engine(config.DATABASE_PATH)
            Base.metadata.bind = engine
            session = scoped_session(sessionmaker(bind=engine))
            new_detail = Detail(ts=datetime.utcnow(), detail = detail)
            session.add(new_detail)
            session.commit()
            session.close()
        else:
            # fallback
            message = Message()

        return message
