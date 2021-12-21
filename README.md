# memestocks AWS components

### Architecture

![alt text](https://github.com/MemestockSentiTracker/memestocks_backend/blob/main/Architecture.png?raw=true)


### API Gateway
- MemeStockProject: MemeStockProject-dev-swagger.json

### Lambda Function: py script
- meme_yahoo_stockprice: lf_yahoo.py
-- this LF is used for collecting daily close prices for the memestocks(triggering an Endpoint on an EC2 instance (Flask server) using yfinance library)

- meme_wordcloud_process: lf_wordcloud_process.py
-- this LF extracts words freqeuncy for posts sent on the lastest finished trading day  

- meme_weekly_postcount_process: lf_weekly_postcount_process.py
-- this LF counts latest 5 trading day's post counts

- meme_sample_comment_process: lf_sample_comment_process.py
-- this LF selects sample comments for the memestocks

- meme_twitter_crawler: lf_twitter.py
-- this LF is used for getting sentiment scores for the memestocks' Twitter posts (triggering an Endpoint on an EC2 instance (Flask server) using yfinance library)

- meme_reddit_crawler: lf_reddit.py
-- this LF is used for getting sentiment scores for the memestocks' Reddit posts (triggering an Endpoint on an EC2 instance (Flask server) using yfinance library)


- meme_stocks_recommend: lf_recommend.py
--  this LF is used for extracting and storing lastest 5 trading days' essential data (stock price, sentiment score statistics) for Frontend fast retrieval.

- meme_stock_history: lf_history.py
-- this LF is used for getting detailed data such as word cloud, weekly post count and sample comments.

