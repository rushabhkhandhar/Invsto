import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_api():
    print("===== Testing Trading Strategy API =====")
    
    # Test data endpoint - get all data
    print("\n1. Testing GET /data/ endpoint...")
    response = requests.get(f"{BASE_URL}/data/")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Retrieved {len(data)} records")
        if len(data) > 0:
            print(f"Sample record: {json.dumps(data[0], indent=2)}")
    else:
        print(f"❌ Error! Status code: {response.status_code}")
        print(response.text)
    
    # Test data endpoint - filter by instrument
    print("\n2. Testing GET /data/?instrument=HINDALCO endpoint...")
    response = requests.get(f"{BASE_URL}/data/?instrument=HINDALCO&limit=5")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Retrieved {len(data)} HINDALCO records")
    else:
        print(f"❌ Error! Status code: {response.status_code}")
    
    # Test strategy endpoint - default parameters
    print("\n3. Testing GET /strategy/performance endpoint...")
    response = requests.get(f"{BASE_URL}/strategy/performance?instrument=HINDALCO")
    if response.status_code == 200:
        strategy = response.json()
        print(f"✅ Success! Strategy performance calculated")
        print(f"Total returns: {strategy['total_returns']:.2%}")
        print(f"Number of signals: {len(strategy['signals'])}")
        print(f"Sharpe ratio: {strategy.get('sharpe_ratio', 'N/A')}")
        print(f"Max drawdown: {strategy.get('max_drawdown', 'N/A')}")
    else:
        print(f"❌ Error! Status code: {response.status_code}")
        print(response.text)
    
    # Test strategy endpoint - custom parameters
    print("\n4. Testing GET /strategy/performance with custom parameters...")
    response = requests.get(f"{BASE_URL}/strategy/performance?instrument=HINDALCO&short_window=10&long_window=30")
    if response.status_code == 200:
        strategy = response.json()
        print(f"✅ Success! Strategy performance calculated with custom parameters")
        print(f"Total returns: {strategy['total_returns']:.2%}")
        print(f"Number of signals: {len(strategy['signals'])}")
    else:
        print(f"❌ Error! Status code: {response.status_code}")
    
    print("\n===== Testing Complete =====")

if __name__ == "__main__":
    test_api()