import json
import requests
requests.adapters.DEFAULT_RETRIES = 5


# https://developer.twitter.com/en/docs/twitter-api/rate-limits#v2-limits
# Twitter API v2 rate limits

if __name__ == '__main__':


    access_token = 'AAAAAAAAAAAAAAAAAAAAAM4pWQEAAAAAsI1%2BKKLpm85%2FHj9eToHnMhwrj7U%3DtTbXi7FwRuadwMewwYYQy0OryfBP0BqhDNTXj8H1GulJaETIyp'
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
        }

    search_params = {
        'q': 'General Election',
        'result_type': 'recent',
        'count': 2
    }
    stock = 'AMC'
    base_url = 'https://api.twitter.com/'
    # search_url = f'{base_url}1.1/search/tweets.json'
    search_url = f"https://api.twitter.com/2/tweets/search/recent?query={stock}&tweet.fields=created_at&expansions=author_id&user.fields=created_at&max_results=100"
    search_resp = requests.get(search_url, headers=search_headers)

    print(search_resp.json())
    # import emoji
    print(len(search_resp.json()['data']))
    with open("test.txt", "w",encoding='utf-8') as f:
        for tweets in search_resp.json()['data']:
            f.write(str(tweets)+'\n')

