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

                # calculating average daily price as the average of open, high, low, and close prices
                current_event["average_daily_price"] = (
                    current_event["open"]
                    + current_event["high"]
                    + current_event["low"]
                    + current_event["close"]
                ) / 4

                # calculating price range
                current_event["price_range"] = (
                    current_event["high"] - current_event["low"]
                )

                # calculating moving averages for 7, 14, and 30 days
                closing_prices = [event["close"] for event in data["events"][: i + 1]]
                for period in [7, 14, 30]:
                    if len(closing_prices) >= period:
                        moving_average = sum(closing_prices[-period:]) / period
                        current_event[f"moving_average_{period}_days"] = moving_average

            jsonfile = json.dumps(data)
            filename = f"P2-{symbol}-{start}-{end}.json"

            self.store_data(jsonfile, filename)

            return json.dumps(data)

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
        "body": json.dumps("Data preprocessing 2 completed successfully!"),
    }
