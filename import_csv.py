import pandas as pd
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import datetime
import psycopg2

# Load environment variables
load_dotenv()

# Get database connection string - use environment variable or fallback
# Inside Docker, we should use 'db' instead of 'localhost'
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/trading_db")

def import_data(file_path):
    # Check file extension
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Read file based on extension
    print(f"Reading file: {file_path}")
    if file_ext == '.csv':
        df = pd.read_csv(file_path)
    elif file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        print(f"Unsupported file format: {file_ext}")
        sys.exit(1)
    
    # Convert datetime strings to datetime objects
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Print data summary
    print(f"Found {len(df)} rows of data")
    print("Sample data:")
    print(df.head())
    
    # Print column information
    print("\nColumn information:")
    for column in df.columns:
        print(f"{column}: {df[column].dtype}")
    
    try:
        # Create database engine
        print(f"Connecting to database at {DATABASE_URL}")
        engine = create_engine(DATABASE_URL)
        
        # Check if connection is successful
        with engine.connect() as conn:
            print("Connected to database successfully")
            
            # Clear existing data
            conn.execute(text("DELETE FROM stock_data"))
            conn.commit()
            print("Cleared existing data")
            
            # Import data to PostgreSQL
            print("Importing data to PostgreSQL...")
            df.to_sql('stock_data', engine, if_exists='append', index=False)
            
            # Verify import
            count = conn.execute(text("SELECT COUNT(*) FROM stock_data")).scalar()
            print(f"Successfully imported {count} rows to the database")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python import_csv.py path/to/your/data.[csv|xlsx]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    import_data(file_path)