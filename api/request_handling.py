import util
import response
import random

import config
import detail_parser

def topic_only(result):
    # find objectives
    topic = result["parameters"]["new_topics"]

    data = util.get_data("/tree/" + topic)
    if not data:
        return response.generate_text("could not find data at " + topic)

    objective_names = list(data.keys())

    # only 1 objective present
    if len(objective_names) == 1:
        # create objective recognized context with objective
        print("only 1 ojective")

    speech = "Es geht also um {}? Kannst du mir hier noch schnell weiterhelfen?".format(topic)

    res = response.generate_quick_replies(speech, objective_names)
    return res

def objective_only(result):
    # find services
    relevant_context = next(item for item in result["contexts"] if item["name"] == "topic-recognized")
    topic = relevant_context["parameters"]["new_topics"]
    objective = result["parameters"]["obj_wo_syn"]

    data = util.get_data("/tree/" + topic + "/" + objective)
    if not data:
        return response.generate_text("could not find data at " + topic + " " + objective)

    service_names = [x["name"] for x in data]
    descriptions = [x["description"] for x in data]

    # only 1 service present
    if len(service_names) < 2:
        print("only one service found.")
        description = util.remove_html(descriptions[0])
        img = random.choice(config.LANDSCAPE_IMAGES)
        card = {
            "title": service_names[0],
            "subtitle": description.split('\n', 1)[0],
            "image_url": img
        }

        res = response.generate_card("Diese Dienstleistung haben wir im Angebot:", [card])

        return res
    else:
        speech = "Gleich hast du es geschafft! Mit diesen Dingen kann ich dir behilflich sein:"
        items = []
        imgs = random.sample(config.IMAGES, len(service_names))
        for i, service in enumerate(service_names):
            description = util.remove_html(descriptions[i])
            test_item = {
                "title": service,
                "subtitle": description.split('\n', 1)[0],
                "image_url": imgs[i]
            }
            items.append(test_item)

        res = response.generate_list('test', items)

        return res

def topic_objective(result):
    # find services
    topic = result["parameters"]["new_topics"]
    objective = result["parameters"]["obj_wo_syn"]

    data = util.get_data("/tree/" + topic + "/" + objective)
    if not data:
        return response.generate_text("could not find data at " + topic + " " + objective)

    service_names = [x["name"] for x in data]

    # only 1 service present
    if len(service_names) == 1:
        print("only 1 service found.")

    speech = "Diese Dienstleistungen bieten wir an:"

    cards = []
    imgs = random.sample(config.IMAGES, len(service_names))

    for i, service in enumerate(service_names):
        description = util.remove_html(descriptions[i])
        test_card = {
            "title": service,
            "subtitle": description.split('\n', 1)[0],
            "image_url": imgs[i]
        }
        cards.append(test_card)

    res = response.generate_list('test', cards)

    return res

def select_detail(result):
    relevant_service_context = next(item for item in result["contexts"] if item["name"] == "service-recognized")
    service = relevant_service_context["parameters"]["service"]
    text = 'Sie möchten Informationen über: "{}". Was interessiert sie genau?'.format(service)
    return response.generate_quick_replies(text, config.KEYS)

def show_detail(result):
    # find service values
    relevant_topic_context = next(item for item in result["contexts"] if item["name"] == "topic-recognized")
    relevant_objective_context = next(item for item in result["contexts"] if item["name"] == "objective-recognized")
    relevant_service_context = next(item for item in result["contexts"] if item["name"] == "service-recognized")
    topic = relevant_topic_context["parameters"]["new_topics"]
    objective = relevant_objective_context["parameters"]["obj_wo_syn"]
    service = relevant_service_context["parameters"]["service"]
    key = result["parameters"]["detail"]

    data = util.get_data("/tree/" + topic + "/" + objective)
    if not data:
        return response.generate_text("could not find data at " + topic + " " + objective + " " + key)
    relevant_service = next(tmp for tmp in data if tmp["name"] == service)

    # key-dependent parsing
    if key == 'meta':
        speech = detail_parser.parse_link(relevant_service[key])
    elif key == 'appointment':
        speech = detail_parser.parse_appointment(relevant_service[key])
    elif key in ['requirements', 'prerequisites']:
        speech = detail_parser.parse_requirements_or_prerequisites(relevant_service[key])
    elif key == 'fees':
        speech = util.remove_html(relevant_service[key], True)
    elif key == 'onlineprocessing':
        speech = detail_parser.parse_onlineprocessing(relevant_service[key])
    elif key == 'Zurück':
        res = response.generate_text("Guten Tag! Ich bin der Chatbot der Stadt Berlin, wie kann ich dir behilflich sein?")
        return res
    else:
        speech = util.remove_html(relevant_service[key], False)

    res = response.generate_quick_replies(speech, config.KEYS)
    return res

def fallback(result):
    return response.generate_text('Intent {} not found.'.format(result))
