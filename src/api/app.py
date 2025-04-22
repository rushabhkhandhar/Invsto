from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Fix the import paths - use relative imports
from .endpoints import data, strategy
from ..database import initialize_db

# Add these imports
import logging
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title="Trading Strategy API",
    description="API for stock data and trading strategy analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(strategy.router, prefix="/strategy", tags=["strategy"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Trading Strategy API"}

@app.on_event("startup")
async def startup_event():
    # Initialize the database on startup
    initialize_db()

# Add these handlers to your app
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )