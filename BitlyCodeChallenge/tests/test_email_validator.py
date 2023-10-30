import unittest
import os
from bitly.event_validator import EventValidator, EventLogger
from bitly.email_validator import EmailValidator


class TestEmailValidator(unittest.TestCase):
    BLACK_LIST = os.path.join(os.path.dirname(__file__), "data", "blacklist.txt")
    WHITE_LIST = os.path.join(os.path.dirname(__file__), "data", "whitelist.txt")

    MISSING_EMAIL_EVENT = '{}'
    MALFORMED_EMAIL_EVENT = '{"email":"wrong.email.com"}'
    BLACKLISTED_EMAIL_EVENT = '{"email":"myname@whoer.net"}'
    WHITELISTED_EMAIL_EVENT = '{"email":"myname@gmail.com"}'
    VALID_EMAIL_EVENT = '{"email":"myname@erikanthony.net"}'

    LOGGER = EventLogger()
    VALIDATOR = EmailValidator(BLACK_LIST, WHITE_LIST)
    VALIDATOR.set_logger(LOGGER)


    def test_extract_domain_when_email_is_valid_succeeds(self):
        email = "valid@gmail.com"
        result = self.VALIDATOR.extract_domain(email)
        self.assertEqual(result,"gmail.com")

    def test_extract_domain_when_email_is_malformed_fails(self):
        email = "gmail.com"
        result = self.VALIDATOR.extract_domain(email)
        self.assertEqual(result,None)

    def test_is_valid_email_when_email_is_valid_succeeds(self):
        email = "valid@gmail.com"
        email_with_subdomain = "valid@subdomain.dummy.co.ru"
        self.assertTrue(self.VALIDATOR.is_valid_email(email))
        self.assertTrue(self.VALIDATOR.is_valid_email(email_with_subdomain))

    def test_is_valid_email_when_email_is_not_valid_fails(self):
        email = "valid.com"
        email_with_bad_characters = "valid$.com"
        email_with_bad_subdomain = "valid@subdomain.dummy.co.99"
        self.assertFalse(self.VALIDATOR.is_valid_email(email))
        self.assertFalse(self.VALIDATOR.is_valid_email(email_with_bad_characters))
        self.assertFalse(self.VALIDATOR.is_valid_email(email_with_bad_subdomain))

    def test_validate_when_email_is_missing_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MISSING_EMAIL_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],"EmailValidator: missing email. Score +0.1")

    def test_validate_when_email_is_malformed_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.MALFORMED_EMAIL_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],"EmailValidator: malformed email (wrong.email.com). Score +0.4")

    def test_validate_when_email_is_blacklisted_logs_alert(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.BLACKLISTED_EMAIL_EVENT)
        self.assertEqual(self.LOGGER.get_alerts()[0],"EmailValidator: email domain (whoer.net) is blacklisted. Score +0.8")

    def test_validate_when_email_is_whitelisted_succeeds(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.WHITELISTED_EMAIL_EVENT)
        self.assertEqual(len(self.LOGGER.get_alerts()),0)

    def test_validate_when_email_is_valid_succeeds(self):
        self.LOGGER.clear_alerts()
        self.VALIDATOR.validate(self.VALID_EMAIL_EVENT)
        self.assertEqual(len(self.LOGGER.get_alerts()),0)

if __name__ == "__main__":
    unittest.main()
