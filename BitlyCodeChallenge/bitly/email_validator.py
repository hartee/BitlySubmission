import json
import os
from bitly.event_validator import *

class EmailValidator(EventValidator):
    """
    This validator looks at the 'email' attribute

    If the email is missing or malformed, that is suspect.
    Also, if the email is on a blacklist.

    My logic here is that a malformed email is more suspect than a missing
    one.
    """
    WHITE_LIST = os.path.join(os.path.dirname(__file__), "data", "whitelist.txt")
    BLACK_LIST = os.path.join(os.path.dirname(__file__), "data", "blacklist.txt")

    EMAIL_MISSING_SCORE = .1
    EMAIL_DOMAIN_BLACKLIST_SCORE = .8
    EMAIL_MALFORMED_SCORE = .4


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
        """
        Split the email address at the "@" symbol
        and return the domain, or None.
        """
        parts = email.split("@")

        if len(parts) == 2:
            domain = parts[1]
            return domain
        else:
            return None


    def validate(self, event):
        """
        Load the event (a JSON block) and test the 'email' attribute,
        logging an alert if necessary.
        """
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
