# Author: Campbell Leckie
# Date: March 18th, 2021
# Additional Contributors: 

import tweepy
import sys


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

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
stream.filter(languages=["en"], track=stocks)