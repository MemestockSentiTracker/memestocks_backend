import json
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import random
import time

requests.adapters.DEFAULT_RETRIES = 5

def get_pushshift_comment(data_type, **kwargs):
    base_url = f"https://api.pushshift.io/reddit/search/comment/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()

def get_pushshift_post(data_type, **kwargs):
    base_url = f"https://api.pushshift.io/reddit/search/submission/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()
    
from datetime import datetime
def convert_time(ts):
    dt = datetime.fromtimestamp(ts)
    return f"{dt.year}-{dt.month}-{dt.day}"
    
def get_stats(arr):
    arr.sort()
    if not arr:
        return []
    ret =  [arr[0], arr[len(arr)//4], arr[len(arr)//2], arr[len(arr)*3//4], arr[-1]]
    for i in range(len(ret)):
        ret[i] = round(ret[i],2)
    return ret

def get_senti_score(text):
    base_url = f"http://52.206.155.70:8080/sentiscore"
    payload = {'text': text}
    request = requests.get(base_url, json=payload)
    print(text)
    print(request)
    return request.json()

def crawler(stock):
    data_type="comment"     # give me comments, use "submission" to publish something
    query= stock #"tsla"          # Add your query
    duration="24h"          # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
    size=10000               # maximum 1000 comments
    sort_type="score"       # Sort by score (Accepted: "score", "num_comments", "created_utc")
    sort="desc"             # sort descending
    aggs="subreddit"        #"author", "link_id", "created_utc", "subreddit"
    try:
        comment = get_pushshift_comment(data_type=data_type,     
                       q=query,                 
                       after=duration,          
                       size=size,               
                       sort_type=sort_type,
                       sort=sort)
    except:
        comment = {'data':[]}
    try:
        
        post = get_pushshift_post(data_type=data_type,     
                       q=query,                 
                       after=duration,          
                       size=size,               
                       sort_type=sort_type,
                       sort=sort)
    except:
        post = {'data':[]}
        
    # print(comment)
    c = []
    for each in post['data']:
        c.append({
            'text': each['title'] +" . "+each['selftext'],
            'date': convert_time(each['created_utc']) ,
            'id': each['id']
        })
    # print(post)
    p = []
    for each in comment['data']:
        p.append({
            'text': each['body'],
            'date': convert_time(each['created_utc']),
            'id': each['id']
        })
    
    text = p + c
    scores = []
    
    
    for i, each in enumerate(text):
        score = get_senti_score(each['text'])# random.randrange(-100,100)*0.01
        s = score['body']['scores']
        scores.append(s)
        text[i]['score'] = s
    
    from datetime import date
    today = date.today()
    date = str(today)
    
    print(date)
    stock = query
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('meme_stock_history')
    response = table.scan(FilterExpression=Attr('stock').eq(stock) & Attr('date').eq(date) )
    # print(response)
    src = 'Reddit'
    
    
    if len(response['Items']) == 0:
        
        
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
        print (response)
        
        
    else:
        
        data = response['Items'][0]
        data['records']['comment'] += text
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
        print (response)
    print(data)
        
    

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
