from src.api.moomoo_api import MooMooAPI
from src.utils.data_processing import process_market_data
import logging

class StockRecommendation:
    """
    Screens and recommends stocks based on predefined investment preferences and selection principles.
    """

    def __init__(self, moomoo_api: MooMooAPI):
        self.api = moomoo_api
        self.logger = logging.getLogger('StockRecommendation')
        self.preferences = {
            "Growth": {"revenue_growth": 20, "profit_growth": 20},
            "Value": {"pe_ratio": 20, "pb_ratio": 3}
            # Add more preferences as needed
        }

    def recommend_stocks(self, preference: str = "Growth") -> list:
        """
        Recommends a list of stocks based on the specified investment preference.
        """
        self.logger.info(f"Generating stock recommendations based on {preference} preference.")
        market_stocks = self.api.get_market_stock_list()
        if not market_stocks:
            self.logger.error("Failed to retrieve market stock list.")
            return []

        filtered_stocks = []
        for stock in market_stocks:
            if self.meets_criteria(stock, preference):
                filtered_stocks.append(stock)

        self.logger.info(f"Recommended stocks: {[stock['symbol'] for stock in filtered_stocks]}")
        return filtered_stocks

    def meets_criteria(self, stock: dict, preference: str) -> bool:
        """
        Determines if a stock meets the criteria based on the investment preference.
        """
        criteria = self.preferences.get(preference, {})
        for key, value in criteria.items():
            if stock.get(key, 0) < value:
                return False
        return True
