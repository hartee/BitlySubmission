import json
from bitly.event_validator import *

class NumericElementValidator(EventValidator):
    """

    Anomaly reasoning:
    1) if element is a number and shouldn't be
    """

    # class constants
    CITY_NUMERIC_SCORE = .25
    IP_DOMAIN_NUMERIC_SCORE = .75
    COUNTRY_CODE_NUMERIC_SCORE = .30
    IP_ORGANIZATION_NUMERIC_SCORE = .50
    LANG_NUMERIC_SCORE = .1
    NETWORK_NAME_NUMERIC_SCORE = .40
    REGION_NUMERIC_SCORE = .35
    EMAIL_NUMERIC_SCORE = .1


    def __init__(self,logger):
        super().__init__(logger)
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
        parts = domain.split(".")
        if len(parts) == 2:
            name = parts[0]
            return name
        else:
            return None

    def validate(self, event):
        # get email from event
        data = json.loads(event)
        for field in self.numeric_fields.keys():
            try:
                element = data[field]
                if field in ['ip_domain', 'ip_organization']:
                    value = self.extract_name(element)
                else:
                    value = element
                if str(value).isdigit():
                    self.logger.add_alert(f"NumericElementValidator: {field} is numeric: {element}. Score +{self.numeric_fields[field]}", self.numeric_fields[field])

            except KeyError as e:
                pass
