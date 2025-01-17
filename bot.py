import tweepy
import time
import random
import os
import string
import requests
from os import environ


CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)

api = tweepy.API(auth)

FN = 'lastId.txt'


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def corona():
    url = "https://covid-19-statistics.p.rapidapi.com/reports/total"
    headers = {'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",'x-rapidapi-key': "809e94140cmsh4623b64aef87772p1dbaedjsn10eccec71da3" }
    response = requests.request("GET", url, headers=headers)
    x = response.text
    x = eval(x)
    a = "Confirmed Cases : " + str(x["data"]["confirmed"])  + "\nRecovered : " + str(x["data"]["recovered"]) + "\nActive Cases : " + str(x["data"]["active"]) + "\nLast update : " + str(x["data"]["last_update"])
    return a

def reply_to_tweets():
    print("BOT UP AND RUNNING")
    last_seen_id = retrieve_last_seen_id(FN)
    mentions = api.mentions_timeline(last_seen_id,tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        print(" ")
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FN)
        if '#ln' in mention.full_text.lower():
            k = str(random.randint(0,100))
            api.update_status('Your lucky number is ' + k + '. @' + mention.user.screen_name, mention.id)
        elif '#jodi' in mention.full_text.lower():
            num2alpha = dict(zip(range(1, 27), string.ascii_uppercase))
            l = random.randint(1,26)
            api.update_status('First Letter Of The Person\'s Name You\'ll Marry to is ' + num2alpha[l] + '. @' + mention.user.screen_name, mention.id)
        elif '#corona' in mention.full_text.lower():
        	g = corona()
        	api.update_status(g + '\n@' + mention.user.screen_name, mention.id)


j = api.mentions_timeline()
print('last id' + str(j[0].id))
store_last_seen_id(j[0].id,FN)         
            

while True:
    reply_to_tweets()
    time.sleep(20)
