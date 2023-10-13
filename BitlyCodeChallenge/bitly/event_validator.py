'''
event_validators
'''

import json

class EventLogger():
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
    def __init__(self,logger):
        self.logger = logger

    def validate(self, event):
        pass
