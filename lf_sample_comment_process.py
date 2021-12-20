import json
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import time

from collections import defaultdict

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
    
    
    date = "2021-12-17"# TODO: fix for now
    sample_comments = []
    for stock in stocks:
        response = table.get_item(
                Key={
                    'rid': f'{stock}_{date}'
                }
            )
        # records
        data = response['Item']
        print(data.keys())
        comments = data['records']['comment']
        c = []
        for com in comments[:20]:
            c.append(com['text'])
            
        
        sample_comments.append({
            'stock': stock,
            'sample_comments': c
        })
        
    data = {
            'rid': f"sample_comments_{date}".lower(),
            'date': date,
            'sample_comments': sample_comments
        }
    print(data)
    
    response = table.put_item(
                Item = json.loads(json.dumps(data), parse_float=Decimal)
            )
    
    return {
        'statusCode': 200,
        'body': json.dumps(sample_comments)
    }
