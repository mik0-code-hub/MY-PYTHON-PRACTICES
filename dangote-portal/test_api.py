import unittest
from fastapi.testclient import TestClient
from main import app

class TestDangotePortalAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")

    def test_stocks(self):
        res = self.client.get("/api/stocks")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("DANGCEM", data)
        self.assertIn("DANGSUGAR", data)
        self.assertIn("NASCON", data)

    def test_businesses(self):
        res = self.client.get("/api/businesses")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 6)
        # Check refinery details
        refinery = next((b for b in data if b["id"] == "refinery"), None)
        self.assertIsNotNone(refinery)
        self.assertIn("650,000", refinery["capacity"])

    def test_countries(self):
        res = self.client.get("/api/countries")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 10)

    def test_news(self):
        res = self.client.get("/api/news")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 5)

    def test_careers(self):
        res = self.client.get("/api/careers")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 5)

    def test_contact_submission(self):
        payload = {
            "fullName": "Chinedu Okafor",
            "email": "chinedu@example.com",
            "phone": "+2348031234567",
            "inquiryType": "Procurement / Vendor Registration",
            "subsidiary": "Dangote Petroleum Refinery",
            "subject": "Supply Chain Partnerships",
            "message": "We would like to register as an industrial consumables supplier."
        }
        res = self.client.post("/api/contact", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertIn("referenceNumber", data)

    def test_calculator(self):
        payload = {
            "subsidiary": "DANGCEM",
            "sharesCount": 1000,
            "purchasePrice": 450.00
        }
        res = self.client.post("/api/calculator", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["sharesHeld"], 1000)
        self.assertGreater(data["annualDividendIncome"], 0)

if __name__ == "__main__":
    unittest.main()
