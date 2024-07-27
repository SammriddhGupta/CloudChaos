import unittest
import urllib3
import json
from urllib.parse import urlencode


class TestRetrievalAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = urllib3.PoolManager()
        cls.api_url = "https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04/retrieve"
        cls.symbol = "AAPL"
        cls.valid_start_date = "2017-01-01"
        cls.valid_end_date = "2017-01-31"
        cls.future_date = "2025-01-01"
        cls.file_type = "collection"

    def send_request(self, payload):
        try:
            url = "https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04/retrieve"
            encoded_args = urlencode(payload)
            full_url = url + "?" + encoded_args
            response = self.http.request("GET", full_url)

            print("Response:", response.status, response.data)  # Debug print

            response_body = response.data.decode("utf-8")
            if response_body:
                return {"statusCode": response.status, "body": response_body}
            else:
                return {"statusCode": response.status, "error": "No response data"}
        except Exception as e:
            print("Exception:", e)  # Debug print
            return {"error": str(e)}

    def test_retrieval_consistency(self):
        payload = {
            "symbol": self.symbol,
            "start_date": self.valid_start_date,
            "end_date": self.valid_end_date,
            "file": self.file_type,
        }
        response1 = self.send_request(payload)
        response2 = self.send_request(payload)
        self.assertEqual(
            response1, response2, "Data is not consistent across retrievals."
        )

    def test_invalid_parameters(self):
        payload = {
            "symbol": "",
            "start_date": self.valid_start_date,
            "end_date": self.valid_end_date,
            "file": self.file_type,
        }
        response = self.send_request(payload)

        self.assertIn(
            "statusCode", response, "Response should contain a statusCode key"
        )
        if "statusCode" in response:
            self.assertEqual(
                response["statusCode"],
                400,
                "Invalid parameters should result in a 400 error.",
            )
        else:
            self.fail("Response missing statusCode")

    def test_future_date(self):
        payload = {
            "symbol": self.symbol,
            "start_date": self.future_date,
            "end_date": self.future_date,
            "file": self.file_type,
        }
        response = self.send_request(payload)
        self.assertEqual(
            response.get("statusCode"),
            400,
            "Future dates should result in a 400 error.",
        )

    def test_start_date_after_end_date(self):
        payload = {
            "symbol": self.symbol,
            "start_date": self.valid_end_date,
            "end_date": self.valid_start_date,
            "file": self.file_type,
        }
        response = self.send_request(payload)
        self.assertEqual(
            response.get("statusCode"),
            400,
            "Start date after end date should result in a 400 error.",
        )

    def test_unsupported_file_type(self):
        payload = {
            "symbol": self.symbol,
            "start_date": self.valid_start_date,
            "end_date": self.valid_end_date,
            "file": "unknown_type",
        }
        response = self.send_request(payload)
        self.assertEqual(
            response.get("statusCode"),
            400,
            "Unsupported file type should result in a 400 error.",
        )


if __name__ == "__main__":
    unittest.main()
