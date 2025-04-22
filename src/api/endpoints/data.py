from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ...database import get_db
from ...database.models import StockData as DbStockData

router = APIRouter()

class StockData(BaseModel):
    datetime: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    instrument: str = "UNKNOWN"

    class Config:
        orm_mode = True

@router.get("/", response_model=List[StockData])
async def get_data(
    limit: int = Query(100, description="Maximum number of records to return"),
    instrument: Optional[str] = Query(None, description="Filter by instrument symbol"),
    db: Session = Depends(get_db)
):
    """Fetch stock data records with optional filtering"""
    try:
        # Start with base query
        query = db.query(DbStockData)
        
        # Apply filter if instrument is provided
        if instrument:
            query = query.filter(DbStockData.instrument == instrument)
        
        # Apply limit and get results
        records = query.order_by(DbStockData.datetime).limit(limit).all()
        
        # Convert to response model format
        result = []
        for record in records:
            result.append(
                StockData(
                    datetime=record.datetime.isoformat(),
                    open=float(record.open),
                    high=float(record.high),
                    low=float(record.low),
                    close=float(record.close),
                    volume=record.volume,
                    instrument=record.instrument
                )
            )
            
        return result
    except Exception as e:
        # Log the exception
        import logging
        logging.error(f"Error fetching data: {str(e)}")
        
        # Raise HTTP exception
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@router.post("/", status_code=201)
async def add_data(stock_data: StockData, db: Session = Depends(get_db)):
    """Add a new stock data record"""
    try:
        # Convert string datetime to datetime object
        dt = datetime.fromisoformat(stock_data.datetime)
        
        # Create new record
        new_record = DbStockData(
            datetime=dt,
            open=stock_data.open,
            high=stock_data.high,
            low=stock_data.low,
            close=stock_data.close,
            volume=stock_data.volume,
            instrument=stock_data.instrument
        )
        
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        return {"message": "Record added successfully", "data": new_record.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding record: {str(e)}")