import unittest
from unittest.mock import MagicMock
from src.api.moomoo_api import MooMooAPI
from src.features.todays_sentiment import TodaysSentiment

class TestTodaysSentiment(unittest.TestCase):
    def test_analyze_sentiment(self):
        mock_api = MooMooAPI(api_key="test_key")
        ts = TodaysSentiment(api=mock_api)
        sentiment = ts.analyze_sentiment()
        self.assertIn(sentiment, ["Optimistic", "Neutral", "Pessimistic", "Error"])

if __name__ == '__main__':
    unittest.main()
