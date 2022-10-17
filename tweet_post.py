#!/usr/bin/python3
from requests_oauthlib import OAuth1Session
import os
import json
import tweepy 
import random 
import logging
from secrets import bearer_token
from secrets import consumer_key_bot
from secrets import consumer_secret_bot
from secrets import access_token_bot
from secrets import access_token_secret_bot

logging.basicConfig(filename='./logs/logging_post.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
datefmt='%Y-%m-%d %H:%M:%S',)
logging.info('tweet_post script startup message ....or at least it should do this')


#function checks if tweet_id has been replied already
def tweet_check_old(tweet_id):
    if tweet_id in open('old_ids.txt').read():
       return (True)
       logging.info('tweetid %s found in old_ids file, exiting...', tweet_id)
    else:
       return (False)
       logging.info('tweetid %s NOT found in old_ids file, proceeding...', tweet_id)

def tweet_post_phase0():
    #read new_ids.txt, if it's a new tweet uploads image (png, jpg, gif...) and post reply
    logging.info('start inspection for new tweet ids --- \n')
    with open(r"new_ids.txt", 'r') as f:
         for index, line in enumerate(f):
             tweet_id_str = index, line
             if not tweet_check_old(line):
                 logging.info ('looks like a new tweet, now reply the tweet id = %s', tweet_id_str)
                 line = line.replace("\n","")
                 # check if tweet id really exists 
                 if check_tweet_exist(line):
                     #upload and post if bool = True
                     mediaidtemp = upload_image()
                     post_tweet_reply(line, mediaidtemp)
                     logging.info ('add tweet_id to old_ids.txt')
                     old_ids_add_line(line)
                 else: 
                     logging.info ('tweet id does not exist, exiting...') 
             else:
                 logging.info ('already replied the tweet id = %s', tweet_id_str)

#function to check if the tweet does (still) exist 
def check_tweet_exist(twid):
    api = tweepy.Client(bearer_token)
    response = api.get_tweet(id=twid)
    if "resource-not-found" in str(response.errors):
       logging.info(f"message id {twid} does not exist...exiting") 
       return False
    else:
       logging.info(f"message id {twid} is still there, replying...")
       return True

#function to add tweet id we already replied at
def old_ids_add_line(tweet_id_str):
    file_object = open('old_ids.txt', 'a')
    file_object.write(tweet_id_str + "\n")
    file_object.close()


def upload_image():
    #function to upload images before posting
    auth = tweepy.OAuthHandler(consumer_key_bot, consumer_secret_bot)
    # access with v1.1 API's for chuncked upload
    auth.set_access_token(access_token_bot, access_token_secret_bot)
    api = tweepy.API(auth)
    # the path of the media to be uploaded randomly chosen in a range of picture files
    random_file_digits = f'{random.randrange(1, 6):02}'
    filename = "./images/" + random_file_digits + "_png.png"
    try:
       img_upload = api.chunked_upload(filename)
       logging.info (f"media id uploaded is : {img_upload.media_id_string}")
       return img_upload.media_id_string
    except tweepy.TweepyException as errorcode:
        logging.info('we got an error code returned by upload image: ', errorcode.api_messages)



def post_tweet_reply(twid, mediaid):
    #now uses twitter API v2 
    api = tweepy.Client(
                    access_token=access_token_bot, 
                    access_token_secret=access_token_secret_bot,
                    consumer_key=consumer_key_bot,
                    consumer_secret=consumer_secret_bot,
                    return_type = dict)

    #the text to be tweeted randomly chosen from a file of quotes
    quote = random.choice(list(open('./quotes/quote_001.txt')))
    #posting the tweet and avoid exceptions 
    try:
       response = api.create_tweet(text=quote, in_reply_to_tweet_id=twid, media_ids=[mediaid])
       posted_msg_id = response.get('data').get('id')
       logging.info ('the newly posted message is = %s', posted_msg_id)
       #add new posted tweet id to old_ids to avoid self-reply in next occurrences
       old_ids_add_line(posted_msg_id)
    except tweepy.TweepyException as errorcode:
       logging.info('we got an error code returned by post tweet: ', errorcode.api_messages)

#deletes new_ids.txt 
def emptyfile(filenamepath):
    with open(filenamepath, 'w'): pass


def main():
    tweet_post_phase0()
    emptyfile("./new_ids.txt")

if __name__ == "__main__":
    main()

