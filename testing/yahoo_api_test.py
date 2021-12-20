import yfinance as yf
import json

pip install numpy==1.14.5 --target .

def lambda_handler(event, context):
    amc = yf.Ticker("AMC")
    hist = amc.history(period="1mo")
    print(type(hist))

    return {

    }
