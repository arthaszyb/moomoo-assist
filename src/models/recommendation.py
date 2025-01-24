# Data models for recommendations can be defined here
class Recommendation:
    def __init__(self, symbol: str, recommendation: str, reasoning: str = ""):
        self.symbol = symbol
        self.recommendation = recommendation
        self.reasoning = reasoning
