import json
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import random
import time
import datetime

requests.adapters.DEFAULT_RETRIES = 5


# https://developer.twitter.com/en/docs/twitter-api/rate-limits#v2-limits
# Twitter API v2 rate limits
def convert_time(t):
    return t[:10]

def get_senti_score(text):
    base_url = f"http://52.206.155.70:8080/sentiscore"
    payload = {'text': text}
    request = requests.get(base_url, json=payload)
    # print(text)
    # print(request)
    return request.json()

def get_stats(arr):
    arr.sort()
    if not arr:
        return []
    ret =  [arr[0], arr[len(arr)//4], arr[len(arr)//2], arr[len(arr)*3//4], arr[-1]]
    for i in range(len(ret)):
        ret[i] = round(ret[i],2)
    return ret

def crawler(stock):
    
    from datetime import date
    today = date.today()
    est = datetime.timedelta(hours=-5)
    today += est
    date = str(today)
    
    print("Today is " + str(date))


    access_token = 'AAAAAAAAAAAAAAAAAAAAAM4pWQEAAAAAsI1%2BKKLpm85%2FHj9eToHnMhwrj7U%3DtTbXi7FwRuadwMewwYYQy0OryfBP0BqhDNTXj8H1GulJaETIyp'
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
        }

   
    stock = stock
    base_url = 'https://api.twitter.com/'
    search_url = f"https://api.twitter.com/2/tweets/search/recent?query={stock}&tweet.fields=created_at&expansions=author_id&user.fields=created_at&max_results=100"
    search_resp = requests.get(search_url, headers=search_headers)

    # print(search_resp.json())
    # import emoji
    # print(len(search_resp.json()['data']))
    
    p = []
    for each in search_resp.json()['data']:
        print(each)
        p.append({
            'text': each['text'],
            'date': date,
            'id': each['id']
        })
    text = p 
    scores = []
    src = 'Twitter'
    
    for i, each in enumerate(text):
        score = get_senti_score(each['text'])# random.randrange(-100,100)*0.01
        s = score['body']['scores']
        scores.append(s)
        text[i]['score'] = s
    
    
    # stock = query
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('meme_stock_history')
    response = table.get_item(
        Key={
            'rid': f'{stock}_{date}'
        }
    )
    # .scan(FilterExpression=Attr('stock').eq(stock) & Attr('date').eq() )
    # print(response)
    
    
    
    if 'Item' not in response:
        
        
        data = {
                'rid': f"{stock}_{date}".lower(),
                'stock': stock,
                'date': date,
                'records': {
                    'comment': text
                },
                'sentiments': [
                    {
                        'source': src,
                        'scores': get_stats(scores)
                    }
                ],
                'v': 0
                
            }
        response = table.put_item(
            Item = json.loads(json.dumps(data), parse_float=Decimal)
        )
        # print (response)
        
        
    else:
        
        data = response['Item']
        data['records']['comment'] += text
        added = False
        for i, each in enumerate(data['sentiments']):
            if each['source'] == src:
                added = True
                data['sentiments'][i] = {
                            'source': src,
                            'scores': get_stats(scores)
                        }
                break
        if not added:
            data['sentiments'].append( {
                            'source': src,
                            'scores': get_stats(scores)
                        })
        for i in range(len(data['sentiments'])):
            for j in range(len(data['sentiments'][i]['scores'])):
                data['sentiments'][i]['scores'][j] = float(data['sentiments'][i]['scores'][j])

        for i in range(len(data['records']['comment'])):
            data['records']['comment'][i]['score'] = float( data['records']['comment'][i]['score'] )
            
        if 'price' in data and 'close' in data['price']:
            data['price']['close'] = float(data['price']['close'])
            
        data['v'] += 1
        data['v'] = float(data['v'])
        
        added = set()
        comments = []
        for comment in data['records']['comment']:
            if comment['id'] not in added:
                added.add(comment['id'])
                comments.append(comment)
        data['records']['comment'] = comments
        
        
        response = table.put_item(
            Item = json.loads(json.dumps(data), parse_float=Decimal)
        )
        # print (response)
    # print(data)
        
        
    
    
    

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('meme_stock_history')
    response = table.get_item(
        Key={
            'rid': 'stock_tickers'
        }
    )
    # print(response)
    stocks = []
    for each in response['Item']['tickers']:
        stocks.append(each)
    print(stocks)
    
    
    
    res = []
    for stock in stocks:
        print("crawling: "+stock)
        print( type(stock) )
        crawler(str(stock))
        time.sleep(2)
        # res.append(response)
    
    

    
    
    return {
        'statusCode': 200,
        'body': {
            'responses': ''
        }
    }
