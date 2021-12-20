import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import random
import requests
import datetime
from decimal import Decimal

def get_recent_dates(stock='amc'):
    base_url = f"http://52.206.155.70:8080/price/{stock}"
    request = requests.get(base_url)
    response = sorted(eval(request.json()['body']['price_date']).keys())[-5:]
    return response
    

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
    
    recent_5_dates = get_recent_dates()
    
    
    recommend_records = []
    stock_names = []
    
    
    for stock in stocks:
        price_data = []
        senti = []
        stock = stock.lower()
        stock_names.append(stock.upper())
        for _date in recent_5_dates:
            response = table.get_item(
                Key={
                    'rid': f'{stock}_{_date}'
                }
            )
            records = []
            
            
            if response:
                print(response)
                if 'Item' in response and 'price' in response['Item']:
                    price_data.append(float(response['Item']['price']['close']))
                    
                else:
                    price_data.append(random.random())
                
                if 'Item' in response:
                    if len(response['Item']['sentiments'])!=0:
                        for i in range(len(response['Item']['sentiments'])):
                            for j in range(len(response['Item']['sentiments'][i]['scores'])):
                                response['Item']['sentiments'][i]['scores'][j] = float(response['Item']['sentiments'][i]['scores'][j])
                                
                            
                    senti.append([ i for i in response['Item']['sentiments'] ])
                else:
                    senti.append([])
                        
                 
        data = {
            'stock': stock,
            'price_data': [float(p) for p in price_data],
            'sentiments': [s for s in senti]
        }
        recommend_records.append(data)
    print(recommend_records)
    
    from datetime import date
    
    import datetime

    today = date.today()
    date = str(today)
    print("Today is (utc)" + str(date))
    est = datetime.timedelta(hours=-5)
    today += est
    
    date = str(today)
    
    data = {
        'rid': f"all_memestock_{''.join(recent_5_dates)}".lower(),
        'date': date,
        'data': {
            'stock_names': stock_names,
            'records': recommend_records,
            'dates': recent_5_dates
        }
    }
    
    response = table.put_item(
        Item = json.loads(json.dumps(data), parse_float=Decimal)
    )


    return {
        'statusCode': 200,
        'body': {
            'data': {
                'stock_names': stock_names,
                'records': recommend_records,
                'dates': recent_5_dates
            }
        }
    }
