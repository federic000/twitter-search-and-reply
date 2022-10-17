# twitter-search-and-reply
the twitter bot for searching and reply.

1) tweet_retrieve.py searches for one or more keywords using the Twitter v2 API (recent searches). 
2) the tweet id's out of the search results are stored in a text file 
3) the tweet_post.py replies to all tweet id's, uploads an image (this uses V1.1 API's with chunked payload) and replies with a quote from a txt file


