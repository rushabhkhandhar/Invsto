import unittest
from pydantic import ValidationError
from src.api.models.stock_data import StockData

class TestDataValidation(unittest.TestCase):

    def test_valid_data(self):
        data = {
            "datetime": "2014-01-24 00:00:00",
            "open": 113.15,
            "high": 115.35,
            "low": 113.00,
            "close": 114.00,
            "volume": 5737135
        }
        stock_data = StockData(**data)
        self.assertEqual(stock_data.datetime, "2014-01-24 00:00:00")
        self.assertEqual(stock_data.open, 113.15)
        self.assertEqual(stock_data.high, 115.35)
        self.assertEqual(stock_data.low, 113.00)
        self.assertEqual(stock_data.close, 114.00)
        self.assertEqual(stock_data.volume, 5737135)

    def test_invalid_datetime(self):
        data = {
            "datetime": "invalid-date",
            "open": 113.15,
            "high": 115.35,
            "low": 113.00,
            "close": 114.00,
            "volume": 5737135
        }
        with self.assertRaises(ValidationError):
            StockData(**data)

    def test_invalid_open(self):
        data = {
            "datetime": "2014-01-24 00:00:00",
            "open": "invalid-open",
            "high": 115.35,
            "low": 113.00,
            "close": 114.00,
            "volume": 5737135
        }
        with self.assertRaises(ValidationError):
            StockData(**data)

    def test_invalid_volume(self):
        data = {
            "datetime": "2014-01-24 00:00:00",
            "open": 113.15,
            "high": 115.35,
            "low": 113.00,
            "close": 114.00,
            "volume": "invalid-volume"
        }
        with self.assertRaises(ValidationError):
            StockData(**data)

if __name__ == '__main__':
    unittest.main()