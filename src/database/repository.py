from sqlalchemy import create_engine, Column, Integer, Numeric, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os
from typing import List, Optional

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, index=True)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    volume = Column(Integer)
    instrument = Column(String, default='UNKNOWN')

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

class StockDataRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self, instrument: Optional[str] = None) -> List[dict]:
        """Fetch all stock data records, optionally filtered by instrument"""
        query = self.db.query(StockData)
        if instrument:
            query = query.filter(StockData.instrument == instrument)
        
        records = query.order_by(StockData.datetime).all()
        
        # Convert ORM objects to dictionaries
        result = []
        for record in records:
            result.append({
                "id": record.id,
                "datetime": record.datetime.isoformat(),
                "open": float(record.open),
                "high": float(record.high),
                "low": float(record.low),
                "close": float(record.close),
                "volume": record.volume,
                "instrument": record.instrument
            })
        
        return result

    def create(self, stock_data_dict: dict) -> StockData:
        """Create a new stock data record"""
        stock_data = StockData(
            datetime=stock_data_dict["datetime"],
            open=stock_data_dict["open"],
            high=stock_data_dict["high"],
            low=stock_data_dict["low"],
            close=stock_data_dict["close"],
            volume=stock_data_dict["volume"],
            instrument=stock_data_dict["instrument"]
        )
        self.db.add(stock_data)
        self.db.commit()
        self.db.refresh(stock_data)
        return stock_data

    def create_many(self, stock_data_list: List[dict]) -> List[StockData]:
        """Create multiple stock data records"""
        stock_data_objects = [
            StockData(
                datetime=item["datetime"],
                open=item["open"],
                high=item["high"],
                low=item["low"],
                close=item["close"],
                volume=item["volume"],
                instrument=item["instrument"]
            )
            for item in stock_data_list
        ]
        self.db.add_all(stock_data_objects)
        self.db.commit()
        for obj in stock_data_objects:
            self.db.refresh(obj)
        return stock_data_objects

# Functions for endpoints
async def fetch_all_records(db: Session) -> List[dict]:
    """Fetch all stock data records from the database"""
    repo = StockDataRepository(db)
    records = repo.get_all()
    return [record.to_dict() for record in records]

async def insert_record(stock_data_dict: dict, db: Session) -> dict:
    """Insert a single stock data record into the database"""
    repo = StockDataRepository(db)
    record = repo.create(stock_data_dict)
    return record.to_dict()