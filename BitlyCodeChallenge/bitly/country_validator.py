import json
from bitly.event_validator import *

class CountryValidator(EventValidator):
    """
    This validator looks at the 'country_code' attribute

    """
    # class constants
    COUNTRY_COUNTS = {}
    COUNTRY_COUNT_IS_HIGH_SCORE = 1.0

    EXPECTED_COUNTS = {'RU':1.0,'IN':2.0}


    def validate(self, event):
        """
        """
        data = json.loads(event)
        try:
            country_code = data['country_code']
            if country_code in self.COUNTRY_COUNTS:
                self.COUNTRY_COUNTS[country_code] += 1
            else:
                self.COUNTRY_COUNTS[country_code] = 1
        except KeyError as e:
            pass

    def self_report(self):
        print()
        print("CountryValidator report:")

        total_count = 0
        for value in self.COUNTRY_COUNTS.values():
            total_count += value

        for country, count in self.COUNTRY_COUNTS.items():
            country_perc = count / total_count * 100
            #print(country, count, country_perc)

            if country in self.EXPECTED_COUNTS:
                if country_perc > self.EXPECTED_COUNTS[country]:
                    print(f"CountryValidator: Country {country} count is high: saw ({country_perc:.2e}), expected ({self.EXPECTED_COUNTS[country]})")
