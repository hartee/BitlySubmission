import json
from bitly.event_validator import *

class UserAgentValidator(EventValidator):
    """
    This validator looks at the user_agent.  Mainly we are checking if it is
    too long as that seems to carry signal on it being suspect.  We also
    note whether it is missing.

    The length we use to determine suspect is not well researched and is the
    result of just reviewing the sample data, so it could use some tuning love.
    """

    USER_AGENT_SUSPICIOUS_LENGTH = 300
    USER_AGENT_SUSPICIOUS_SCORE = .80

    def validate(self, event):
        data = json.loads(event)
        try:
            user_agent = data['user_agent']
            if len(user_agent) > self.USER_AGENT_SUSPICIOUS_LENGTH:
                if (self.logger):
                    self.logger.add_alert(f"UserAgentValidator: user_agent suspiciously long. Score +{self.USER_AGENT_SUSPICIOUS_SCORE}", self.USER_AGENT_SUSPICIOUS_SCORE)
        except KeyError as e:
            if (self.logger):
                self.logger.add_alert(f"UserAgentValidator: missing user_agent. Score +{self.USER_AGENT_SUSPICIOUS_SCORE}", self.USER_AGENT_SUSPICIOUS_SCORE)
