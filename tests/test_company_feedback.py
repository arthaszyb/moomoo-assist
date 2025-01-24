import unittest
from src.api.moomoo_api import MooMooAPI
from src.api.moomoo_openD import MooMooOpenD
from src.features.company_feedback import CompanyFeedback

class TestCompanyFeedback(unittest.TestCase):
    def setUp(self):
        self.api = MooMooAPI(api_key="test_api_key")
        self.stream = MooMooOpenD(stream_url="wss://test_stream_url")
        self.feedback = CompanyFeedback(self.api, self.stream)

    def test_analyze_stock_buy(self):
        # Mock the API responses
        self.api.get_stock_quote = lambda symbol: {
            'current_price': 150,
            'pe_ratio': 18,
            'pb_ratio': 2
        }
        self.feedback.calculate_moving_average = lambda symbol, period=20: 140
        self.feedback.analyze_news_sentiment = lambda symbol: "Positive"

        result = self.feedback.analyze_stock("AAPL")
        self.assertEqual(result, "Buy")

    def test_analyze_stock_sell(self):
        self.api.get_stock_quote = lambda symbol: {
            'current_price': 130,
            'pe_ratio': 22,
            'pb_ratio': 3.5
        }
        self.feedback.calculate_moving_average = lambda symbol, period=20: 140
        self.feedback.analyze_news_sentiment = lambda symbol: "Negative"

        result = self.feedback.analyze_stock("AAPL")
        self.assertEqual(result, "Sell")

    def test_analyze_stock_hold(self):
        self.api.get_stock_quote = lambda symbol: {
            'current_price': 145,
            'pe_ratio': 20,
            'pb_ratio': 3
        }
        self.feedback.calculate_moving_average = lambda symbol, period=20: 140
        self.feedback.analyze_news_sentiment = lambda symbol: "Neutral"

        result = self.feedback.analyze_stock("AAPL")
        self.assertEqual(result, "Hold")

if __name__ == '__main__':
    unittest.main()
