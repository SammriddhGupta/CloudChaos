import unittest
import boto3
import json
import time


class LambdaIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3_client = boto3.client(
            "s3",
            region_name="ap-southeast-2",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        cls.lambda_client = boto3.client(
            "lambda",
            region_name="ap-southeast-2",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        cls.bucket_name = "seng3011-student"
        cls.folder = "SE3011-24-F11A-04"
        cls.collection_lambda_arn = "arn:aws:lambda:ap-southeast-2:381491885579:function:SE3011-24-F11A-04_collection"
        cls.preprocessing_1_lambda_arn = "arn:aws:lambda:ap-southeast-2:381491885579:function:SE3011-24-F11A-04_dev_preprocessing"
        cls.preprocessing_2_lambda_arn = "arn:aws:lambda:ap-southeast-2:381491885579:function:SE3011-24-F11A-04_dev_preprocessing-2"
        cls.preprocessing_final_lambda_arn = "arn:aws:lambda:ap-southeast-2:381491885579:function:SE3011-24-F11A-04_dev_preprocessing-final"
        cls.retrieval_lambda_arn = "arn:aws:lambda:ap-southeast-2:381491885579:function:SE3011-24-F11A-04_dev_retrieval"

    def test_collection_and_preprocessing1_flow(self):
        # Test data
        test_symbol = "GOOG"
        test_start_date = "2022-01-01"
        test_end_date = "2022-01-10"

        # File names
        collection_output_filename = (
            f"{test_symbol}-{test_start_date}-{test_end_date}.json"
        )
        preprocessing_output_filename = (
            f"P1-{test_symbol}-{test_start_date}-{test_end_date}.json"
        )

        # Trigger data collection Lambda
        self.lambda_client.invoke(
            FunctionName=self.collection_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "queryStringParameters": {
                        "symbol": test_symbol,
                        "start_date": test_start_date,
                        "end_date": test_end_date,
                    }
                }
            ),
        )
        # Wait for collection Lambda to process
        time.sleep(10)

        # Check if the file is in S3 after collection
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=f"{self.folder}/{collection_output_filename}",
            )
            data = json.loads(response["Body"].read().decode("utf-8"))
            self.assertTrue(isinstance(data, dict))  # Basic check for data format
        except self.s3_client.exceptions.NoSuchKey:
            self.fail(
                f"File {collection_output_filename} was not found in S3 bucket after collection."
            )

        # Trigger preprocessing-1 Lambda
        self.lambda_client.invoke(
            FunctionName=self.preprocessing_1_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "queryStringParameters": {
                        "symbol": test_symbol,
                        "start_date": test_start_date,
                        "end_date": test_end_date,
                    }
                }
            ),
        )
        # Wait for preprocessing Lambda to process
        time.sleep(10)

        # Check if the processed file is in S3 after preprocessing-1
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=f"{self.folder}/{preprocessing_output_filename}",
            )
            data = json.loads(response["Body"].read().decode("utf-8"))
            self.assertTrue(
                isinstance(data, dict)
            )  # Basic check for processed data format
        except self.s3_client.exceptions.NoSuchKey:
            self.fail(
                f"Processed file {preprocessing_output_filename} was not found in S3 bucket after preprocessing-1."
            )

    def test_collection_and_preprocessing2_flow(self):
        # Test data
        test_symbol = "NVDA"
        test_start_date = "2022-01-01"
        test_end_date = "2022-01-10"

        # File names
        collection_output_filename = (
            f"{test_symbol}-{test_start_date}-{test_end_date}.json"
        )
        preprocessing_2_output_filename = (
            f"P2-{test_symbol}-{test_start_date}-{test_end_date}.json"
        )

        # Trigger data collection Lambda
        self.lambda_client.invoke(
            FunctionName=self.collection_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "queryStringParameters": {
                        "symbol": test_symbol,
                        "start_date": test_start_date,
                        "end_date": test_end_date,
                    }
                }
            ),
        )
        # Wait for collection Lambda to process
        time.sleep(10)

        # Check if the file is in S3 after collection
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=f"{self.folder}/{collection_output_filename}",
            )
            data = json.loads(response["Body"].read().decode("utf-8"))
            self.assertTrue(isinstance(data, dict))  # Basic check for data format
        except self.s3_client.exceptions.NoSuchKey:
            self.fail(
                f"File {collection_output_filename} was not found in S3 bucket after collection."
            )

        # Trigger preprocessing-2 Lambda
        self.lambda_client.invoke(
            FunctionName=self.preprocessing_2_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "queryStringParameters": {
                        "symbol": test_symbol,
                        "start_date": test_start_date,
                        "end_date": test_end_date,
                    }
                }
            ),
        )
        # Wait for preprocessing Lambda to process
        time.sleep(10)

        # Check if the processed file is in S3 after preprocessing-2
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=f"{self.folder}/{preprocessing_2_output_filename}",
            )
            data = json.loads(response["Body"].read().decode("utf-8"))
            self.assertTrue(
                isinstance(data, dict)
            )  # Basic check for processed data format
        except self.s3_client.exceptions.NoSuchKey:
            self.fail(
                f"Processed file {preprocessing_2_output_filename} was not found in S3 bucket after preprocessing-2."
            )

    def test_collection_and_preprocessingfinal_flow(self):
        # Test data
        test_symbol = "SHEL"
        test_start_date = "2022-01-01"
        test_end_date = "2022-01-10"

        # File names
        collection_output_filename = (
            f"{test_symbol}-{test_start_date}-{test_end_date}.json"
        )
        preprocessing_final_output_filename = (
            f"FP-{test_symbol}-{test_start_date}-{test_end_date}.json"
        )

        # Trigger data collection Lambda
        self.lambda_client.invoke(
            FunctionName=self.collection_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "queryStringParameters": {
                        "symbol": test_symbol,
                        "start_date": test_start_date,
                        "end_date": test_end_date,
                    }
                }
            ),
        )
        # Wait for collection Lambda to process
        time.sleep(10)

        # Check if the file is in S3 after collection
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=f"{self.folder}/{collection_output_filename}",
            )
            data = json.loads(response["Body"].read().decode("utf-8"))
            self.assertTrue(isinstance(data, dict))  # Basic check for data format
        except self.s3_client.exceptions.NoSuchKey:
            self.fail(
                f"File {collection_output_filename} was not found in S3 bucket after collection."
            )

        # Trigger preprocessing-final Lambda
        self.lambda_client.invoke(
            FunctionName=self.preprocessing_final_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "queryStringParameters": {
                        "symbol": test_symbol,
                        "start_date": test_start_date,
                        "end_date": test_end_date,
                    }
                }
            ),
        )
        # Wait for preprocessing Lambda to process
        time.sleep(10)

        # Check if the processed file is in S3 after preprocessing-final
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=f"{self.folder}/{preprocessing_final_output_filename}",
            )
            data = json.loads(response["Body"].read().decode("utf-8"))
            self.assertTrue(
                isinstance(data, dict)
            )  # Basic check for processed data format
        except self.s3_client.exceptions.NoSuchKey:
            self.fail(
                f"Processed file {preprocessing_final_output_filename} was not found in S3 bucket after preprocessing-final."
            )

    def test_collection_retrieval_preprocessingfinal_flow(self):
        # Test data and file names
        test_symbol = "META"
        test_start_date = "2022-01-01"
        test_end_date = "2022-01-10"
        collection_output_filename = (
            f"{test_symbol}-{test_start_date}-{test_end_date}.json"
        )
        preprocessing_final_output_filename = (
            f"FP-{test_symbol}-{test_start_date}-{test_end_date}.json"
        )

        # Step 1: Trigger data collection Lambda
        self.lambda_client.invoke(
            FunctionName=self.collection_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "queryStringParameters": {
                        "symbol": test_symbol,
                        "start_date": test_start_date,
                        "end_date": test_end_date,
                    }
                }
            ),
        )
        time.sleep(10)  # Wait for collection Lambda to process

        # Step 2: Retrieve and assert the collected data
        self.retrieve_and_assert(
            test_symbol,
            test_start_date,
            test_end_date,
            "collection",
            collection_output_filename,
        )

        # Step 3: Trigger preprocessing-final Lambda
        self.lambda_client.invoke(
            FunctionName=self.preprocessing_final_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "queryStringParameters": {
                        "symbol": test_symbol,
                        "start_date": test_start_date,
                        "end_date": test_end_date,
                    }
                }
            ),
        )
        time.sleep(10)  # Wait for preprocessing-final Lambda to process

        # Step 4: Retrieve and assert the preprocessed data
        self.retrieve_and_assert(
            test_symbol,
            test_start_date,
            test_end_date,
            "preprocessing-final",
            preprocessing_final_output_filename,
        )

    def retrieve_and_assert(
        self, symbol, start_date, end_date, file_type, expected_filename
    ):
        # Invoke the retrieval Lambda
        response = self.lambda_client.invoke(
            FunctionName=self.retrieval_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "queryStringParameters": {
                        "file": file_type,
                        "symbol": symbol,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                }
            ),
        )

        # Parse and check the response
        response_payload = json.loads(response["Payload"].read().decode("utf-8"))
        self.assertEqual(
            response_payload.get("statusCode"),
            200,
            "Retrieval Lambda did not return status 200",
        )
        self.assertIn(
            "body", response_payload, "Retrieval response does not contain a body"
        )

        # Extract the body from the response and parse it as JSON
        retrieved_data = response_payload["body"]
        print("Retrieved raw data:", retrieved_data)
        retrieved_data_json = json.loads(retrieved_data)
        print("Parsed JSON data:", retrieved_data_json)

        # Validate specific fields in the response
        self.assertIn(
            "data_source",
            retrieved_data_json,
            "Retrieved data does not contain 'data_source'",
        )
        self.assertIn(
            "events", retrieved_data_json, "Retrieved data does not contain 'events'"
        )


if __name__ == "__main__":
    unittest.main()
