import json
import os
import boto3
import logging
import botocore.exceptions

AWS_ACCESS_KEY_ID = os.getenv('MY_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('MY_AWS_SECRET_ACCESS_KEY')

class DataPreprocessingAPI:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.bucket_name = "seng3011-student"
        self.folder = "SE3011-24-F11A-04"
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
        return logger

    def store_data(self, jsonfile, filename):
        try:
            response = self.s3.put_object(
                Bucket=self.bucket_name, Key=self.folder + "/" + filename, Body=jsonfile
            )
            http_status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if http_status_code == 200:
                self.logger.info(f"File '{filename}' uploaded successfully!")
            else:
                self.logger.error(
                    f"Failed to upload file '{filename}' to S3. HTTP Status Code: {http_status_code}"
                )

        # In store_data method:
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(
                    f"File {filename} not found in S3 bucket. Data needs to be collected first!"
                ) from e
            else:
                raise

    def preprocess_data(self, symbol, start, end):
        s3_key = f"{symbol}-{start}-{end}.json"

        try:
            # now retrieving data from S3
            response = self.s3.get_object(
                Bucket=self.bucket_name, Key=self.folder + "/" + s3_key
            )
            data = json.loads(response["Body"].read().decode("utf-8"))

            # Sort events by timestamp to ensure sequential processing
            data["events"] = sorted(data["events"], key=lambda x: x["timestamp"])

            for i in range(1, len(data["events"])):
                current_event = data["events"][i]
                prev_event = data["events"][i - 1]

                # Ensure both current and previous events have "close" prices
                if "close" not in current_event and "close" not in prev_event:
                    current_event["daily_return"] = None
                    continue

                close_price = current_event["close"]
                prev_close_price = prev_event["close"]

                # Calculate daily percentage change
                if prev_close_price != 0:
                    daily_return = (
                        (close_price - prev_close_price) / prev_close_price * 100.0
                    )
                else:
                    daily_return = None

                # Add the daily percentage change to the current event
                current_event["daily_return"] = daily_return

            jsonfile = json.dumps(data)
            filename = f"P1-{symbol}-{start}-{end}.json"

            self.store_data(jsonfile, filename)

            return json.dumps(data)

        # In preprocess_data method:
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(
                    f"File {s3_key} not found in S3 bucket. Data needs to be collected first!"
                ) from e
            else:
                raise


def lambda_handler(event, context):
    # Extract parameters from the event payload
    payload = event["queryStringParameters"]
    symbol = payload.get("symbol")  # MSFT
    start_date = payload.get("start_date")  # YYYY-MM-DD
    end_date = payload.get("end_date")  # YYYY-MM-DD

    # Create an instance of DataPreprocessingAPI and preprocess data with parameters
    api = DataPreprocessingAPI()
    api.preprocess_data(symbol, start_date, end_date)

    return {
        "statusCode": 200,
        "body": json.dumps("Data preprocessing completed successfully!"),
    }
