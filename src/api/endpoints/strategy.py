from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from ...database.repository import StockDataRepository
from ...strategy.moving_average import MovingAverageCrossover
from ...database import get_db
from ...config import SHORT_WINDOW, LONG_WINDOW

router = APIRouter()

@router.get("/performance")
async def get_strategy_performance(
    instrument: str = Query(..., description="Instrument symbol to analyze"),
    short_window: int = Query(SHORT_WINDOW, description="Short-term moving average window"),
    long_window: int = Query(LONG_WINDOW, description="Long-term moving average window"),
    db: Session = Depends(get_db)
):
    """
    Calculate and return the performance of the moving average crossover strategy
    for the specified instrument
    """
    try:
        # Fetch data for the instrument
        repo = StockDataRepository(db)
        data = repo.get_all(instrument=instrument)
        
        if not data:
            raise HTTPException(status_code=404, detail=f"No data found for instrument {instrument}")
        
        # Calculate strategy performance
        strategy = MovingAverageCrossover(short_window=short_window, long_window=long_window)
        performance = strategy.calculate_signals(data)
        
        if "error" in performance:
            raise HTTPException(status_code=400, detail=performance["error"])
            
        return performance
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        # Add logging
        import logging
        logger = logging.getLogger("src.api.app")
        logger.error(f"Error calculating strategy: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating strategy: {str(e)}")