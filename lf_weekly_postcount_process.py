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
    
    all_counts = defaultdict(list)
    dates = ['2021-12-13', '2021-12-14', '2021-12-15', '2021-12-16', '2021-12-17']
    for date in dates:
        # date = "2021-12-17"# TODO: fix for now
        sample_comments = []
        for stock in stocks:
            response = table.get_item(
                    Key={
                        'rid': f'{stock}_{date}'
                    }
                )
            # records
            data = response['Item']
            # print(data.keys())
            comments = data['records']['comment']
            # sample_comments.append({
                
                
            # })
            all_counts[stock].append({
                'date': date,
                'num_posts': len(comments)
            })
        time.sleep(3)
        
    data = {
            'rid': f"num_posts_{''.join(dates)}".lower(),
            'weekly_post_count': all_counts
            
        }
    print(all_counts)
    print(data)
    
    response = table.put_item(
                Item = json.loads(json.dumps(data), parse_float=Decimal)
            )
    
    return {
        'statusCode': 200,
        'body': data
    }
