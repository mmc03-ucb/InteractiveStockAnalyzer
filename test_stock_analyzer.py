import unittest
from trading_strategy import (
    StockAnalyzer,
)


class TestStockAnalyzer(unittest.TestCase):
    def setUp(self):
        # Setup that is run before each test
        self.analyzer = StockAnalyzer("AAPL", "2020-01-01", "2020-12-31")

    def test_fetch_data(self):
        """Test if data is fetched correctly."""
        self.analyzer.fetch_data()
        self.assertIsNotNone(self.analyzer.data)
        self.assertFalse(self.analyzer.data.empty)

    def test_calculate_technical_indicators(self):
        """Test the calculation of technical indicators."""
        self.analyzer.fetch_data()
        self.analyzer.calculate_technical_indicators()
        self.assertIn("RSI", self.analyzer.data.columns)
        self.assertIn("Bollinger_High", self.analyzer.data.columns)
        self.assertIn("Bollinger_Low", self.analyzer.data.columns)


if __name__ == "__main__":
    unittest.main()
