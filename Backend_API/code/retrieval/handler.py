import json
import os
from datetime import datetime
import boto3
import urllib3

AWS_ACCESS_KEY_ID = os.getenv('MY_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('MY_AWS_SECRET_ACCESS_KEY')

class DataRetrievalAPI:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.bucket_name = "seng3011-student"
        self.folder = "SE3011-24-F11A-04"

    def valid_date_format(self, date):
        if date is None:
            return False
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def retrieve_data(self, file, symbol, start_date, end_date):
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }

        current_date = datetime.now().strftime("%Y-%m-%d")

        # Check for None values before comparing dates
        if (start_date and start_date > current_date) or (
            end_date and end_date > current_date
        ):
            return {"statusCode": 400, "body": "Future dates are not allowed"}

        # Validate date formats
        if not self.valid_date_format(start_date) or not self.valid_date_format(
            end_date
        ):
            return {"statusCode": 400, "body": "Invalid date format"}

        # Validate that start_date is before end_date
        if datetime.strptime(start_date, "%Y-%m-%d") >= datetime.strptime(
            end_date, "%Y-%m-%d"
        ):
            return {"statusCode": 400, "body": "Start date must be before end date"}

        if not file or not symbol:
            return {"statusCode": 400, "body": "Invalid parameters"}
        if file not in [
            "collection",
            "preprocessing-1",
            "preprocessing-2",
            "preprocessing-final",
        ]:
            return {"statusCode": 400, "body": "Unsupported file type"}
        if not self.valid_date_format(start_date) or not self.valid_date_format(
            end_date
        ):
            return {"statusCode": 400, "body": "Invalid date format"}
        filename = symbol + "-" + start_date + "-" + end_date + ".json"
        try:
            s3_response_object = self.s3.get_object(
                Bucket=self.bucket_name, Key=self.folder + "/" + filename
            )
            data = s3_response_object["Body"].read().decode("utf-8")
            if file == "collection":
                return {"statusCode": 200, "headers": headers, "body": json.dumps(data)}
            elif file == "preprocessing-1":
                filename = "P1-" + filename
            elif file == "preprocessing-2":
                filename = "P2-" + filename
            elif file == "preprocessing-final":
                filename = "FP-" + filename
            try:
                s3_response_object = self.s3.get_object(
                    Bucket=self.bucket_name, Key=self.folder + "/" + filename
                )
                data = s3_response_object["Body"].read().decode("utf-8")
                return {"statusCode": 200, "headers": headers, "body": json.dumps(data)}
            except:
                if file == "preprocessing-1":
                    return self.invoke_preprocessing_1(symbol, start_date, end_date)
                elif file == "preprocessing-2":
                    return self.invoke_preprocessing_2(symbol, start_date, end_date)
                elif file == "preprocessing-final":
                    return self.invoke_preprocessing_final(symbol, start_date, end_date)
        except:
            if file == "collection":
                return self.invoke_data_collection(symbol, start_date, end_date)
            elif file == "preprocessing-1":
                self.invoke_data_collection(symbol, start_date, end_date)
                return self.invoke_preprocessing_1(symbol, start_date, end_date)
            elif file == "preprocessing-2":
                self.invoke_data_collection(symbol, start_date, end_date)
                return self.invoke_preprocessing_2(symbol, start_date, end_date)
            elif file == "preprocessing-final":
                self.invoke_data_collection(symbol, start_date, end_date)
                return self.invoke_preprocessing_final(symbol, start_date, end_date)

    def invoke_data_collection(self, symbol, start_date, end_date):
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }

        url = "https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04_collection"
        url += (
            "?symbol=" + symbol + "&start_date=" + start_date + "&end_date=" + end_date
        )
        response = self.http.request("GET", url)
        response_data = response.data.decode("utf-8")
        if response.status == 200:
            filename = symbol + "-" + start_date + "-" + end_date + ".json"
            s3_response_object = self.s3.get_object(
                Bucket=self.bucket_name, Key=self.folder + "/" + filename
            )
            data = s3_response_object["Body"].read().decode("utf-8")
            return {"statusCode": 200, "headers": headers, "body": json.dumps(data)}
        else:
            print(response.status, response.text)
            return {"statusCode": response.status, "body": response_data}

    def invoke_preprocessing_1(self, symbol, start_date, end_date):
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }

        url = "https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04/preprocess-1"
        url += (
            "?symbol=" + symbol + "&start_date=" + start_date + "&end_date=" + end_date
        )
        try:
            response = self.http.request("GET", url)
            if response.status != 200:
                return {
                    "statusCode": response.status,
                    "body": json.dumps({"error": "External API Error"}),
                }
            filename = "P1-" + symbol + "-" + start_date + "-" + end_date + ".json"
            s3_response_object = self.s3.get_object(
                Bucket=self.bucket_name, Key=self.folder + "/" + filename
            )
            data = s3_response_object["Body"].read().decode("utf-8")
            return {"statusCode": 200, "headers": headers, "body": json.dumps(data)}
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    def invoke_preprocessing_2(self, symbol, start_date, end_date):
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }

        url = "https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04/preprocess-2"
        url += (
            "?symbol=" + symbol + "&start_date=" + start_date + "&end_date=" + end_date
        )
        try:
            response = self.http.request("GET", url)
            if response.status != 200:
                return {
                    "statusCode": response.status,
                    "body": json.dumps({"error": "External API Error"}),
                }
            filename = "P2-" + symbol + "-" + start_date + "-" + end_date + ".json"
            s3_response_object = self.s3.get_object(
                Bucket=self.bucket_name, Key=self.folder + "/" + filename
            )
            data = s3_response_object["Body"].read().decode("utf-8")
            return {"statusCode": 200, "headers": headers, "body": json.dumps(data)}
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    def invoke_preprocessing_final(self, symbol, start_date, end_date):
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }

        url = "https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04/preprocess-final"
        url += (
            "?symbol=" + symbol + "&start_date=" + start_date + "&end_date=" + end_date
        )
        try:
            response = self.http.request("GET", url)
            if response.status != 200:
                return {
                    "statusCode": response.status,
                    "body": json.dumps({"error": "External API Error"}),
                }
            filename = "FP-" + symbol + "-" + start_date + "-" + end_date + ".json"
            s3_response_object = self.s3.get_object(
                Bucket=self.bucket_name, Key=self.folder + "/" + filename
            )
            data = s3_response_object["Body"].read().decode("utf-8")
            return {"statusCode": 200, "headers": headers, "body": json.dumps(data)}
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def lambda_handler(event, context):
    # Extract parameters from the event payload
    payload = event["queryStringParameters"]
    symbol = payload.get("symbol")  # MSFT
    start_date = payload.get("start_date")  # YYYY-MM-DD
    end_date = payload.get("end_date")  # YYYY-MM-DD
    file = payload.get(
        "file", "collection"
    )  # collection, preprocessing-1, preprocessing-2, preprocessing-final

    # Check if file parameter is valid (collection, preprocessing-1, preprocessing-2, preprocessing-final)
    if file not in [
        "collection",
        "preprocessing-1",
        "preprocessing-2",
        "preprocessing-final",
    ]:
        return {
            "statusCode": 400,
            "body": "The file parameter should be one of the following: collection, preprocessing-1, preprocessing-2, preprocessing-final.",
        }

    # Check if parameters are provided
    if not symbol or not start_date or not end_date:
        print("The parameters symbol, start_date, and end_date are required.")
        return {
            "statusCode": 400,
            "body": "The parameters symbol, start_date, and end_date are required.",
        }

    # Check if start and end date are in the correct format (YYYY-MM-DD)
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except:
        return {
            "statusCode": 400,
            "body": "The parameters start_date and end_date should be in the format YYYY-MM-DD.",
        }

    # Check if start date and end date is not a future date
    if start_date > datetime.now().strftime(
        "%Y-%m-%d"
    ) or end_date > datetime.now().strftime("%Y-%m-%d"):
        return {
            "statusCode": 400,
            "body": "The parameters start_date and end_date should not be future dates.",
        }

    # Check if start date is before end date
    if start_date >= end_date:
        print("Start date must be before end date.")
        return {"statusCode": 400, "body": "Start date must be before end date."}

    # Create an instance of DataRetrievalAPI and retrieve data with parameters
    api = DataRetrievalAPI()
    return api.retrieve_data(file, symbol, start_date, end_date)
