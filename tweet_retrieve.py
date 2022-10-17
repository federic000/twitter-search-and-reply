#!/usr/bin/python3
import requests
import os
import json
import sys
import logging
from secrets import bearer_token 

#this script refreshes the new tweet lists  
#logging level can be changed here, INFO, DEBUG or other.
logging.basicConfig(filename='./logs/logging_retrieve.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',)
logging.info('script startup message ....script starting now')

#Twitter API v2 used here
search_url = "https://api.twitter.com/2/tweets/search/recent"

#Query string, change keywords or result(s) number
query_params = {'query': '-is:retweet (keyword1 OR keyword2)', 'max_results': '50'} 


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
    json_response = connect_to_endpoint(search_url, query_params)
    with open("new_ids.txt", 'w') as f:
         results = int(json_response.get('meta').get('result_count'))
         sys.stdout = f
         for i in range(results):
             print(json_response.get('data')[i].get('id'))


def main():
    tweet_id_retrieve()

if __name__ == "__main__":
    main()
