

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
        return "Für diese Dienstleistung können Sie leider keinen Termin vereinbaren."

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
    return "Alle Informationen über diese Dienstleistung finden sie unter: {}".format(meta["url"][2:])

def parse_onlineprocessing(onlineprocessing):
    """
    onlineprocessing in format:
    {
        "description": "true",
        "link": //link
    }
    """
    if onlineprocessing["description"] == "true":
        return "Die Online Bearbeitung finden sie unter: {}".format(onlineprocessing["link"][2:])
    else:
        return "Diese Dienstleistung können wir leider nur vor Ort bearbeiten."

def parse_processtime(process_time):
    if process_time == "false":
        return "Die Dauer kann leider nicht vorhergesagt werden."
    else:
        return process_time
