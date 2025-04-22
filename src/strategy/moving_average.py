import pandas as pd
import numpy as np
from typing import List, Dict, Any

class MovingAverageCrossover:
    def __init__(self, short_window: int = 5, long_window: int = 20):
        """
        Initialize the moving average crossover strategy
        
        Args:
            short_window: The window for the short-term moving average (default: 5)
            long_window: The window for the long-term moving average (default: 20)
        """
        self.short_window = short_window
        self.long_window = long_window
    
    def calculate_signals(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate trading signals based on moving average crossover
        
        Args:
            data: List of dictionaries containing stock data with columns:
                 datetime, open, high, low, close, volume, instrument
                 
        Returns:
            Dict containing:
                signals: List of trade signals with entry/exit points
                total_returns: Cumulative returns from the strategy
                sharpe_ratio: Sharpe ratio of the strategy returns
                max_drawdown: Maximum drawdown experienced during the period
        """
        # Validate input data
        if not data or len(data) == 0:
            return {"error": "No data provided"}
        
        if len(data) < self.long_window:
            return {
                "error": f"Insufficient data. Need at least {self.long_window} data points."
            }
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        
        # Make sure datetime is in the right format
        if 'datetime' in df.columns:
            if isinstance(df['datetime'].iloc[0], str):
                df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Sort by datetime
        df = df.sort_values('datetime')
        
        # Calculate moving averages
        df['short_ma'] = df['close'].rolling(window=self.short_window).mean()
        df['long_ma'] = df['close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        df['signal'] = 0.0
        df['signal'][self.short_window:] = np.where(
            df['short_ma'][self.short_window:] > df['long_ma'][self.short_window:], 1.0, 0.0
        )
        
        # Generate trading orders
        df['position'] = df['signal'].diff()
        
        # Calculate strategy returns
        df['returns'] = df['close'].pct_change() * df['signal'].shift(1)
        df['cumulative_returns'] = (1 + df['returns']).cumprod()
        
        # Calculate metrics
        total_return = df['cumulative_returns'].iloc[-1] - 1 if not df['cumulative_returns'].empty else 0
        
        # Calculate Sharpe ratio (annualized)
        sharpe_ratio = 0
        if len(df) > 1:
            sharpe_ratio = df['returns'].mean() / df['returns'].std() * np.sqrt(252) if df['returns'].std() > 0 else 0
        
        # Calculate maximum drawdown
        df['drawdown'] = 1 - df['cumulative_returns'] / df['cumulative_returns'].cummax()
        max_drawdown = df['drawdown'].max()
        
        # Prepare signals for response
        signals = []
        for idx, row in df[df['position'] != 0].iterrows():
            signal_type = "BUY" if row['position'] > 0 else "SELL"
            signals.append({
                "datetime": row['datetime'].isoformat(),
                "price": float(row['close']),
                "type": signal_type
            })
        
        return {
            "signals": signals,
            "total_returns": float(total_return),
            "sharpe_ratio": float(sharpe_ratio),
            "max_drawdown": float(max_drawdown)
        }