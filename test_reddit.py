import json
import requests
requests.adapters.DEFAULT_RETRIES = 5
def get_pushshift_comment(data_type, **kwargs):
    """
    Gets data from the pushshift api.
 
    data_type can be 'comment' or 'submission'
    The rest of the args are interpreted as payload.
 
    Read more: https://github.com/pushshift/api
    """
 
    base_url = f"https://api.pushshift.io/reddit/search/comment/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()

def get_pushshift_post(data_type, **kwargs):
    """
    Gets data from the pushshift api.
 
    data_type can be 'comment' or 'submission'
    The rest of the args are interpreted as payload.
 
    Read more: https://github.com/pushshift/api
    """
 
    base_url = f"https://api.pushshift.io/reddit/search/submission/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()

if __name__ == '__main__':
    data_type="comment"     # give me comments, use "submission" to publish something
    query="amc"          # Add your query
    duration="24h"          # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
    size=100               # maximum 1000 comments
    sort_type="score"       # Sort by score (Accepted: "score", "num_comments", "created_utc")
    sort="desc"             # sort descending
    aggs="subreddit"        #"author", "link_id", "created_utc", "subreddit"
    comment = get_pushshift_comment(data_type=data_type,     
                   q=query,                 
                   after=duration,          
                   size=size,               
                   sort_type=sort_type,
                   sort=sort)
    with open('amc_comment.txt', 'w') as f:
        json.dump(comment, f, ensure_ascii=False)


    post = get_pushshift_post(data_type=data_type,     
                   q=query,                 
                   after=duration,          
                   size=size,               
                   sort_type=sort_type,
                   sort=sort)
    with open('amc_post.txt', 'w') as f:
        json.dump(post, f, ensure_ascii=False)