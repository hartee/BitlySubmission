import unittest
import os
from bitly.event_validator import EventValidator, EventLogger
from bitly.action_validator import ActionValidator


class TestActionValidator(unittest.TestCase):
    MISSING_ACTION_EVENT = '{}'
    SUSPICIOUS_ACTION_EVENT = '{"action":"sign_up_finish_api"}'
    VALID_ACTION_EVENT = '{"action":"sign_up_finish_google"}'

    LOGGER = EventLogger()
    VALIDATOR = ActionValidator(LOGGER)

    def test_validate_when_action_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_ACTION_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],"ActionValidator: missing action. Score +1.0")

    def test_validate_when_action_is_suspicious_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.SUSPICIOUS_ACTION_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],"ActionValidator: action (sign_up_finish_api) is suspicious. Score +0.1")

    def test_validate_when_action_is_valid_succeeds(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.VALID_ACTION_EVENT)
        self.assertEqual(len(self.LOGGER.get_alerts()),0)

if __name__ == "__main__":
    unittest.main()
