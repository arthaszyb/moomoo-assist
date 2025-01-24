from moomoo import *  # MooMoo is the correct package name according to docs
from typing import Optional, Dict, Any, List
import logging
from pathlib import Path
import time  # Added for subscription handling

class MooMooAPI:
    """
    Handles interactions with the MooMoo OpenAPI for data retrieval and trading operations.
    Uses OpenQuoteContext and OpenSecTradeContext for market data and trading.
    """

    def __init__(self, 
                 host: str = '127.0.0.1', 
                 port: int = 11111, 
                 is_encrypt: bool = False,
                 api_key: Optional[str] = None):
        """
        Initialize MooMoo API connections.
        
        Args:
            host (str): OpenD listening address
            port (int): OpenD listening port
            is_encrypt (bool): Whether to enable encryption
            api_key (Optional[str]): API key for authentication
        """
        # Initialize logger first
        self.logger = logging.getLogger('MooMooAPI')
        
        try:
            # Initialize quote context for market data
            self.quote_ctx = OpenQuoteContext(
                host=host,
                port=port,
                is_encrypt=is_encrypt
            )
            
            # Initialize trade context with additional parameters
            self.trade_ctx = OpenSecTradeContext(
                filter_trdmarket=TrdMarket.US,
                security_firm=SecurityFirm.FUTUSG,
                host=host,
                port=port
            )
            
            self.logger.info("Successfully initialized MooMoo API connections")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize MooMoo API connections: {str(e)}")
            self.cleanup()
            raise

    def cleanup(self):
        """Clean up method to properly close connections"""
        try:
            if hasattr(self, 'quote_ctx'):
                self.quote_ctx.close()
            if hasattr(self, 'trade_ctx'):
                self.trade_ctx.close()
        except Exception as e:
            self.logger.error(f"Error in cleanup: {str(e)}")

    def __del__(self):
        """Destructor to ensure connections are closed"""
        self.cleanup()

    def get_stock_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get real-time quote for a stock"""
        try:
            # Get market state first
            ret_state, data_state = self.quote_ctx.get_market_state([symbol])
            if ret_state == RET_OK:
                market_state = data_state.loc[0, 'market_state']
                self.logger.info(f"Market state for {symbol}: {market_state}")

            # Get basic stock info
            ret_info, data_info = self.quote_ctx.get_stock_basicinfo(
                Market.HK if symbol.startswith('HK.') else Market.US,
                SecurityType.STOCK,
                symbol
            )
            if ret_info != RET_OK:
                self.logger.error(f"Failed to get stock info: {data_info}")
                return None

            # Get snapshot directly without subscription
            ret_snap, data_snap = self.quote_ctx.get_market_snapshot([symbol])
            if ret_snap == RET_OK and not data_snap.empty:
                snapshot_data = data_snap.iloc[0].to_dict()
                self.logger.debug(f"Got snapshot for {symbol}: {snapshot_data}")
                return snapshot_data
            
            self.logger.error(f"Failed to get snapshot data: {data_snap}")
            return None

        except Exception as e:
            self.logger.error(f"Error getting quote: {str(e)}")
            return None

    def place_order(self, 
                   code: str,
                   price: float,
                   qty: int,
                   trd_side: TrdSide) -> Optional[Dict[str, Any]]:
        """Place a trading order"""
        try:
            ret, data = self.trade_ctx.place_order(
                price=price,
                qty=qty,
                code=code,
                trd_side=trd_side,
                order_type=OrderType.NORMAL,
                trd_env=TrdEnv.SIMULATE
            )
            
            if ret == RET_OK:
                self.logger.debug(f"Order placed: {data}")
                return data
            self.logger.error(f"Failed to place order: {data}")
            return None
        except Exception as e:
            self.logger.error(f"Error placing order: {str(e)}")
            return None

    def get_market_state(self, codes: list) -> Optional[Dict[str, Any]]:
        """Get market state for given stock codes"""
        try:
            ret, data = self.quote_ctx.get_market_state(codes)
            if ret == RET_OK:
                return data
            self.logger.error(f"Failed to get market state: {data}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting market state: {str(e)}")
            return None

    def query_account_info(self, currency: Currency = Currency.USD) -> Optional[List[Any]]:
        """
        Queries the account information for the specified currency.

        Args:
            currency (Currency): The currency for which to query account info. Defaults to Currency.USD.

        Returns:
            list: A list of purchasing power values.

        Raises:
            Exception: If the account information query fails.
        """
        try:
            ret, data = self.trade_ctx.accinfo_query(currency=currency)
            if ret == RET_OK:
                print(data)
                print(data['power'][0])  # 取第一行的购买力
                return data['power'].values.tolist()  # 转为 list
            else:
                print('accinfo_query error:', data)
                raise Exception(f'accinfo_query error: {data}')
        except Exception as e:
            self.logger.error(f"Error querying account info: {str(e)}")
            return None

if __name__ == "__main__":
    r = MooMooAPI()
    
    try:
        # Test market state
        print("\nTesting market state:")
        state = r.get_market_state(['HK.00700'])
        print(state)
        
        # Test stock quote
        print("\nTesting stock quote:")
        quote = r.get_stock_quote('HK.00700')
        if quote:
            print(f"Last Price: {quote.get('last_price', 'N/A')}")
            print(f"Open Price: {quote.get('open_price', 'N/A')}")
            print(f"High Price: {quote.get('high_price', 'N/A')}")
            print(f"Low Price: {quote.get('low_price', 'N/A')}")
            print(f"Volume: {quote.get('volume', 'N/A')}")
        else:
            print("No quote data available")

        # Test place order
        print("\nTesting place order:")
        order = r.place_order('HK.00700', 100, 100, TrdSide.BUY)
        print(order)

        # Test query account info
        print("\nTesting query account info:")
        info = r.query_account_info(Currency.USD)
        print(info)
    
    finally:
        r.cleanup()

    