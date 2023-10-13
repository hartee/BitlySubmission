import json
from bitly.event_validator import *

class UserAgentValidator(EventValidator):
    """

    Anomaly reasoning:
    1) if too long
    2) if doesn't have the right words?
    """

    # class constants
    USER_AGENT_SUSPICIOUS_LENGTH = 300
    USER_AGENT_SUSPICIOUS_SCORE = .80


    def validate(self, event):
        # get email from event
        data = json.loads(event)
        try:
            user_agent = data['user_agent']
            if len(user_agent) > self.USER_AGENT_SUSPICIOUS_LENGTH:
                self.logger.add_alert(f"UserAgentValidator: user_agent suspiciously long. Score +{self.USER_AGENT_SUSPICIOUS_SCORE}", self.USER_AGENT_SUSPICIOUS_SCORE)
        except KeyError as e:
            self.logger.add_alert(f"UserAgentValidator: missing user_agent. Score +{self.USER_AGENT_SUSPICIOUS_SCORE}", self.USER_AGENT_SUSPICIOUS_SCORE)
