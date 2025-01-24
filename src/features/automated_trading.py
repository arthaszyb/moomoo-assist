from api.moomoo_api import MooMooAPI
from api.moomoo_openD import MooMooOpenD
import logging
import threading

class AutomatedTrading:
    """
    Executes automated trading strategies based on user-defined goals and real-time market data.
    """

    def __init__(self, moomoo_api: MooMooAPI, moomoo_openD: MooMooOpenD):
        self.api = moomoo_api
        self.stream = moomoo_openD
        self.logger = logging.getLogger('AutomatedTrading')
        self.active_strategies = []
        self.trade_records = []

    def execute_strategy(self, strategy: dict):
        """
        Executes a trading strategy based on the provided strategy configuration.
        """
        self.logger.info(f"Executing strategy: {strategy['name']}")
        if strategy['type'] == 'BreakoutBuy':
            threading.Thread(target=self.breakout_buy_strategy, args=(strategy,)).start()
        elif strategy['type'] == 'MovingAverageCrossover':
            threading.Thread(target=self.moving_average_crossover_strategy, args=(strategy,)).start()
        else:
            self.logger.error(f"Unknown strategy type: {strategy['type']}")

    def breakout_buy_strategy(self, strategy: dict):
        """
        Implements the Breakout Buy Strategy.
        """
        symbol = strategy['symbol']
        n_days_high = self.api.get_n_days_high(symbol, strategy['n_days'])

        while True:
            real_time_price = self.api.get_real_time_price(symbol)
            if real_time_price > n_days_high:
                order_details = {
                    "symbol": symbol,
                    "quantity": strategy['quantity'],
                    "order_type": "market",
                    "action": "buy"
                }
                order_response = self.api.place_order(order_details)
                if order_response:
                    self.trade_records.append(order_response)
                    self.logger.info(f"Breakout Buy order placed for {symbol}: {order_response}")
                break

    def moving_average_crossover_strategy(self, strategy: dict):
        """
        Implements the Moving Average Crossover Strategy.
        """
        symbol = strategy['symbol']
        short_ma_period = strategy['short_ma']
        long_ma_period = strategy['long_ma']

        short_ma = self.api.get_moving_average(symbol, short_ma_period)
        long_ma = self.api.get_moving_average(symbol, long_ma_period)

        while True:
            real_time_price = self.api.get_real_time_price(symbol)
            new_short_ma = self.api.get_moving_average(symbol, short_ma_period)
            new_long_ma = self.api.get_moving_average(symbol, long_ma_period)

            if new_short_ma > new_long_ma and short_ma <= long_ma:
                order_details = {
                    "symbol": symbol,
                    "quantity": strategy['quantity'],
                    "order_type": "limit",
                    "action": "buy",
                    "limit_price": real_time_price
                }
                order_response = self.api.place_order(order_details)
                if order_response:
                    self.trade_records.append(order_response)
                    self.logger.info(f"Moving Average Crossover order placed for {symbol}: {order_response}")
                break

            short_ma = new_short_ma
            long_ma = new_long_ma

    def monitor_orders(self):
        """
        Monitors the status of placed orders.
        """
        for order in self.trade_records:
            status = self.api.get_order_status(order['order_id'])
            self.logger.debug(f"Order {order['order_id']} status: {status}")
            # Update order records based on status
