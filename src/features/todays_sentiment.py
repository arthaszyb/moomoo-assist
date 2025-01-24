from api.moomoo_api import MooMooAPI
from api.moomoo_openD import MooMooOpenD
import logging

class TodaysSentiment:
    """
    Analyzes recent financial news and market data to determine the day's market sentiment.
    """

    def __init__(self, moomoo_api: MooMooAPI, moomoo_openD: MooMooOpenD):
        self.moomoo_api = moomoo_api
        self.moomoo_openD = moomoo_openD
        self.logger = logging.getLogger(__name__)

    def evaluate_sentiment(self) -> str:
        """
        Evaluates and returns the current market sentiment: Optimistic, Neutral, or Pessimistic.
        """
        self.logger.info("Evaluating today's market sentiment.")
        news_sentiment = self.analyze_news_sentiment()
        market_data_sentiment = self.analyze_market_data()

        if news_sentiment == "Positive" and market_data_sentiment == "Positive":
            sentiment = "Optimistic"
        elif news_sentiment == "Negative" and market_data_sentiment == "Negative":
            sentiment = "Pessimistic"
        else:
            sentiment = "Neutral"

        self.logger.info(f"Today's market sentiment: {sentiment}")
        return sentiment

    def analyze_news_sentiment(self, symbol: str) -> str:
        """Analyze sentiment for a given stock"""
        try:
            quote_data = self.moomoo_api.get_stock_quote(symbol)
            if not quote_data:
                return f"Unable to analyze - no market data available for {symbol}"

            # Basic sentiment based on price change
            change_rate = quote_data.get('change_rate', 0)
            if isinstance(change_rate, (int, float)):
                if change_rate > 1:  # More than 1% up
                    return "Strongly Positive"
                elif change_rate > 0:
                    return "Positive"
                elif change_rate < -1:  # More than 1% down
                    return "Strongly Negative"
                elif change_rate < 0:
                    return "Negative"
            return "Neutral"

        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return f"Error analyzing sentiment: {str(e)}"

    def analyze_market_data(self) -> str:
        """
        Analyzes real-time market data to determine overall sentiment.
        """
        market_snapshot = self.moomoo_api.get_market_snapshot()
        if not market_snapshot:
            return "Neutral"

        index_change = market_snapshot.get('benchmark_index_change', 0)
        adv_decl_ratio = market_snapshot.get('advancing_declining_ratio', {'advancing': 0, 'declining': 0})

        if index_change > 0 and adv_decl_ratio['advancing'] > adv_decl_ratio['declining']:
            sentiment = "Positive"
        elif index_change < 0 and adv_decl_ratio['declining'] > adv_decl_ratio['advancing']:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        self.logger.debug(f"Market data sentiment: {sentiment}")
        return sentiment
