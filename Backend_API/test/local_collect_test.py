import sys
import os
import unittest
import json
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from code.collection.handler import DataCollectionAPI, lambda_handler


class LocalCollectTest(unittest.TestCase):
    @patch("code.collection.handler.boto3.client")
    def test_lambda_handler(self, mock_boto3_client):
        mock_s3 = mock_boto3_client.return_value
        mock_s3.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        event = {
            "queryStringParameters": {
                "symbol": "AAPL",
                "start_date": "2022-01-01",
                "end_date": "2022-04-30",
            }
        }
        response = lambda_handler(event, None)
        response_body = json.loads(response["body"])

        self.assertEqual(response_body, "Data collection completed successfully!")
        self.assertEqual(response["statusCode"], 200)
        mock_s3.put_object.assert_called_once()

    @patch("code.collection.handler.boto3.client")
    def test_collect_data_successful(self, mock_boto3_client):
        mock_s3 = mock_boto3_client.return_value
        mock_s3.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        api = DataCollectionAPI()
        api.collect_data("AAPL", "2022-01-01", "2022-04-30")

        mock_s3.put_object.assert_called_once()

    @patch("code.collection.handler.pdr.get_data_yahoo")
    @patch("code.collection.handler.boto3.client")
    def test_collect_data_failure(self, mock_boto3_client, mock_get_data_yahoo):
        # Simulating a failure in fetching data
        mock_get_data_yahoo.side_effect = Exception("Failed to fetch data")

        api = DataCollectionAPI()

        # If an exception should be raised, then assertRaises is correct.
        with self.assertRaises(Exception):
            api.collect_data("INVALID", "2022-01-01", "2022-04-30")

    @patch("code.collection.handler.boto3.client")
    def test_store_data_failure(self, mock_boto3_client):
        mock_s3 = mock_boto3_client.return_value
        mock_s3.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 400}}

        api = DataCollectionAPI()
        json_data = json.dumps({"test": "data"})
        filename = "test.json"

        # Assertion for an exception should pass
        with self.assertRaises(Exception):
            api.store_data(json_data, filename)


if __name__ == "__main__":
    unittest.main()
