import unittest
import os
from bitly.event_validator import EventValidator, EventLogger
from bitly.user_agent_validator import UserAgentValidator


class TestActionValidator(unittest.TestCase):
    MISSING_USER_AGENT_EVENT = '{}'
    SUSPICIOUS_USER_AGENT_EVENT = '{"user_agent":"this is a really long string...\
                                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
                                  sed do eiusmod tempor incididunt ut labore et dolore magna \
                                  aliqua. Ut enim ad minim veniam, quis nostrud exercitation \
                                  ullamco laboris nisi ut aliquip ex ea commodo consequat. \
                                  Duis aute irure dolor in reprehenderit in voluptate velit \
                                  esse cillum dolore eu fugiat nulla pariatur. Excepteur sint \
                                  occaecat cupidatat non proident, sunt in culpa qui officia \
                                  deserunt mollit anim id est laborum."}'

    VALID_USER_AGENT_EVENT = '{"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}'

    LOGGER = EventLogger()
    VALIDATOR = UserAgentValidator()
    VALIDATOR.set_logger(LOGGER)

    def test_validate_when_user_agent_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_USER_AGENT_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],F"UserAgentValidator: missing user_agent. Score +{UserAgentValidator.USER_AGENT_SUSPICIOUS_SCORE}")

    def test_validate_when_user_agent_is_too_long_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.SUSPICIOUS_USER_AGENT_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"UserAgentValidator: user_agent suspiciously long. Score +{UserAgentValidator.USER_AGENT_SUSPICIOUS_SCORE}")

    def test_validate_when_user_agent_is_valid_succeeds(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.VALID_USER_AGENT_EVENT)
        self.assertEqual(len(self.LOGGER.get_alerts()),0)

if __name__ == "__main__":
    unittest.main()
