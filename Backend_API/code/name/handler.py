import yfinance as yf

def lambda_handler(event, context):
    payload = event["queryStringParameters"]
    symbol = payload.get("symbol")

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    stock = yf.Ticker(symbol)
    name = stock.info["longName"]

    return {"statusCode": 200, "headers": headers, "body": name}
