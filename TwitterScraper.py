
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 09:33:00 2018

@author: kateschulz
"""
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys


#keys and tokens to Twitter app
consumer_key = 'LFxLOTtKNgfAbTmJsIIKNjPtz'
consumer_secret = '7f3H02uvEnf4hMVGa7oqtcgxrzovQifGlspX14RHeFEk4aRNup'
access_token = '1054412149420949514-0UzKziPkn6zhzKoT43xROolXVGbLuU'
access_secret = 'zERzaxVDgeqoFbJL9KK2FJ46g48ToGIKjeFEdS5vW6Uo0'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


#error trapping for user input
try:
    input = raw_input
except NameError:
    pass

def prompt(message, errormessage, isvalid):
    res = None
    while res is None:
        res = input(str(message)+': ')
        if not isvalid(res):
            print (str(errormessage))
            res = None
    return res

#user input hashtag and number of tweets to scrape
hashtag = prompt(
        message = 'Enter a hashtag ', 
        errormessage = 'Please use a hashtag (#)',
        isvalid = lambda hashtag : hashtag.startswith('#'))

num_tweets = prompt(
        message = 'How many tweets? ', 
        errormessage= 'Number of tweets must be between 1 and 30',
        isvalid = lambda num : 1 <= int(num) <= 30)


# class TwitterListener scrapes tweets based on specified hashtag and 
# number of tweets and writes them to file 'data.json'.
class TwitterListener(StreamListener):
    tweet_number = 0
    
    #tracks number of tweets to scrape
    def __init__(self, max_tweets):
        self.max_tweets = max_tweets
    
    #writes tweets to .json file
    def on_data(self, data):
        if self.tweet_number >= self.max_tweets:
            sys.exit('Congratulations! Your tweets are now in data.json. ' +
                     'Move on to TwitterWordCloud.py.')
            
        self.tweet_number = self.tweet_number +1
        
        try:
            with open('data.json', 'a') as f: 
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    
    #error trapping
    def on_error(self, status):
                
        if self.tweet_number >= self.max_tweets:
            sys.exit('Limit of ' + str(self.max_tweets) + ' tweets reached.')
        
        print(status)
        
        if(status == 420):
            print("Error", status, "rate limited")
            sys.exit('Uh-oh! Twitter is throttling you. Try again in 15 min.')
        return True


#scrape tweets based on user input
twitter_stream = Stream(auth, TwitterListener(int(num_tweets)))
twitter_stream.filter(track=[hashtag])





