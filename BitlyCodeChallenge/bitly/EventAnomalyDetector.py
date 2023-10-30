
from event_ingestion import FileEventIngester
from event_validator import *
from bitly.action_validator import ActionValidator
from bitly.missing_element_validator import MissingElementValidator
from bitly.user_agent_validator import UserAgentValidator
from bitly.numeric_element_validator import NumericElementValidator
from bitly.email_validator import EmailValidator
from bitly.base_validator import BaseValidator
from bitly.country_validator import CountryValidator


class EventAnomalyDetector:
    """
    This is the main class of the project.

    The detector creates a set of validators, then reads each event from an
    ingester, passing the event through each of the validators.

    Each validator uses its own logic to determine if an event is suspect.  If
    so, it adds an alert and score to a common logger.

    Once all of the validators have had their say, the detector looks to see if
    the accumulated score for an event is greater than EVENT_THRESHOLD, if so,
    it then displays the alerts, the scores, and reports the anomaly.
    """
    EVENT_THRESHOLD = 1.2

    def __init__(self):
        self.event_validators = []
        self.total_events = 0
        self.anomalies = 0

        # attach an event logger
        self.logger = EventLogger()

    def add_validator(self,validator):
        """
        Add a new validator to the process_pipeline,
        and set it's logger
        """
        self.event_validators.append(validator)
        validator.set_logger(self.logger)

    def add_event_ingester(self,ingester):
        """
        Define the ingester which will supply events
        """
        self.ingester = ingester

    def process(self, event):
        """
        Process a single event through all the event_validators
        """
        for vl in self.event_validators:
            vl.validate(event)


    def process_pipeline(self):
        """
        This runs the whole pipeline:

        get an event,
        process it through all the validators,
        report an anomaly if found
        """
        with self.ingester as reader:
            for event in reader.get_events():
                self.total_events += 1
                self.process(event)

                # is this event likely an anomaly?
                if self.logger.score_above_threshold(self.EVENT_THRESHOLD):
                    self.anomalies += 1
                    self.logger.display_alerts()
                    self.logger.update_alerts_by_type()
                    print(event)
                    print()
                self.logger.clear_alerts()




    def report_results(self):
        print("---")
        print("Results:")
        print("---")
        print("Total events: ", self.total_events)
        print("Total anomalies: ", self.anomalies)
        print("--")
        print("Total anomalies by type:")
        self.logger.display_alerts_by_type()

        # report additional lerts by validator
        print("---")
        print("Reports by individual validators")
        self.validator_report()


    def validator_report(self):
        """
        Have each validator report
        """
        for vl in self.event_validators:
            vl.self_report()

if __name__ == "__main__":
    """
    Main program entry point
    """

    # create a new EventAnomolyDetector
    ead = EventAnomalyDetector()

    # add EventIngester
    ead.add_event_ingester(FileEventIngester(FileEventIngester.FULL_DATA))

    # add validators to the pipeline
    ead.add_validator(EmailValidator(EmailValidator.BLACK_LIST, EmailValidator.WHITE_LIST))
    ead.add_validator(ActionValidator())
    ead.add_validator(MissingElementValidator())
    ead.add_validator(UserAgentValidator())
    ead.add_validator(NumericElementValidator())
    ead.add_validator(CountryValidator())

    # process the events
    ead.process_pipeline()

    # report final tally
    ead.report_results()
