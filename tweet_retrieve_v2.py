#!/usr/bin/python3
import requests
import os
import json
import sys
import logging
import re
from secrets import bearer_token 

#this script refreshes the new tweet lists  
#logging level can be changed here, INFO, DEBUG or other.
logging.basicConfig(filename='./logs/logging_retrieve.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',)
logging.info('script startup message ....script starting now')

#Twitter API v2 used here
search_url = "https://api.twitter.com/2/tweets/search/recent"

#Query string, change keywords or result(s) number
#added -from with the bot account name to avoid auto-reply 
query_params = {'query': '-from:botaccountname -is:retweet (keyword1 OR keyword2)', 'max_results': '50'} 


def bearer_oauth(r):
    #bearer_token is taken from secrets file 
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def tweet_id_retrieve():
    #writes a file new_ids.txt with recent tweets (no retweets) containing the keywords
    #the function has been enhanced to avoid replies to those tweets where the username includes the search keywords
    #it also check if it's a legit tweeet to be replied (this is because Twitter API v2 does not allow searching with Regexp's) 
    #as usual, regexp strings can be improvoved...
    json_response = connect_to_endpoint(search_url, query_params)
    with open("new_ids.txt", 'w') as f:
         results = int(json_response.get('meta').get('result_count'))
         sys.stdout = f
         for i in range(results):
             tweet_text = str(json_response.get('data')[i].get('text'))
             if (re.search(r"[@]\S*keyword1*", tweet_text)) or (re.search(r"[@]\S*keyword2*", tweet_text)):
                   logging.info("username including a search keyword has been found, check if goes into new_ids.txt ----> %s", tweet_text)
                   if re.search(r"\skeyword[12][345]", tweet_text):
                        logging.info("...but text does include search keyword hence add it to new_ids.txt anyway")
                        print(json_response.get('data')[i].get('id'))
                   else:
                        logging.info("text does not include search keyword hence does not go into new_ids.txt")
             else:
                  print(json_response.get('data')[i].get('id'))


def main():
    tweet_id_retrieve()

if __name__ == "__main__":
    main()
