import tweepy
import time
CONSUMER_KEY = "XU8an5Rjf2Jt7DLiKCVa7yXqa"
CONSUMER_SECRET = "5Hu3ouTlGT2ZID2oYup5oJXK4VbtBALzKk6eJRaeHVqVUfqaUB"
ACCESS_KEY = "1078872398441734145-7ae0Q8eOXAl2w9vWN1FEfEfT59PvtA"
ACCESS_SECRET = "RzrEvRFhFdNSHaSd30CcQwF1Q0vaDL8dgX3FXq0fLWNyM"
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

last_seen_id = retrieve_last_seen_id(FN)
mentions = api.mentions_timeline(last_seen_id,tweet_mode='extended')

def reply_to_tweets():
    print("Replying")
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FN)
        if '#jsm' in mention.full_text.lower():
            api.update_status('Jai Shree Ram @' + mention.user.screen_name, mention.id)

while True:
    reply_to_tweets()
    time.sleep(15)