"""
script to parse detail informations
"""

import strs

def parse_requirements_or_prerequisites(requirements):
    """
    requirements format:
    [{
        "description": desc,
        "link": link,
        "name": name
    }]
    """
    text = """"""
    for i, requirement in enumerate(requirements):
        name = requirement["name"]
        desc = requirement["description"]
        link = requirement["link"]

        tmp = """{number}: {name} \n {desc} \n {link}""".format(number= i + 1,
                                                                name = name,
                                                                desc = desc,
                                                                link = link)
        text += tmp

    return text

def parse_appointment(appointment):
    if appointment["link"]:
        return appointment["link"]
    else:
        return strs.APPOINTMENT

def parse_link(meta):
    """
    meta in format:
    {
        "keywords": [keywords],
        "lastupdate": ts,
        "locale": de,
        "url": //link
    }
    """
    return strs.LINK.format(meta["url"][2:])

def parse_onlineprocessing(onlineprocessing):
    """
    onlineprocessing in format:
    {
        "description": "true",
        "link": //link
    }
    """
    if onlineprocessing["description"] == "true":
        return strs.ONLINE_PROCESSING.format(onlineprocessing["link"][2:])
    else:
        return strs.OFFLINE_PROCESSING

def parse_processtime(process_time):
    if process_time == "false":
        return strs.NO_PROCESS_TIME
    else:
        return process_time
