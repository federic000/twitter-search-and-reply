# twitter-search-and-reply

## a simple twitter bot for searching a string (one ore more) and reply to those tweet id's.

1. tweet_retrieve.py searches for one or more keywords using the Twitter v2 API (recent searches, bearer token required). 
2. the tweet id's out of the search results are stored in a text file named new_ids.txt 
3. the tweet_post.py script tries to reply to all tweet id's that have been found
   - uploads an image (this uses V1.1 API's with chunked payload, elevated access required) and...
   - ...replies with a quote from a txt file stored under a local directory 
   - tweet id's are eventually stored in another file (old_ids.txt) to avoid a) multiple replies to the same tweet and b) to avoid self-replies. 

Some more details: 
1. it normally runs from crontab with shell scripts (run_script_post and _retrieve.sh).
2. the number of tweet id's varies from 10 to 100 as per Twitter API V2 and it's configurable in tweet_retrieve.py. 
3. the format of image files is today xy_gif.gif (or xy_png.png) where xy is a number between 00 and 99. This allows for random selection of image to be uploaded and posted. 
4. Format of quote file is simple text as in quote_001.txt example (quote is also randomly chosen)
5. The "logs" directory is hidden by .gitignore but shall be there. 
6. A new retrieve_v2 script has been added, this has a better refined search method

