from pydantic import BaseModel
from datetime import datetime

class StockData(BaseModel):
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

class StockDataCreate(BaseModel):
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int