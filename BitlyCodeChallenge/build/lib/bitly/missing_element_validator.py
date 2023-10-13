import json
from bitly.event_validator import *

class MissingElementValidator(EventValidator):
    """

    Anomaly reasoning:
    1) if one of the following is missing
    """

    # class constants
    CITY_MISSING_SCORE = 0.1
    IP_DOMAIN_MISSING_SCORE = 0.50
    POSTAL_CODE_MISSING_SCORE = 0.1
    COUNTRY_CODE_MISSING_SCORE = 0.1
    IP_ORGANIZATION_MISSING_SCORE = 0.40
    LANG_MISSING_SCORE = 0.1
    NETWORK_NAME_MISSING_SCORE = 0.75
    REGION_MISSING_SCORE = 0.50
    #EMAIL_MISSING_SCORE = 0.75


    def __init__(self,logger):
        super().__init__(logger)
        self.missing_fields = {}
        self.missing_fields['city'] = self.CITY_MISSING_SCORE
        self.missing_fields['ip_domain'] = self.IP_DOMAIN_MISSING_SCORE
        self.missing_fields['postal_code'] = self.POSTAL_CODE_MISSING_SCORE
        self.missing_fields['country_code'] = self.COUNTRY_CODE_MISSING_SCORE
        self.missing_fields['ip_organization'] = self.IP_ORGANIZATION_MISSING_SCORE
        self.missing_fields['lang'] = self.LANG_MISSING_SCORE
        self.missing_fields['network_name'] = self.NETWORK_NAME_MISSING_SCORE
        self.missing_fields['region'] = self.REGION_MISSING_SCORE

    def validate(self, event):
        # get email from event
        data = json.loads(event)
        for field in self.missing_fields.keys():
            try:
                element = data[field]
                if element == '':
                    self.logger.add_alert(f"MissingElementValidator: empty {field}. Score +{self.missing_fields[field]}", self.missing_fields[field])

            except KeyError as e:
                self.logger.add_alert(f"MissingElementValidator: missing {field}. Score +{self.missing_fields[field]}", self.missing_fields[field])
            continue
