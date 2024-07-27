import yfinance as yf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from scipy import stats
import datetime
from datetime import timedelta
import json
import os

AWS_ACCESS_KEY_ID = os.getenv('MY_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('MY_AWS_SECRET_ACCESS_KEY')

# Function to fetch historical stock data
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function to preprocess data and split into features and target
def preprocess_data(data):
    data["Date"] = data.index
    data["Date"] = data["Date"].astype(str)
    data["Date"] = data["Date"].str.replace("-", "")
    data["Date"] = data["Date"].astype(int)
    X = data[["Date"]].values
    y = data["Close"].values
    return X, y

# Function to train a linear regression model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    return regressor, X_test, y_test

# Function to make predictions
def make_predictions(regressor, X_test):
    y_pred = regressor.predict(X_test)
    return y_pred

# Function to convert integer date to proper date format
def convert_to_date(date_int):
    date_str = str(date_int)
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:])
    return datetime.date(year, month, day)

# Function to make predictions with confidence intervals
def make_predictions_with_intervals(regressor, X, y_pred):
    n = X.shape[0]
    dof = n - regressor.coef_.shape[0] - 1
    confidence = 0.95
    t_value = np.abs(stats.t.ppf((1 - confidence) / 2, dof))
    margin_of_error = t_value * np.sqrt(
        mean_squared_error(y_pred, y_pred)
        * (1 / n + (X - X.mean()) ** 2 / np.sum((X - X.mean()) ** 2))
    )
    lower_bound = y_pred - margin_of_error
    upper_bound = y_pred + margin_of_error
    return lower_bound, upper_bound

# Main function
def main(ticker="AAPL", start_date="2022-01-01", end_date="2024-04-14"):

    # Fetch stock data
    stock_data = get_stock_data(ticker, start_date, end_date)

    # Preprocess data
    X, y = preprocess_data(stock_data)

    # Train model
    regressor, X_test, y_test = train_model(X, y)

    # Make predictions for historical dates
    y_pred = make_predictions(regressor, X_test)

    print("Historical Data Predictions:")
    print("Date\t\tActual\t\tPredicted\tError")
    results = []
    for i in range(len(y_test)):
        error = abs(y_test[i] - y_pred[i])
        date = convert_to_date(X_test[i][0])
        results.append((date, y_test[i], y_pred[i], error))

    # Sort results based on date
    results.sort(key=lambda x: x[0])

    for result in results:
        print(f"{result[0]}\t{result[1]:.2f}\t\t{result[2]:.2f}\t\t{result[3]:.2f}")

    # Make predictions with confidence intervals for future dates
    startdate = datetime.datetime.today()
    future_dates = []

    # Generate the next 30 days of future dates
    for i in range(30):
        future_date = startdate + timedelta(days=i)
        future_dates.append(int(future_date.strftime("%Y%m%d")))

    future_dates_formatted = np.array(
        [[date] for date in future_dates]
    )  # Convert to NumPy array
    future_predictions = make_predictions(regressor, future_dates_formatted)
    lower_bound, upper_bound = make_predictions_with_intervals(
        regressor, future_dates_formatted, future_predictions
    )

    # Store future predictions in a dictionary
    future_data = {}
    for i in range(len(future_dates)):
        formatted_date = convert_to_date(future_dates[i])
        prediction = future_predictions[i]
        future_data[str(formatted_date)] = prediction

    # Convert future data to JSON
    future_json = json.dumps(future_data, indent=4)

    # Print future predictions
    print("\nFuture Data Predictions with Confidence Intervals:")
    print("Date\t\tPredicted")
    for i in range(len(future_dates)):
        formatted_date = convert_to_date(future_dates[i])
        prediction = future_predictions[i]  # Accessing the value directly
        lower = lower_bound[i][0]  # Accessing the scalar value
        upper = upper_bound[i][0]  # Accessing the scalar value
        print(f"{formatted_date}\t{prediction:.2f}")  # Corrected format here

    # Calculate evaluation metrics for historical data
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # Print evaluation metrics for historical data
    print("\nEvaluation Metrics for Historical Data:")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R-squared: {r2:.2f}")

    # Return future predictions as JSON
    print("\nFuture Predictions:" + future_json)
    return future_json

def lambda_handler(event, context):
    payload = event["queryStringParameters"]
    symbol = payload["symbol"]
    start_date = payload["start_date"]
    end_date = payload["end_date"]
    jsonResponse = main(symbol, start_date, end_date)
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    return {"statusCode": 200, "headers": headers, "body": jsonResponse}
