import unittest
from unittest.mock import MagicMock
from src.api.moomoo_api import MooMooAPI
from src.features.stock_recommendation import StockRecommendation

class TestStockRecommendation(unittest.TestCase):
    def test_recommend_stocks(self):
        mock_api = MooMooAPI(api_key="test_key")
        sr = StockRecommendation(api=mock_api, preference="Growth")
        stocks = sr.recommend_stocks()
        self.assertIsInstance(stocks, list)
        self.assertGreater(len(stocks), 0)

if __name__ == '__main__':
    unittest.main()
