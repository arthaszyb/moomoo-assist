from dataclasses import dataclass

@dataclass
class Stock:
    """
    Represents a stock with relevant attributes.
    """
    symbol: str
    name: str
    current_price: float
    pe_ratio: float
    pb_ratio: float
    revenue_growth: float
    profit_growth: float
    industry: str 