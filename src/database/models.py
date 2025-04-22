from sqlalchemy import Column, Integer, Numeric, String, DateTime
from . import Base  # Import Base from __init__.py

class StockData(Base):
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    open = Column(Numeric, nullable=False)
    high = Column(Numeric, nullable=False)
    low = Column(Numeric, nullable=False)
    close = Column(Numeric, nullable=False)
    volume = Column(Integer, nullable=False)
    instrument = Column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "datetime": self.datetime.isoformat(),
            "open": float(self.open),
            "high": float(self.high),
            "low": float(self.low),
            "close": float(self.close),
            "volume": self.volume,
            "instrument": self.instrument
        }