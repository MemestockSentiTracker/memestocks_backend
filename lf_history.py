import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    print(event)
    if 'stock' not in event:
        return {
        'statusCode': 200,
        'body': json.dumps('No stock name in path')
    }


    date = "2021-12-17" # TODO: Fix for now

    
    
    stock = event['stock']
    print(stock)
    print(event)
    
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('meme_stock_history')
    response = table.get_item(
        Key={
            'rid': f"sample_comments_{date}".lower()
        }
    )
    
    sample_comments = response['Item']['sample_comments']
    
    # ---------
    
    response = table.get_item(
        Key={
            'rid': f"wordcloud_{date}".lower()
        }
    )
    
    word_cloud = response['Item']['word_cloud']
    
    # ---------
    
    dates = ['2021-12-13', '2021-12-14', '2021-12-15', '2021-12-16', '2021-12-17']
    
    response = table.get_item(
        Key={
            'rid': f"num_posts_{''.join(dates)}".lower()
        }
    )
    
    weekly_post_count = response['Item']['weekly_post_count']
    
    print(weekly_post_count)
    
    # weekly_data = weekly_post_count[stock.lower()]
    # print(weekly_data)
    
    return {
        'statusCode': 200,
        'body': {
            # 'stock': stock,
            'word_cloud': word_cloud,
            'sample_comments': sample_comments,
            'weekly_post_count':  weekly_post_count
            
        }
    }
