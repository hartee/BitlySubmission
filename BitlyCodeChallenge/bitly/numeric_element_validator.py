import json
from bitly.event_validator import *

class NumericElementValidator(EventValidator):
    """
    This validator looks for a set of attributes we expect to see.  If they
    are numeric, this is suspect.  The score is dependent on the attribute;
    some attributes have more signal than others.
    """

    CITY_NUMERIC_SCORE = .5
    IP_DOMAIN_NUMERIC_SCORE = .75
    COUNTRY_CODE_NUMERIC_SCORE = .25
    IP_ORGANIZATION_NUMERIC_SCORE = .5
    LANG_NUMERIC_SCORE = .1
    NETWORK_NAME_NUMERIC_SCORE = .5
    REGION_NUMERIC_SCORE = .5
    EMAIL_NUMERIC_SCORE = .1


    def __init__(self):
        self.logger = None
        self.numeric_fields = {}
        self.numeric_fields['city'] = self.CITY_NUMERIC_SCORE
        self.numeric_fields['ip_domain'] = self.IP_DOMAIN_NUMERIC_SCORE
        self.numeric_fields['country_code'] = self.COUNTRY_CODE_NUMERIC_SCORE
        self.numeric_fields['ip_organization'] = self.IP_ORGANIZATION_NUMERIC_SCORE
        self.numeric_fields['lang'] = self.LANG_NUMERIC_SCORE
        self.numeric_fields['network_name'] = self.NETWORK_NAME_NUMERIC_SCORE
        self.numeric_fields['region'] = self.REGION_NUMERIC_SCORE
        self.numeric_fields['email'] = self.EMAIL_NUMERIC_SCORE

    def extract_name(self,domain):
        """
        ip_domain when well-formed looks like "infornetnetwork.net.br". If we
        see something like "123.net" that is suspect.
        """
        parts = domain.split(".")
        if len(parts) == 2:
            name = parts[0]
            return name
        else:
            return None

    def validate(self, event):
        data = json.loads(event)
        for field in self.numeric_fields.keys():
            try:
                element = data[field]
                if field in ['ip_domain']:
                    value = self.extract_name(element)
                else:
                    value = element
                if str(value).isdigit():
                    if (self.logger):
                        self.logger.add_alert(f"NumericElementValidator: {field} is numeric: {element}. Score +{self.numeric_fields[field]}", self.numeric_fields[field])

            except KeyError as e:
                # this validator doesn't care if the attribute is present or not
                pass
