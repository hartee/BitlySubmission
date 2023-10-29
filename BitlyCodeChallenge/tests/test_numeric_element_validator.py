import unittest
import os
from bitly.event_validator import EventValidator, EventLogger
from bitly.numeric_element_validator import NumericElementValidator


class TestNumericElementValidator(unittest.TestCase):

    CITY_NUMERIC_EVENT = '{"city":"123"}'
    IP_DOMAIN_NUMERIC_EVENT = '{"ip_domain":"123.net"}'
    EMAIL_NUMERIC_EVENT = '{"email":"123"}'
    COUNTRY_CODE_NUMERIC_EVENT = '{"country_code":"123"}'
    IP_ORGANIZATION_NUMERIC_EVENT = '{"ip_organization":"123.net"}'
    LANG_NUMERIC_EVENT = '{"lang":"123"}'
    NETWORK_NAME_NUMERIC_EVENT = '{"network_name":"123"}'
    REGION_NUMERIC_EVENT = '{"region":"123"}'

    VALID_EVENT = '{"city":"foo","ip_domain":"foo","email":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'

    LOGGER = EventLogger()
    VALIDATOR = NumericElementValidator()
    VALIDATOR.set_logger(LOGGER)


    def test_extract_name_when_ip_domain_is_valid_succeeds(self):
        ip_domain = "gmail.com"
        result = self.VALIDATOR.extract_name(ip_domain)
        self.assertEqual(result,"gmail")

    def test_extract_name_when_ip_domain_is_malformed_fails(self):
        ip_domain = "gmail"
        result = self.VALIDATOR.extract_name(ip_domain)
        self.assertEqual(result,None)

    # city
    def test_validate_when_city_is_numeric_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.CITY_NUMERIC_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"NumericElementValidator: city is numeric: 123. Score +{NumericElementValidator.CITY_NUMERIC_SCORE}")

    # ip_domain
    def test_validate_when_ip_domain_is_numeric_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.IP_DOMAIN_NUMERIC_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"NumericElementValidator: ip_domain is numeric: 123.net. Score +{NumericElementValidator.IP_DOMAIN_NUMERIC_SCORE}")

    # email
    def test_validate_when_email_is_numeric_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.EMAIL_NUMERIC_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"NumericElementValidator: email is numeric: 123. Score +{NumericElementValidator.EMAIL_NUMERIC_SCORE}")

    # country_code
    def test_validate_when_country_code_is_numeric_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.COUNTRY_CODE_NUMERIC_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"NumericElementValidator: country_code is numeric: 123. Score +{NumericElementValidator.COUNTRY_CODE_NUMERIC_SCORE}")

    # lang
    def test_validate_when_lang_is_numeric_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.LANG_NUMERIC_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"NumericElementValidator: lang is numeric: 123. Score +{NumericElementValidator.LANG_NUMERIC_SCORE}")

    # network_name
    def test_validate_when_network_name_is_numeric_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.NETWORK_NAME_NUMERIC_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"NumericElementValidator: network_name is numeric: 123. Score +{NumericElementValidator.NETWORK_NAME_NUMERIC_SCORE}")

    # region
    def test_validate_when_region_is_numeric_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.REGION_NUMERIC_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"NumericElementValidator: region is numeric: 123. Score +{NumericElementValidator.REGION_NUMERIC_SCORE}")


    # all fields present and non-numeric
    def test_validate_when_event_is_valid_succeeds(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.VALID_EVENT)
        self.assertEqual(len(self.LOGGER.get_alerts()),0)

if __name__ == "__main__":
    unittest.main()
