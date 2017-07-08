import responses_templates
import copy

def generate_text(speech):
    return {
        "speech": str(speech),
        "displayText": str(speech),
        "data": [],
        "contextOut": [],
        "source": "api"
    }

def generate_quick_replies(speech, options):
     template = copy.deepcopy(responses_templates.quick_reply_template)
     template["text"] = speech

     for option in options:
         reply = copy.deepcopy(responses_templates.quick_reply_element)
         reply['title'] = option
         reply['payload'] = option

         template["quick_replies"].append(reply)

     return {
         "speech": str(speech),
         "displayText": str(speech),
         "data": {"facebook": template},
         "contextOut": [],
         "source": "api",
         "messages": [
         {
             "type": 0,
             "speech": "; ".join(options)
         }]
     }

def generate_list(speech, listings):
    """
    listings in format
    {
        "title": title,
        "subtitle": subtitle,
        "image_url": url,

    }
    """
    template = copy.deepcopy(responses_templates.list_template)

    for elem in listings:
        element = copy.deepcopy(responses_templates.list_element)
        element["title"] = elem["title"]
        element["image_url"] = elem["image_url"]
        element["subtitle"] = elem["subtitle"]
        element['buttons'].append(generate_button("web_url", "View", "https://google.com"))

        template['attachment']['payload']['elements'].append(element)

    return {
        "speech": str(speech),
        "displayText": str(speech),
        "data": {"facebook": template},
        "contextOut": [],
        "source": "api",
        "messages": [
        {
            "type": 0,
            "speech": "; ".join([x["title"] for x in listings])
        }]
    }


def generate_card(speech, cards):
    """
    cards in format
    {
        "title": title,
        "subtitle": subtitle,
        "image_url": url
    }
    """
    template = copy.deepcopy(responses_templates.card_template)

    for card in cards:

        card_template = copy.deepcopy(responses_templates.card_element)

        card_template["title"] = card["title"]
        card_template["image_url"] = card["image_url"]
        card_template["subtitle"] = card["subtitle"]

        card_template["buttons"].append(generate_button("postback", "TestTitle"))

        template["attachment"]["payload"]["elements"].append(card_template)

    return {
        "speech": str(speech),
        "displayText": str(speech),
        "data": {"facebook": template},
        "contextOut": [],
        "source": "api",
        "messages": [
        {
            "type": 0,
            "speech": "; ".join([x["title"] for x in cards])
        }]
    }

def generate_button(btn_type, title, url=""):
    if btn_type == "web_url":
        return {
            "type": btn_type,
            "url": url,
            "title": title
        }
    else:
        return {
            "type": "postback",
            "title": title,
            "payload": title
        }
