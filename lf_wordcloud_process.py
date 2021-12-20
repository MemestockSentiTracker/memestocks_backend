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
    word_cloud = []
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
        
        words = defaultdict(int)
        for comment in comments:
            text = comment['text']
            for w in text.split(" "):
                if '$' not in w:
                    words[w.strip(",").strip(".")] += 1
        
        
        most_frequent = sorted( words.items(), key=lambda x: (-x[1], x[0]))
        # print(stock)
        word_cloud.append({
            'stock': stock,
            'freq': most_frequent[20:120]
        })
        
    data = {
            'rid': f"wordcloud_{date}".lower(),
            'date': date,
            'word_cloud': word_cloud
        }
    print(data)
    
    response = table.put_item(
                Item = json.loads(json.dumps(data), parse_float=Decimal)
            )
    
    return {
        'statusCode': 200,
        'body': json.dumps(word_cloud)
    }
