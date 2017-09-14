from message import Message

class MessageParser:
    def parse_message_event(self, req):

        intent = req.get("result").get("metadata").get("intentName")

        if intent == "berlina.topic.only":
            topic = req.get("result").get("parameters").get("new_topics")

            message = Message(intent, topic)

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
        else:
            # fallback
            message = Message()

        return message
