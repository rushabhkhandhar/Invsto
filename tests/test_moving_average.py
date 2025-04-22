import unittest
from src.strategy.moving_average import calculate_moving_average, generate_signals

class TestMovingAverage(unittest.TestCase):

    def setUp(self):
        self.data = [
            {'datetime': '2014-01-24 00:00:00', 'close': 114},
            {'datetime': '2014-01-25 00:00:00', 'close': 115},
            {'datetime': '2014-01-26 00:00:00', 'close': 116},
            {'datetime': '2014-01-27 00:00:00', 'close': 117},
            {'datetime': '2014-01-28 00:00:00', 'close': 118},
            {'datetime': '2014-01-29 00:00:00', 'close': 119},
            {'datetime': '2014-01-30 00:00:00', 'close': 120},
        ]

    def test_calculate_moving_average(self):
        short_term = 3
        long_term = 5
        short_ma = calculate_moving_average(self.data, short_term)
        long_ma = calculate_moving_average(self.data, long_term)

        self.assertEqual(short_ma[-1], 118)  # Last short-term MA
        self.assertEqual(long_ma[-1], 116)   # Last long-term MA

    def test_generate_signals(self):
        short_term = 3
        long_term = 5
        signals = generate_signals(self.data, short_term, long_term)

        self.assertEqual(signals[0], 'hold')  # Initial signal
        self.assertEqual(signals[1], 'buy')    # First crossover signal
        self.assertEqual(signals[-1], 'sell')  # Last crossover signal

if __name__ == '__main__':
    unittest.main()