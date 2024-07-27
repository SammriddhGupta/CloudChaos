import os
import sys
import unittest
import json
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from io import BytesIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from code.retrieval.handler import DataRetrievalAPI, lambda_handler


class TestDataRetrievalAPI(unittest.TestCase):
    def setUp(self):
        self.api = DataRetrievalAPI()
        self.mock_s3 = MagicMock()
        self.api.s3 = self.mock_s3

        self.mock_http_request_patch = patch(
            "code.retrieval.handler.urllib3.PoolManager.request"
        )
        self.mock_http_request = self.mock_http_request_patch.start()

    def tearDown(self):
        patch.stopall()

    def test_unexpected_file_type(self):
        response = self.api.retrieve_data(
            "unexpected-type", "AAPL", "2017-01-01", "2017-04-30"
        )
        self.assertNotEqual(response["statusCode"], 200)

    def test_invalid_s3_bucket_or_key(self):
        self.mock_s3.get_object.side_effect = Exception("NoSuchBucket or NoSuchKey")

        response_mock = MagicMock()
        response_mock.status = 404
        response_mock.data = json.dumps(
            {"error": "S3 service error"}
        ).encode()  # Encode to bytes
        self.mock_http_request.return_value = response_mock

        # Invoke the method under test
        response = self.api.retrieve_data(
            "collection", "AAPL", "2017-01-01", "2017-04-30"
        )

        self.assertNotEqual(response["statusCode"], 200)

    def test_invalid_input_parameters(self):
        # Testing with various invalid inputs
        responses = [
            self.api.retrieve_data(None, "AAPL", "2017-01-01", "2017-04-30"),
            self.api.retrieve_data("collection", None, "2017-01-01", "2017-04-30"),
            self.api.retrieve_data("collection", "AAPL", None, "2017-04-30"),
            self.api.retrieve_data("collection", "AAPL", "2017-01-01", None),
        ]
        for response in responses:
            self.assertNotEqual(response["statusCode"], 200)

    def test_boundary_date_conditions(self):
        # Mock S3 get_object response
        self.mock_s3.get_object.return_value = {
            "Body": BytesIO(b'{"data": "boundary data"}')
        }

        # Assuming 'boundary_date' is not in the future
        boundary_date = "2023-01-01"  # Adjust to a date that is not in the future

        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.text = json.dumps({"data": "mocked data"})

        with patch("requests.get", return_value=response_mock):
            response = self.api.retrieve_data(
                "collection", "AAPL", boundary_date, "2023-01-02"
            )

        self.assertEqual(response["statusCode"], 200)

    def test_invalid_permissions(self):
        # Simulating permission error
        self.mock_s3.get_object.side_effect = Exception("AccessDenied")

        response_mock = MagicMock()
        response_mock.status = 403
        response_mock.data = json.dumps(
            {"error": "Access denied"}
        ).encode()  # Encode to bytes
        self.mock_http_request.return_value = response_mock

        response = self.api.retrieve_data(
            "collection", "AAPL", "2017-01-01", "2017-04-30"
        )

        self.assertNotEqual(response["statusCode"], 200)

    def test_future_date_inputs(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.api.retrieve_data(
            "collection", "AAPL", future_date, future_date
        )
        self.assertNotEqual(response["statusCode"], 200)  # Expecting an error code

    def test_start_date_after_end_date(self):
        self.mock_s3.get_object.return_value = {
            "Body": BytesIO(b'{"data": "mocked data"}')
        }

        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.text = json.dumps({"data": "mocked data"})

        with patch("requests.get", return_value=response_mock):
            response = self.api.retrieve_data(
                "collection", "AAPL", "2024-01-02", "2024-01-01"
            )

        self.assertNotEqual(response["statusCode"], 200)

    def test_date_format_validation(self):
        invalid_date = "2024/01/01"  # Invalid format
        response = self.api.retrieve_data(
            "collection", "AAPL", invalid_date, invalid_date
        )
        self.assertNotEqual(response["statusCode"], 200)

    def test_api_call_failures(self):
        response_mock = MagicMock()
        response_mock.status_code = 404
        response_mock.text = json.dumps({"error": "Not found"})

        with patch("requests.get", return_value=response_mock):
            response = self.api.invoke_data_collection(
                "AAPL", "2024-01-01", "2024-01-02"
            )

        self.assertNotEqual(response["statusCode"], 200)

    def test_different_file_types(self):
        response = self.api.retrieve_data(
            "invalid-type", "AAPL", "2024-01-01", "2024-01-02"
        )
        self.assertNotEqual(response["statusCode"], 200)

    def test_s3_bucket_access_issues(self):
        self.mock_s3.get_object.side_effect = Exception("S3 Access Error")

        response_mock = MagicMock()
        response_mock.status_code = 404  # Example error code
        response_mock.text = json.dumps({"error": "S3 service error"})

        with patch("requests.get", return_value=response_mock):
            response = self.api.retrieve_data(
                "collection", "AAPL", "2024-01-01", "2024-01-02"
            )

        self.assertNotEqual(response["statusCode"], 200)

    def test_retrieve_data_exception_handling(self):
        self.mock_s3.get_object.side_effect = Exception("S3 Error")

        response_mock = MagicMock()
        response_mock.status_code = 404
        response_mock.text = json.dumps({"error": "External API Error"})

        with patch("requests.get", return_value=response_mock):
            response = self.api.retrieve_data(
                "collection", "AAPL", "2024-01-01", "2024-01-02"
            )

        self.assertNotEqual(response["statusCode"], 200)

    def test_retrieve_data_collection(self):
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=b'{"data": "example"}'))
        }

        response = self.api.retrieve_data(
            "collection", "AAPL", "2017-01-01", "2017-04-30"
        )

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("data", json.loads(response["body"]))

    def test_retrieve_data_preprocessing_1_success(self):
        # Test successful retrieval for preprocessing-1
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=b'{"preprocessed": "data"}'))
        }
        response = self.api.retrieve_data(
            "preprocessing-1", "AAPL", "2017-01-01", "2017-04-30"
        )
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("preprocessed", json.loads(response["body"]))

    def test_retrieve_data_preprocessing_2_success(self):
        # Test successful retrieval for preprocessing-2
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=b'{"preprocessed": "data"}'))
        }
        response = self.api.retrieve_data(
            "preprocessing-2", "AAPL", "2017-01-01", "2017-04-30"
        )
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("preprocessed", json.loads(response["body"]))

    def test_retrieve_data_preprocessing_final_success(self):
        # Test successful retrieval for preprocessing-final
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=b'{"preprocessed": "data"}'))
        }
        response = self.api.retrieve_data(
            "preprocessing-final", "AAPL", "2017-01-01", "2017-04-30"
        )
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("preprocessed", json.loads(response["body"]))

    def test_retrieve_data_with_api_call_failure(self):
        # Test API call failure handling
        response_mock = MagicMock()
        response_mock.status = 404  # Using 404 status code
        response_mock.data = json.dumps(
            {"error": "Not found"}
        ).encode()  # Encode to bytes
        self.mock_http_request.return_value = response_mock

        response = self.api.retrieve_data(
            "collection", "AAPL", "2017-01-01", "2017-04-30"
        )

        self.assertNotEqual(response["statusCode"], 200)

    def test_retrieve_data_s3_exception(self):
        self.mock_s3.get_object.side_effect = Exception("S3 error")

        response_mock = MagicMock()
        response_mock.status = 404  # Using 404 status code
        response_mock.data = json.dumps(
            {"error": "S3 service error"}
        ).encode()  # Encode to bytes
        self.mock_http_request.return_value = response_mock

        response = self.api.retrieve_data(
            "collection", "AAPL", "2017-01-01", "2017-04-30"
        )

        # Assert that the status code is not 200 (indicating an error)
        self.assertNotEqual(response["statusCode"], 200)

    def test_retrieve_data_invalid_parameters(self):
        # Test invalid parameters handling
        response = self.api.retrieve_data("", "AAPL", "2017-01-01", "2017-04-30")
        self.assertNotEqual(response["statusCode"], 200)

        # Test handling of empty symbol parameter
        response = self.api.retrieve_data("collection", "", "2017-01-01", "2017-04-30")
        self.assertNotEqual(response["statusCode"], 200)

    def test_retrieve_data_invalid_date_format(self):
        # Test invalid date format handling
        response = self.api.retrieve_data(
            "collection", "AAPL", "01-01-2017", "2017-04-30"
        )
        self.assertNotEqual(response["statusCode"], 200)

        response = self.api.retrieve_data(
            "collection", "AAPL", "2017-01-01", "30-04-2017"
        )
        self.assertNotEqual(response["statusCode"], 200)

    def test_invoke_preprocessing_1_success(self):
        self.mock_s3.get_object.return_value = {
            "Body": BytesIO(b'{"preprocessed": "data"}')
        }

        response_mock = MagicMock()
        response_mock.status = 200  # HTTP status code
        response_mock.data = json.dumps(
            {"preprocessed": "data"}
        ).encode()  # Encode to bytes
        self.mock_http_request.return_value = response_mock

        response = self.api.invoke_preprocessing_1("AAPL", "2017-01-01", "2017-04-30")

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("preprocessed", json.loads(response["body"]))

    def test_invoke_preprocessing_2_success(self):
        self.mock_s3.get_object.return_value = {
            "Body": BytesIO(b'{"preprocessed": "data"}')
        }

        response_mock = MagicMock()
        response_mock.status = 200  # HTTP status code
        response_mock.data = json.dumps(
            {"preprocessed": "data"}
        ).encode()  # Encode to bytes
        self.mock_http_request.return_value = response_mock

        response = self.api.invoke_preprocessing_2("AAPL", "2017-01-01", "2017-04-30")

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("preprocessed", json.loads(response["body"]))

    def test_invoke_preprocessing_final_success(self):
        self.mock_s3.get_object.return_value = {
            "Body": BytesIO(b'{"preprocessed": "data"}')
        }

        response_mock = MagicMock()
        response_mock.status = 200  # HTTP status code
        response_mock.data = json.dumps(
            {"preprocessed": "data"}
        ).encode()  # Encode to bytes
        self.mock_http_request.return_value = response_mock

        response = self.api.invoke_preprocessing_final(
            "AAPL", "2017-01-01", "2017-04-30"
        )

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("preprocessed", json.loads(response["body"]))

    def test_invoke_preprocessing_1_failure(self):
        response_mock = MagicMock()
        response_mock.status_code = 500
        response_mock.text = json.dumps(
            {"error": "Internal Server Error"}
        )  # Mock response as JSON string

        with patch("requests.get", return_value=response_mock):
            response = self.api.invoke_preprocessing_1(
                "AAPL", "2017-01-01", "2017-04-30"
            )

        self.assertNotEqual(response["statusCode"], 200)

    def test_invoke_preprocessing_2_failure(self):
        response_mock = MagicMock()
        response_mock.status_code = 500
        response_mock.text = json.dumps(
            {"error": "Internal Server Error"}
        )  # Mock response as JSON string

        with patch("requests.get", return_value=response_mock):
            response = self.api.invoke_preprocessing_2(
                "AAPL", "2017-01-01", "2017-04-30"
            )

        self.assertNotEqual(response["statusCode"], 200)

    def test_invoke_preprocessing_final_failure(self):
        response_mock = MagicMock()
        response_mock.status_code = 500
        response_mock.text = json.dumps(
            {"error": "Internal Server Error"}
        )  # Mock response as JSON string

        with patch("requests.get", return_value=response_mock):
            response = self.api.invoke_preprocessing_final(
                "AAPL", "2017-01-01", "2017-04-30"
            )

        self.assertNotEqual(response["statusCode"], 200)

    def test_lambda_handler_invalid_parameters(self):
        event = {
            "queryStringParameters": {"symbol": "AAPL", "start_date": "2024-01-01"}
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)

    def test_invoke_preprocessing_1_exception(self):
        self.mock_http_request.side_effect = Exception("Request failed")
        response = self.api.invoke_preprocessing_1("AAPL", "2017-01-01", "2017-04-30")
        self.assertNotEqual(response["statusCode"], 200)

    def test_invoke_preprocessing_2_exception(self):
        self.mock_http_request.side_effect = Exception("Request failed")
        response = self.api.invoke_preprocessing_2("AAPL", "2017-01-01", "2017-04-30")
        self.assertNotEqual(response["statusCode"], 200)

    def test_invoke_preprocessing_final_exception(self):
        self.mock_http_request.side_effect = Exception("Request failed")
        response = self.api.invoke_preprocessing_final(
            "AAPL", "2017-01-01", "2017-04-30"
        )
        self.assertNotEqual(response["statusCode"], 200)

    def test_preprocessing_1_successful_s3_response(self):
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=b'{"preprocessed": "data"}'))
        }

        response_mock = MagicMock()
        response_mock.status = 200
        response_mock.data = json.dumps({"some": "data"}).encode()
        self.mock_http_request.return_value = response_mock

        response = self.api.invoke_preprocessing_1("AAPL", "2017-01-01", "2017-04-30")

        # Assertions for successful retrieval
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("preprocessed", json.loads(response["body"]))

    def test_preprocessing_2_successful_s3_response(self):
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=b'{"preprocessed": "data"}'))
        }

        response_mock = MagicMock()
        response_mock.status = 200
        response_mock.data = json.dumps({"some": "data"}).encode()
        self.mock_http_request.return_value = response_mock

        response = self.api.invoke_preprocessing_2("AAPL", "2017-01-01", "2017-04-30")

        # Assertions for successful retrieval
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("preprocessed", json.loads(response["body"]))

    def test_preprocessing_final_successful_s3_response(self):
        self.mock_s3.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=b'{"preprocessed": "data"}'))
        }

        response_mock = MagicMock()
        response_mock.status = 200
        response_mock.data = json.dumps({"some": "data"}).encode()
        self.mock_http_request.return_value = response_mock

        response = self.api.invoke_preprocessing_final(
            "AAPL", "2017-01-01", "2017-04-30"
        )

        # Assertions for successful retrieval
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("preprocessed", json.loads(response["body"]))

    def test_invoke_data_collection_non_200_status(self):
        # Simulating a non-200 response from the external API
        response_mock = MagicMock()
        response_mock.status = 500
        response_mock.data = json.dumps({"error": "Server error"}).encode()
        self.mock_http_request.return_value = response_mock

        response = self.api.invoke_data_collection("AAPL", "2017-01-01", "2017-04-30")

        self.assertNotEqual(response["statusCode"], 200)
        self.assertIn("Server error", response["body"])

    def test_invoke_preprocessing_1_api_call_exception(self):
        self.mock_http_request.side_effect = Exception("API call failed")

        response = self.api.invoke_preprocessing_1("AAPL", "2017-01-01", "2017-04-30")

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("API call failed", response["body"])

    def test_invoke_preprocessing_2_api_call_exception(self):
        self.mock_http_request.side_effect = Exception("API call failed")

        response = self.api.invoke_preprocessing_2("AAPL", "2017-01-01", "2017-04-30")

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("API call failed", response["body"])

    def test_invoke_preprocessing_final_api_call_exception(self):
        self.mock_http_request.side_effect = Exception("API call failed")

        response = self.api.invoke_preprocessing_final(
            "AAPL", "2017-01-01", "2017-04-30"
        )

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("API call failed", response["body"])

    def test_retrieve_data_with_malformed_date_format(self):
        # Testing with a malformed date format
        response = self.api.retrieve_data(
            "collection", "AAPL", "2017/01/01", "2017-04-30"
        )

        # Assert that the status code indicates an error
        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Invalid date format", response["body"])

    def test_s3_permission_exception(self):
        # Simulate S3 permission exception
        self.mock_s3.get_object.side_effect = Exception("Access Denied")

        response_mock = MagicMock()
        response_mock.status = 500
        response_mock.data = json.dumps({"error": "S3 Access Denied"}).encode()
        self.mock_http_request.return_value = response_mock

        response = self.api.retrieve_data(
            "collection", "AAPL", "2017-01-01", "2017-04-30"
        )

        # Assert that the status code indicates an error and contains the "Access Denied" message
        self.assertNotEqual(response["statusCode"], 200)
        self.assertIn("Access Denied", response["body"])

    def test_retrieve_data_empty_symbol(self):
        # Testing with an empty symbol
        response = self.api.retrieve_data("collection", "", "2017-01-01", "2017-04-30")

        # Assert that the status code indicates an error
        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Invalid parameters", response["body"])

    def test_lambda_handler_invalid_date_format(self):
        event = {
            "queryStringParameters": {
                "symbol": "AAPL",
                "start_date": "01-01-2017",
                "end_date": "2017-04-30",
            }
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)
        self.assertIn(
            "The parameters start_date and end_date should be in the format YYYY-MM-DD",
            response["body"],
        )

    def test_successful_s3_response(self):
        mock_s3_response = {
            "Body": MagicMock(read=MagicMock(return_value=b'{"data": "example"}'))
        }
        self.mock_s3.get_object.return_value = mock_s3_response

        response = self.api.retrieve_data(
            "collection", "AAPL", "2017-01-01", "2017-04-30"
        )

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])  # Parse the JSON string
        self.assertIn("data", body)
        body = json.loads(response["body"])
        data = json.loads(body)
        self.assertIn("example", data["data"])

    def test_future_dates(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        event = {
            "queryStringParameters": {
                "symbol": "AAPL",
                "start_date": future_date,
                "end_date": "2023-01-01",
            }
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)
        self.assertIn(
            "The parameters start_date and end_date should not be future dates",
            response["body"],
        )

    def test_start_date_after_end_date(self):
        event = {
            "queryStringParameters": {
                "symbol": "AAPL",
                "start_date": "2023-01-02",
                "end_date": "2023-01-01",
            }
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Start date must be before end date", response["body"])

    def test_valid_data_retrieval(self):
        valid_symbol = "AAPL"
        valid_start_date = "2023-01-01"
        valid_end_date = "2023-01-10"

        event = {
            "queryStringParameters": {
                "symbol": valid_symbol,
                "start_date": valid_start_date,
                "end_date": valid_end_date,
                "file": "collection",
            }
        }

        with patch("code.retrieval.handler.DataRetrievalAPI") as mock_api:
            mock_instance = mock_api.return_value
            mock_instance.retrieve_data.return_value = {
                "statusCode": 200,
                "body": "some mock response",
            }

            response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        mock_instance.retrieve_data.assert_called_once_with(
            "collection", valid_symbol, valid_start_date, valid_end_date
        )

    def test_retrieve_data_successful_s3_fetch(self):
        # Mock parameters
        symbol = "AAPL"
        start_date = "2023-01-01"
        end_date = "2023-01-10"
        file = "collection"
        filename = f"{symbol}-{start_date}-{end_date}.json"
        bucket_name = "seng3011-student"
        folder = "SE3011-24-F11A-04"

        # Mock S3 response
        mock_s3_response = {
            "Body": MagicMock(
                read=MagicMock(return_value=b'{"data": "mocked response"}')
            )
        }

        # Patch boto3 S3 client
        with patch("boto3.client") as mock_boto3_client:
            mock_s3 = mock_boto3_client.return_value
            mock_s3.get_object.return_value = mock_s3_response

            api = DataRetrievalAPI()
            response = api.retrieve_data(file, symbol, start_date, end_date)
            body_str = json.loads(response["body"])  # This will be a string, not a dict
            body_dict = json.loads(body_str)  # Decode again to get the dict

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("mocked response", body_dict["data"])
        mock_s3.get_object.assert_called_with(
            Bucket=bucket_name, Key=f"{folder}/{filename}"
        )


if __name__ == "__main__":
    unittest.main()
