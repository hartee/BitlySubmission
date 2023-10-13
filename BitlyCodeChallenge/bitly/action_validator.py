import json
from bitly.event_validator import *

class ActionValidator(EventValidator):
    """

    Anomaly reasoning:
    1) if the action is sign_up_finish_api
    """

    # class constants
    ACTION_MISSING_SCORE = 1.0
    ACTION_IS_API_SCORE = 0.1

    def validate(self, event):
        # get email from event
        data = json.loads(event)
        try:
            action = data['action']
        except KeyError as e:
            self.logger.add_alert(f"ActionValidator: missing action. Score +{self.ACTION_MISSING_SCORE}", self.ACTION_MISSING_SCORE)
            return

        if action == "sign_up_finish_api":
            self.logger.add_alert(f"ActionValidator: action ({action}) is suspicious. Score +{self.ACTION_IS_API_SCORE}", self.ACTION_IS_API_SCORE)
