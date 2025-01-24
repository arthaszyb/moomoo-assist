import logging
from utils.logger import setup_logger
from api.moomoo_api import MooMooAPI
from api.moomoo_openD import MooMooOpenD
from features.company_feedback import CompanyFeedback
from features.stock_recommendation import StockRecommendation
from features.todays_sentiment import TodaysSentiment
from features.automated_trading import AutomatedTrading
import yaml

def load_config():
    """Load configuration from yaml file"""
    with open('src/config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def main():
    """
    Entry point for the MooMoo Investment Assistant Tool.
    Initializes the system and routes user commands.
    """
    # Setup logger
    logger = setup_logger('app_logger')
    
    try:
        # Load configuration
        config = load_config()
        
        # Initialize MooMoo API
        moomoo_api = MooMooAPI(
            host=config.get('api', {}).get('host', '127.0.0.1'),
            port=config.get('api', {}).get('port', 11111),
            is_encrypt=config.get('api', {}).get('is_encrypt', False),
            api_key=config.get('api', {}).get('moomoo_api_key')
        )
        
        # Initialize APIs
        moomoo_openD = MooMooOpenD(stream_url=config['api']['moomoo_openD_url'])

        # Initialize Features
        company_feedback = CompanyFeedback(moomoo_api, moomoo_openD)
        stock_recommendation = StockRecommendation(moomoo_api)
        todays_sentiment = TodaysSentiment(moomoo_api, moomoo_openD)
        automated_trading = AutomatedTrading(moomoo_api, moomoo_openD)

        # Example usage with error handling
        try:
            symbol = input("Enter stock symbol for feedback: ")
            recommendation = company_feedback.analyze_stock(symbol)
            print(f"Recommendation for {symbol}: {recommendation}")
            
            sentiment = todays_sentiment.analyze_news_sentiment(symbol)
            print(f"Today's sentiment for {symbol}: {sentiment}")
            
            logger.info("Analysis completed successfully")
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            print(f"Error analyzing stock: {str(e)}")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
