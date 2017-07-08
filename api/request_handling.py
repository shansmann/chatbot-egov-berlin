import util
import response


def topic_only(result):
    # find objectives
    topic = result["parameters"]["topic"]

    data = util.get_data("/tree/" + topic)
    if not data:
        return response.generate_text("could not find data at " + topic)

    objective_names = list(data.keys())

    # only 1 objective present
    if len(objective_names) == 1:
        print("only 1 objective found.")

    speech = "Es geht also um {}? Kannst du mir hier noch schnell weiterhelfen?".format(topic)

    res = response.generate_quick_replies(speech, objective_names)
    return res

def objective_only(result):
    # find services
    relevant_context = next(item for item in result["contexts"] if item["name"] == "topic-recognized")
    topic = relevant_context["parameters"]["topic"]
    objective = result["parameters"]["obj_wo_syn"]

    data = util.get_data("/tree/" + topic + "/" + objective)
    if not data:
        return response.generate_text("could not find data at " + topic + " " + objective)

    service_names = [x["name"] for x in data]

    # only 1 service present
    if len(service_names) == 1:
        print("only 1 service found.")

    speech = "Gleich hast du es geschafft! Mit diesen Dingen kann ich dir behilflich sein:"
    res = response.generate_quick_replies(speech, service_names)

    return res

def topic_objective(result):
    # find services
    topic = result["parameters"]["topic"]
    objective = result["parameters"]["obj_wo_syn"]

    data = util.get_data("/tree/" + topic + "/" + objective)
    if not data:
        return response.generate_text("could not find data at " + topic + " " + objective)

    service_names = [x["name"] for x in data]

    # only 1 service present
    if len(service_names) == 1:
        print("only 1 service found.")

    speech = "Gleich hast du es geschafft! Mit diesen Dingen kann ich dir behilflich sein:"
    res = response.generate_quick_replies(speech, service_names)

    return res

def service_selection(result):
    keys = ["Gebühren", "Termin", "Online", "Vorrausetzungen", "Dauer", "Verantwortlichkeit"]
    return response.generate_quick_replies("Gleich haben sie es geschafft!", keys)

def detail_selection(result):
    # find service values
    relevant_topic_context = next(item for item in result["contexts"] if item["name"] == "topic-recognized")
    relevant_objective_context = next(item for item in result["contexts"] if item["name"] == "objective-recognized")
    relevant_service_context = next(item for item in result["contexts"] if item["name"] == "service-recognized")

    topic = relevant_topic_context["parameters"]["topic"]
    objective = relevant_objective_context["parameters"]["obj_wo_syn"]
    service = relevant_service_context["parameters"]["service"]
    key = result["parameters"]["detail"]

    data = util.get_data("/tree/" + topic + "/" + objective)

    if not data:
        return response.generate_text("could not find data at " + topic + " " + objective + " " + key)

    relevant_service = next(tmp for tmp in data if tmp["name"] == service)
    res = response.generate_text(relevant_service[key])

    return res

def fallback(result):
    #return response.generate_card('testResponse', ['1', '2'])
    return response.generate_text('Intent {} not found.'.format(result))
    #return response.generate_quick_replies("Choose:", ["option1", "option2"])
    #return response.generate_list("Test", ["list1", "list2"])
