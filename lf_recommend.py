import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import random

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('meme_stock_history')
    response = table.scan(FilterExpression=Attr('rid').eq('stock_tickers'))
    
    stocks = []
    
    if response:
        print(response)
        for record in response['Items']:
            stocks+=(record['tickers'])
    print(type(stocks))
    print(stocks)
    
    recommend_records = []
    stock_names = []
    price_data = []
    
    for stock in stocks:
        stock = stock.lower()
        response = table.scan(FilterExpression=Attr('stock').eq(stock))
        records = []
        stock_names.append(stock.upper())
        
        if response:
            print(response)
            for record in response['Items']:
                # print(record)
                if 'price' in record:
                    print(record['price'])
                    record['price']['close'] = float(record['price']['close']) # str(record['price'].get(['close'], 'Not Available Yet'))
                    record['price']['open'] = float(record['price']['open']) # str(record['price'].get(['open'], 'Not Available Yet'))
                    price_data.append(record['price']['open'])
                else:
                    price_data.append(random.random())
                    
             
        data = {
            'stock': stock,
            # 'records': records,
            'price_data': [p for p in price_data]
        }
        recommend_records.append(data)
    print(recommend_records)
    
    

    
    return {
        'statusCode': 200,
        'body': {
            'data': {
                'stock_names': stock_names,
                'records': recommend_records
            }
        }
    }
