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

    def test_add_alert_counts_by_type(self):
        logger = EventLogger()

        logger.add_alert("EmailAlert: test alert 1", 0.25)
        logger.add_alert("UserAgentAlert: Test alert 2", 0.25)
        logger.update_alerts_by_type()
        
        logger.clear_alerts()

        self.assertEqual(len(logger.alerts_by_type),2)
        self.assertTrue("EmailAlert" in logger.alerts_by_type)

        logger.display_alerts_by_type()


if __name__ == "__main__":
    unittest.main()
