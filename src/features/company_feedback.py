from api.moomoo_api import MooMooAPI
from api.moomoo_openD import MooMooOpenD
from utils.data_processing import process_market_data
import logging

class CompanyFeedback:
    """
    Provides investment recommendations (Buy/Sell/Hold) based on comprehensive stock analysis.
    """

    def __init__(self, moomoo_api: MooMooAPI, moomoo_openD: MooMooOpenD):
        self.api = moomoo_api
        self.stream = moomoo_openD
        self.logger = logging.getLogger('CompanyFeedback')

    def analyze_stock(self, symbol: str) -> str:
        """
        Analyzes the stock and returns a recommendation: Buy, Sell, or Hold.
        """
        self.logger.info(f"Analyzing stock: {symbol}")
        quote = self.api.get_stock_quote(symbol)
        if not quote:
            self.logger.error(f"No data available for symbol: {symbol}")
            return "Hold"

        # Example simplified analysis logic
        price = quote.get('current_price')
        moving_average = self.calculate_moving_average(symbol)
        sentiment = self.analyze_news_sentiment(symbol)

        if price > moving_average and sentiment == "Positive":
            recommendation = "Buy"
        elif price < moving_average and sentiment == "Negative":
            recommendation = "Sell"
        else:
            recommendation = "Hold"

        self.logger.info(f"Recommendation for {symbol}: {recommendation}")
        return recommendation

    def calculate_moving_average(self, symbol: str, period: int = 20) -> float:
        """
        Calculates the moving average for the given symbol and period.
        """
        # Placeholder for moving average calculation
        historical_data = self.api.get_historical_k_lines(symbol, period)
        if not historical_data:
            return 0
        prices = [day['close'] for day in historical_data]
        moving_average = sum(prices) / len(prices)
        self.logger.debug(f"{period}-day moving average for {symbol}: {moving_average}")
        return moving_average

    def analyze_news_sentiment(self, symbol: str) -> str:
        """
        Analyzes news sentiment for the given symbol.
        """
        news = self.api.get_company_news(symbol)
        if not news:
            return "Neutral"

        positive = sum(1 for article in news if "bullish" in article['title'].lower())
        negative = sum(1 for article in news if "bearish" in article['title'].lower())

        if positive > negative:
            sentiment = "Positive"
        elif negative > positive:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        self.logger.debug(f"News sentiment for {symbol}: {sentiment}")
        return sentiment
