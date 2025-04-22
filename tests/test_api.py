import unittest
from fastapi.testclient import TestClient
from src.api.app import app

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_data(self):
        response = self.client.get("/data")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_post_data(self):
        new_data = {
            "datetime": "2023-01-01T00:00:00",
            "open": 100.0,
            "high": 110.0,
            "low": 90.0,
            "close": 105.0,
            "volume": 1000
        }
        response = self.client.post("/data", json=new_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_post_data_validation(self):
        invalid_data = {
            "datetime": "invalid_date",
            "open": "not_a_decimal",
            "high": 110.0,
            "low": 90.0,
            "close": 105.0,
            "volume": "not_an_integer"
        }
        response = self.client.post("/data", json=invalid_data)
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()