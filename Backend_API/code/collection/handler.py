import json
import os
import boto3
import datetime
from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf

AWS_ACCESS_KEY_ID = os.getenv('MY_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('MY_AWS_SECRET_ACCESS_KEY')

yf.pdr_override()

class DataCollectionAPI:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.bucket_name = "seng3011-student"
        self.folder = "SE3011-24-F11A-04"

    def collect_data(self, symbol, start, end):
        data = pdr.get_data_yahoo(symbol, start=start, end=end)

        # Fill NaN values with 0 using the recommended method
        data.fillna({"Dividends": 0}, inplace=True)
        data.fillna({"Stock Splits": 0}, inplace=True)

        # Convert the index to a DatetimeIndex
        data.index = pd.to_datetime(data.index)

        # Remove timezone information from index to prevent AttributeError
        data.index = data.index.tz_localize(None)

        # Get current timestamp and timezone
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timezone = datetime.datetime.now().astimezone().tzinfo

        jsonfile_ohlc = {
            "data_source": "Yahoo Finance",
            "dataset_type": "Stock Price from " + start + " to " + end,
            "dataset_id": "http://seng3011-student.ap-southeast-2.amazonaws.com",
            "time_object": {"timestamp": timestamp, "timezone": str(timezone)},
            "events": [],
        }
        for index, row in data.iterrows():
            jsonfile_ohlc["events"].append(
                {
                    "type": "stock_price",
                    "timestamp": index.strftime("%Y-%m-%d"),
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": row["Volume"],
                }
            )
        jsonfile = json.dumps(jsonfile_ohlc)
        filename = symbol + "-" + start + "-" + end + ".json"
        self.store_data(jsonfile, filename)

    def store_data(self, jsonfile, filename):
        response = self.s3.put_object(
            Bucket=self.bucket_name, Key=self.folder + "/" + filename, Body=jsonfile
        )

        # Retrieve the status code from the response
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]

        # Check if the upload was successful
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("File uploaded successfully!")
        else:
            raise Exception(f"Failed to upload file, status code {status_code}")


def lambda_handler(event, context):
    payload = event["queryStringParameters"]
    symbol = payload["symbol"]
    start_date = payload["start_date"]
    end_date = payload["end_date"]

    # Create an instance of DataCollectionAPI and collect data with parameters
    api = DataCollectionAPI()
    api.collect_data(symbol, start_date, end_date)

    return {
        "statusCode": 200,
        "body": json.dumps("Data collection completed successfully!"),
    }
