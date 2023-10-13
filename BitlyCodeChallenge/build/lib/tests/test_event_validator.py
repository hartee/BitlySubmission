import unittest
from bitly.event_validator import EventLogger

class TestEventLogger(unittest.TestCase):
    def test_score_above_threshold_score_is_above_succeeds(self):
        logger = EventLogger()

        logger.add_alert("Test alert 1", 0.5)
        logger.add_alert("Test alert 2", 0.75)

        result = logger.score_above_threshold(1.0)
        self.assertTrue(result)

    def test_score_above_threshold_score_is_below_fails(self):
        logger = EventLogger()

        logger.add_alert("Test alert 1", 0.25)
        logger.add_alert("Test alert 2", 0.25)

        result = logger.score_above_threshold(1.0)
        self.assertFalse(result)

    def test_clear_alerts_succeeds(self):
        logger = EventLogger()

        logger.add_alert("Test alert 1", 0.25)
        logger.add_alert("Test alert 2", 0.25)

        logger.clear_alerts()
        self.assertEqual(len(logger.alerts),0)

if __name__ == "__main__":
    unittest.main()
