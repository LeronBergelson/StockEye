# Author: Campbell Leckie
# Date: March 18th, 2021
# Additional Contributors: 

import tweepy
import sys
import time

class Tweet():
    __text = ""
    __id = -1
    __date = None

    # Class constructor
    def __init__(self, text, id, date):
        self.__text = text
        self.__id = id
        self.__date = date
        return

    # Getter methods
    def getText(self):
        return self.__text

    def getID(self):
        return self.__id

    def getDate(self):
        return self.__date


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        # If tweet has been truncated, get full text
        if hasattr(status, "extended_tweet"):
            text = (status.extended_tweet["full_text"])

        else:
            text = status.text
        
        # Construct Tweet object from streamed data
        currentTweet = Tweet(text, status.id, status.created_at)

    def on_error(self, status_code):
        print("Error")


# Try to open secrets.txt
try:
    secretsFile = open("secrets.txt", 'r')

except:
    print("ERROR: Unable to open/read secrets.txt")
    sys.exit(1)

# Read in tokens from secrets.txt file
APIKey = secretsFile.readline().strip()
APISecretKey = secretsFile.readline().strip()
accessToken = secretsFile.readline().strip()
acessTokenSecret = secretsFile.readline().strip()
secretsFile.close()

# Try to open stocks.txt
try:
    stocksFile = open("stocks.txt", "r")

except:
    print("ERROR: Unable to open/read stocks.txt")
    sys.exit(1)

# Read all tickers from stocks.txt into list
stocksFile.seek(0)
stocks = []

for line in stocksFile:
    stocks.append("$" + line.strip())

stocksFile.close()

# Authenticate with twitter API
auth = tweepy.OAuthHandler(APIKey, APISecretKey)
auth.set_access_token(accessToken, acessTokenSecret)
api = tweepy.API(auth)

# Connect to twitter stream and filter by stocks list
streamListener = MyStreamListener()
stream = tweepy.Stream(auth = api.auth, listener=streamListener)
stream.filter(languages=["en"], track=stocks, is_async=True)

# is_async parameter sets stream filter to its own thread, allowing execution to continue
while(1):
    time.sleep(1)
    print("The program is continuing")