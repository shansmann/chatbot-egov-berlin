import random

import config
import util
import response
import strs
import detail_parser

def show_objective_selection(message):
    data = util.get_data("/tree/" + message.topic)
    if not data:
        res = response.generate_text("could not find data at {}".format(message.topic))
        return response.send_message(res)

    objective_names = list(data.keys())

    res = response.generate_quick_replies(strs.SHOW_OBJECTIVES.format(message.topic),
                                          objective_names)
    return response.send_message([res])

def show_service_selection(message):
    data = util.get_data("/tree/" + message.topic + "/" + message.objective)
    if not data:
        res = response.generate_text("could not find data at {} {}".format(message.topic,
                                                               message.objective))
        return response.send_message(res)

    service_names = [x["name"] for x in data]
    descriptions = [x["description"] for x in data]

    # only 1 service present
    if len(service_names) < 2:
        description = util.remove_html(descriptions[0])
        img = random.choice(config.LANDSCAPE_IMAGES)
        card = {
            "title": service_names[0],
            "subtitle": description.split('\n', 1)[0],
            "image_url": img
        }
        res = response.generate_card("Diese Dienstleistung haben wir im Angebot:", [card])
        return response.send_message([res])
    elif len(service_names) < 5:
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

        return response.send_message([res])
    else:
        print("more than 4 services present.")
        items = []
        responses = []
        counter = 0
        imgs = random.sample(config.IMAGES, 4)
        for i, service in enumerate(service_names):

            if (counter + 1) % 4 == 0:
                # got 4 items
                responses.append(response.generate_list('test', items))
                items = []
                imgs = random.sample(config.IMAGES, 4)
                counter = 0

            description = util.remove_html(descriptions[i])
            test_item = {
                "title": service,
                "subtitle": description.split('\n', 1)[0],
                "image_url": imgs[counter]
            }
            items.append(test_item)
            counter += 1

        return response.send_message(responses)


def show_detail_selection(message):
    msg_1 = response.generate_text('Sie möchten Informationen über: "{}".'.format(message.service))
    msg_2 = response.generate_quick_replies('Was möchten Sie erfahren?', config.KEYS)

    return response.send_message([msg_1[0], msg_2])

def show_detail(message):
    data = util.get_data("/tree/" + message.topic + "/" + message.objective)
    if not data:
        res = response.generate_text("could not find data at {} {}".format(message.topic,
                                                               message.objective))
        return response.send_message(res)

    relevant_service = next(tmp for tmp in data if tmp["name"] == message.service)

    # key-dependent parsing
    if message.detail == 'meta':
        speech = detail_parser.parse_link(relevant_service[message.detail])
    elif message.detail == 'appointment':
        speech = detail_parser.parse_appointment(relevant_service[message.detail])
    elif message.detail in ['requirements', 'prerequisites']:
        speech = detail_parser.parse_requirements_or_prerequisites(relevant_service[message.detail])
    elif message.detail == 'fees':
        speech = util.remove_html(relevant_service[message.detail], True)
    elif message.detail == 'onlineprocessing':
        speech = detail_parser.parse_onlineprocessing(relevant_service[message.detail])
    elif message.detail == 'description':
        print('detail = description')
        speech = "Was möchten Sie erfahren?"
        msgs = response.generate_text(util.remove_html(relevant_service[message.detail], False))
        quick = response.generate_quick_replies(speech, config.KEYS)
        msgs.append(quick)
        return response.send_message(msgs)
    elif message.detail == 'process_time':
        speech = detail_parser.parse_processtime(util.remove_html(relevant_service[message.detail], False))
    elif message.detail == 'Zurück':
        res = response.generate_text("Guten Tag! Ich bin der Chatbot der Stadt Berlin, wie kann ich dir behilflich sein?")
        return response.send_message(res)
    else:
        speech = util.remove_html(relevant_service[message.detail], False)

    res = response.generate_quick_replies(speech, config.KEYS)
    return response.send_message([res])
