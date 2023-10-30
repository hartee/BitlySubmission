import unittest
import os
from bitly.event_validator import EventValidator, EventLogger
from bitly.country_validator import CountryValidator


class TestCountryValidator(unittest.TestCase):
    VALID_COUNTRY_EVENT = '{"country_code":"RU"}'

    LOGGER = EventLogger()
    VALIDATOR = CountryValidator()
    VALIDATOR.set_logger(LOGGER)

    def test_validate_when_country_code_is_valid_succeeds(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.VALID_COUNTRY_EVENT)
        self.assertEqual(len(self.LOGGER.get_alerts()),0)

if __name__ == "__main__":
    unittest.main()
