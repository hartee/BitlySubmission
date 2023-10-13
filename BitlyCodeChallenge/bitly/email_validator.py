import json
import os
from bitly.event_validator import *

class EmailValidator(EventValidator):
    """

    Anomaly reasoning:
    1) We have a white list and a black list of email domains
    2) if the domain is all numeric then it is SUSPECT
    TODO: 3) if the domain starts with "admin" it is SUSPECT
    """

    # class constants
    WHITE_LIST = os.path.join(os.path.dirname(__file__), "data", "whitelist.txt")
    BLACK_LIST = os.path.join(os.path.dirname(__file__), "data", "blacklist.txt")

    EMAIL_MISSING_SCORE = .30
    EMAIL_DOMAIN_BLACKLIST_SCORE = .80
    EMAIL_MALFORMED_SCORE = .40


    def __init__(self, logger, black_list_fn, white_list_fn):
        super().__init__(logger)
        self.black_list_fn = black_list_fn
        self.white_list_fn = white_list_fn
        self.black_list = []
        self.white_list = []

        with open(self.black_list_fn, "r") as file:
            for line in file:
                self.black_list.append(line.strip())

        with open(self.white_list_fn, "r") as file:
            for line in file:
                self.white_list.append(line.strip())

    def extract_domain(self,email):
        # Split the email address at the "@" symbol
        parts = email.split("@")

        # Check if the email address has the "@" symbol
        if len(parts) == 2:
            domain = parts[1]
            return domain
        else:
            return None  # Invalid email address format

    def validate(self, event):
        # get email from event
        data = json.loads(event)
        try:
            email = data['email']
        except KeyError as e:
            email = None
            # missing email is an alert
            self.logger.add_alert(f"EmailValidator: missing email. Score +{self.EMAIL_MISSING_SCORE}", self.EMAIL_MISSING_SCORE)
            return

        email_domain = self.extract_domain(email)
        if email_domain is None:
            self.logger.add_alert(f"EmailValidator: malformed email ({email}). Score +{self.EMAIL_MALFORMED_SCORE}", self.EMAIL_MALFORMED_SCORE)
        elif email_domain in self.white_list:
            return
        elif email_domain in self.black_list:
            self.logger.add_alert(f"EmailValidator: email domain ({email_domain}) is blacklisted. Score +{self.EMAIL_DOMAIN_BLACKLIST_SCORE}", self.EMAIL_DOMAIN_BLACKLIST_SCORE)
