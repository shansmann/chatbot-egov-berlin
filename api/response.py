import responses_templates
import copy

def generate_text(speech, context=[]):
    return {
        "speech": str(speech),
        "displayText": str(speech),
        "data": [],
        "contextOut": context,
        "source": "api"
    }

def generate_multiple_lines(lines):
    response = {
        "speech": "",
        "messages": []
    }
    for line in lines:
        message = {
            "type": 0,
            "platform" : "facebook",
            "speech": line
        }
        response["messages"].append(message)

    return response

def generate_quick_replies(speech, options, contexts = []):
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
         "contextOut": contexts,
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
        element['buttons'].append(generate_button("postback", "Mehr Informationen", postback=elem["title"]))

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
        print("generate card: ", card)
        """
        card_template = copy.deepcopy(responses_templates.card_element)

        card_template["title"] = card["title"]
        card_template["image_url"] = card["image_url"]
        card_template["subtitle"] = card["subtitle"]

        card_template["buttons"].append(generate_button("postback", card["title"]))

        template["attachment"]["payload"]["elements"].append(card_template)
        """
        title = card["title"]

        button = generate_button("postback", "Mehr Informationen", postback=title)

        card["buttons"] = [button]

        template["attachment"]["payload"]["elements"].append(card)

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

def generate_button(btn_type, title, url="", postback=None):
    if btn_type == "web_url":
        return {
            "type": btn_type,
            "url": url,
            "title": title
        }
    else:
        if postback:
            return {
                "type": "postback",
                "title": title,
                "payload": postback
            }
        else:
            return {
                "type": "postback",
                "title": title,
                "payload": title
            }
