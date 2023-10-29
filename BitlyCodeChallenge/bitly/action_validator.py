import json
from bitly.event_validator import *

class ActionValidator(EventValidator):
    """
    This validator looks at the 'action' attribute

    There are two reasons that an event might be considered suspicious due to
    this attribute.  First is if it is missing.  This should never happen and
    wasn't seen in the data.

    The other is is the action is "sign_up_finish_api".  I don't know if this
    is actually signal that the event is suspicious for sure, so I give it a
    very low score.
    """
    # class constants
    ACTION_MISSING_SCORE = 1.0
    ACTION_IS_API_SCORE = 0.1

    def validate(self, event):
        """
        Load the event (a JSON block) and test the 'action' attribute,
        logging an alert if necessary.
        """
        data = json.loads(event)
        try:
            action = data['action']
        except KeyError as e:
            if (self.logger):
                self.logger.add_alert(f"ActionValidator: missing action. Score +{self.ACTION_MISSING_SCORE}", self.ACTION_MISSING_SCORE)
            return

        if action == "sign_up_finish_api":
            if (self.logger):
                self.logger.add_alert(f"ActionValidator: action ({action}) is suspicious. Score +{self.ACTION_IS_API_SCORE}", self.ACTION_IS_API_SCORE)
