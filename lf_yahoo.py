# import yfinance as yf
import json
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import time

def get_price(stock, data_type, **kwargs):
    base_url = f"http://52.206.155.70:8080/price/{stock}"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('meme_stock_history')
    response = table.get_item(
        Key={
            'rid': 'stock_tickers'
        }
    )
    print(response)
    stocks = []
    for each in response['Item']['tickers']:
        stocks.append(each)
    print(stocks)
    
    all_data = []
    _start, _end = 10,12
    for stock in stocks[_start: _end]:
        
    
        stock = stock.lower() #'tsla'.lower()
        d = get_price(stock, '')
        d['body']['price_date'] = eval(d['body']['price_date'])
        
        print(stock)
        print(d['body']['price_date'])
        
        for _close in [ i for i in reversed(sorted(d['body']['price_date']))][:5]:
            
            date = str(_close)[:10]
            print(f'{stock}_{date}')
            response = table.get_item(
                Key={
                    'rid': f'{stock}_{date}'
                }
            )
            data = None
            print(date)
            print(stock)
            print(d['body']['price_date'][_close])
            print(response)
            # print(len(response['Items']))
            if 'Item' not in response:
                data = {
                        'rid': f"{stock}_{date}".lower(),
                        'stock': stock,
                        'date': date,
                        'records': {
                            'comment': []
                        },
                        'sentiments': [],
                        'v': 0,
                        'price':{
                            'close': d['body']['price_date'][_close],
                           
                        }
                    }
                print(data)
                
            else:
                
                data = response['Item']
                data['price'] = {
                        'close': d['body']['price_date'][_close]
                    }
                data['v'] += 1
                data['v'] = float(data['v'])
                        
       
                        
                    
        
            for i in range(len(data['records']['comment'])):
                data['records']['comment'][i]['score'] = float(data['records']['comment'][i]['score'])
            for i in range(len(data['sentiments'])):
                for j in range(len(data['sentiments'][i]['scores'])):
                    data['sentiments'][i]['scores'][j] = float(data['sentiments'][i]['scores'][j])
            data['price']['close'] = float(data['price']['close'])
            
            
                
            response = table.put_item(
                Item = json.loads(json.dumps(data), parse_float=Decimal)
            )
            
            # print(response)
            time.sleep(3)
            

    return {
        'status': 200,
        'body': 'Success'
    }
