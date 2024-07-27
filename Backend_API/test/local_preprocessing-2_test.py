import os
import sys
import unittest
import json
import botocore.exceptions
from unittest.mock import MagicMock, patch

# Adjust the path for correct imports in the test directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from code.preprocessing2.preprocessing2_handler import (
    DataPreprocessingAPI,
    lambda_handler,
)


class TestDataPreprocessing2API(unittest.TestCase):
    def setUp(self):
        self.api = DataPreprocessingAPI()
        self.mock_s3 = MagicMock()
        self.api.s3 = self.mock_s3

        # Mock S3 response for get_object (assuming successful retrieval)
        # This should match the key format used in preprocess_data
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(
                read=MagicMock(
                    return_value=b'{"events": [{"timestamp": "2017-01-01", "close": 100}]}'
                )
            )
        }

        # Mock S3 response for successful put_object
        self.mock_s3.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

    def test_lambda_handler(self):
        # Mock S3 get_object for the test case
        test_s3_key = "AAPL-2017-01-01-2017-04-30.json"
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(
                read=MagicMock(
                    return_value=b'{"events": [{"timestamp": "2017-01-01", "close": 100}]}'
                )
            )
        }

        event = {
            "queryStringParameters": {
                "symbol": "AAPL",
                "start_date": "2017-01-01",
                "end_date": "2017-04-30",
            }
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            json.loads(response["body"]), "Data preprocessing 2 completed successfully!"
        )

    def test_preprocess_data(self):
        # Mock S3 response for get_object
        # This should match the key format used in preprocess_data
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(
                read=MagicMock(
                    return_value=b'{"events": [{"timestamp": "2017-01-01", "close": 100}]}'
                )
            )
        }

        # Mock S3 response for successful put_object
        self.mock_s3.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

        result = self.api.preprocess_data("AAPL", "2017-01-01", "2017-04-30")

        # Check if the S3 get_object was called once with the correct parameters
        self.mock_s3.get_object.assert_called_once_with(
            Bucket="seng3011-student",
            Key="SE3011-24-F11A-04/AAPL-2017-01-01-2017-04-30.json",
        )

        # Check if the S3 put_object was called once with the correct parameters
        expected_filename = "P2-AAPL-2017-01-01-2017-04-30.json"
        self.mock_s3.put_object.assert_called_once()

        # Check the processed data is as expected
        expected_data = {"events": [{"timestamp": "2017-01-01", "close": 100}]}
        self.assertEqual(result, json.dumps(expected_data))

    def test_store_data_success(self):
        # Mock S3 response for successful put_object
        self.mock_s3.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }
        self.api.store_data(json.dumps({"test": "data"}), "test.json")
        self.mock_s3.put_object.assert_called_once()

    def test_store_data_failure(self):
        # Simulate a failure response from S3 put_object method
        self.mock_s3.put_object.side_effect = botocore.exceptions.ClientError(
            {"Error": {"Code": "500", "Message": "Internal Server Error"}},
            operation_name="PutObject",
        )
        with self.assertRaises(Exception):  # Expecting a general exception
            self.api.store_data(json.dumps({"test": "data"}), "test.json")

    def test_preprocess_data_failure(self):
        self.mock_s3.get_object.side_effect = botocore.exceptions.ClientError(
            {
                "ResponseMetadata": {"HTTPStatusCode": 404},
                "Error": {"Code": "NoSuchKey", "Message": "Not Found"},
            },
            operation_name="GetObject",
        )
        with self.assertRaises(FileNotFoundError):
            self.api.preprocess_data("AAPL", "2017-01-01", "2017-04-30")


if __name__ == "__main__":
    unittest.main()
