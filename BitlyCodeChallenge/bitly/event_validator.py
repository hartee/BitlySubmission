import json

class EventLogger():
    """
    The EventLogger is used by the main program class to track alerts.  It is
    passed to each validator to let them accumulate alerts and scores.  After
    all the validators have had their say, if the total score is above a
    provided threshold, the alerts are then displayed and the anomaly
    reported.
    """

    def __init__(self):
        self.alerts = []
        self.total_events = 0
        self.anomalies = 0
        self.score = 0.0

    def add_alert(self,alert,score):
        self.alerts.append(alert)
        self.anomalies += 1
        self.score += score

    def score_above_threshold(self,threshold):
        return self.score > threshold

    def display_alerts(self):
        if len(self.alerts) != 0:
            print(f"Anomaly Detected: score({self.score:.2f})")
            for alert in self.alerts:
                print(alert)
            print()

    def clear_alerts(self):
        self.alerts = []
        self.score = 0

    def get_alerts(self):
        return self.alerts


class EventValidator():
    """
    Base class for validators.
    """

    def __init__(self,logger):
        self.logger = logger

    def validate(self, event):
        """
        All validators must override this method
        """
        raise NotImplementedError("Subclasses must implement validate")
