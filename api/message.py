"""
message class
"""

import util
import request_handling

class Message:
    def __init__(self, intent, topic="", objective="", service="", detail="", state=""):
        self.intent = intent
        self.topic = topic
        self.objective = objective
        self.service = service
        self.detail = detail
        self.state = state

    def get_state(self):
        return self.state

    def set_state(self):
        """
        set state
        """
        if not self.objective:
            # get data at topic
            data = util.get_data("/tree/" + self.topic)
            if not data:
                # fallback
                print("no data found.")
            else:
                n_objectives = len(list(data.keys()))

                if n_objectives < 2:
                    # jump to service selection hence only 1 objective present
                    self.state = "show_service_selection"
                    self.objective = list(data.keys())[0]
                else:
                    # otherwise show objective first
                    self.state = "show_objective_selection"
        elif not self.service:
            self.state = "show_service_selection"
        elif not self.detail:
            self.state = "show_detail_selection"
        else:
            self.state = "show_detail"

    def handle_message(self):
        """
        handle message dependent on state
        """
        if self.state == "show_objective_selection":
            response = request_handling.show_objective_selection(self)
        elif self.state == "show_service_selection":
            response = request_handling.show_service_selection(self)
        elif self.state == "show_detail_selection":
            response = request_handling.show_detail_selection(self)
        else:
            # state "show_detail"
            response = request_handling.show_detail(self)
        return response
