import unittest
import os
from bitly.event_validator import EventValidator, EventLogger
from bitly.missing_element_validator import MissingElementValidator


class TestMissingElementValidator(unittest.TestCase):
    MISSING_CITY_EVENT = '{"ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'
    EMPTY_CITY_EVENT = '{"city":"","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'

    MISSING_IP_DOMAIN_EVENT = '{"city":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'
    EMPTY_IP_DOMAIN_EVENT = '{"city":"foo","ip_domain":"","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'

    MISSING_POSTAL_CODE_EVENT = '{"city":"foo","ip_domain":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'
    EMPTY_POSTAL_CODE_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'

    MISSING_COUNTRY_CODE_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'
    EMPTY_COUNTRY_CODE_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'

    MISSING_IP_ORGANIZATION_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "lang":"foo","network_name":"foo","region":"foo"}'
    EMPTY_IP_ORGANIZATION_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"","lang":"foo","network_name":"foo","region":"foo"}'

    MISSING_LANG_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","network_name":"foo","region":"foo"}'
    EMPTY_LANG_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"","network_name":"foo","region":"foo"}'

    MISSING_NETWORK_NAME_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","region":"foo"}'
    EMPTY_NETWORK_NAME_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"","region":"foo"}'

    MISSING_REGION_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo"}'
    EMPTY_REGION_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":""}'


    VALID_EVENT = '{"city":"foo","ip_domain":"foo","postal_code":"foo","country_code":"foo",\
                    "ip_organization":"foo","lang":"foo","network_name":"foo","region":"foo"}'


    LOGGER = EventLogger()
    VALIDATOR = MissingElementValidator(LOGGER)

    # city
    def test_validate_when_city_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_CITY_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: missing city. Score +{MissingElementValidator.CITY_MISSING_SCORE}")

    def test_validate_when_city_is_empty_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.EMPTY_CITY_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: empty city. Score +{MissingElementValidator.CITY_MISSING_SCORE}")

    # ip_domain
    def test_validate_when_ip_domain_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_IP_DOMAIN_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: missing ip_domain. Score +{MissingElementValidator.IP_DOMAIN_MISSING_SCORE}")

    def test_validate_when_ip_domain_is_empty_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.EMPTY_IP_DOMAIN_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: empty ip_domain. Score +{MissingElementValidator.IP_DOMAIN_MISSING_SCORE}")

    # postal_code
    def test_validate_when_postal_code_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_POSTAL_CODE_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: missing postal_code. Score +{MissingElementValidator.POSTAL_CODE_MISSING_SCORE}")

    def test_validate_when_city_is_empty_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.EMPTY_POSTAL_CODE_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: empty postal_code. Score +{MissingElementValidator.POSTAL_CODE_MISSING_SCORE}")

    # country_code
    def test_validate_when_country_code_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_COUNTRY_CODE_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: missing country_code. Score +{MissingElementValidator.COUNTRY_CODE_MISSING_SCORE}")

    def test_validate_when_country_code_is_empty_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.EMPTY_COUNTRY_CODE_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: empty country_code. Score +{MissingElementValidator.COUNTRY_CODE_MISSING_SCORE}")

    # ip_organization
    def test_validate_when_ip_organization_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_IP_ORGANIZATION_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: missing ip_organization. Score +{MissingElementValidator.IP_ORGANIZATION_MISSING_SCORE}")

    def test_validate_when_ip_organization_is_empty_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.EMPTY_IP_ORGANIZATION_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: empty ip_organization. Score +{MissingElementValidator.IP_ORGANIZATION_MISSING_SCORE}")

    # lang
    def test_validate_when_lang_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_LANG_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: missing lang. Score +{MissingElementValidator.LANG_MISSING_SCORE}")

    def test_validate_when_lang_is_empty_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.EMPTY_LANG_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: empty lang. Score +{MissingElementValidator.LANG_MISSING_SCORE}")

    # network_name
    def test_validate_when_network_name_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_NETWORK_NAME_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: missing network_name. Score +{MissingElementValidator.NETWORK_NAME_MISSING_SCORE}")

    def test_validate_when_network_name_is_empty_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.EMPTY_NETWORK_NAME_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: empty network_name. Score +{MissingElementValidator.NETWORK_NAME_MISSING_SCORE}")

    # region
    def test_validate_when_region_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_REGION_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: missing region. Score +{MissingElementValidator.REGION_MISSING_SCORE}")

    def test_validate_when_region_is_empty_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.EMPTY_REGION_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],f"MissingElementValidator: empty region. Score +{MissingElementValidator.REGION_MISSING_SCORE}")


    # all necessary fields present
    def test_validate_when_event_is_valid_succeeds(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.VALID_EVENT)
        self.assertEqual(len(self.LOGGER.get_alerts()),0)

if __name__ == "__main__":
    unittest.main()
