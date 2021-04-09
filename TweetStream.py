# Author: Campbell Leckie
# Date: March 18th, 2021
# Additional Contributors: 

import MachineLearning
import tweepy
import sys
import time

class Tweet():
    __text = ""
    __id = -1
    __date = None
    __symbol = None

    # Class constructor
    def __init__(self, text, id, date, symbol):
        self.__text = text
        self.__id = id
        self.__date = date
        self.__symbol = symbol
        return

    # Getter methods
    def getText(self):
        return self.__text

    def getID(self):
        return self.__id

    def getDate(self):
        return self.__date

    def getSymbol(self):
        return self.__symbol
        

class MyStreamListener(tweepy.StreamListener):
    stocks = []
    
    def on_status(self, status):
        # If tweet has been truncated, get full text
        if hasattr(status, "extended_tweet"):
            text = (status.extended_tweet["full_text"])
        else:
            text = status.text

        symbol = self.__parseSymbol(text)

        if symbol != -1:
            # Construct Tweet object from streamed data
            currentTweet = Tweet(text, status.id, status.created_at, symbol)

            #print(text)
            MachineLearning.evaluate(currentTweet)


    def on_error(self, status_code):
        print("Error: ", status_code)
        # Attempts to reconnect to Twitter stream (with backoff)
        return True


    def __parseSymbol(self, text):

        for symbol in self.stocks:

            if symbol in text:
                return symbol

        return -1


    def start():
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

        # Authenticate with twitter API
        auth = tweepy.OAuthHandler(APIKey, APISecretKey)
        auth.set_access_token(accessToken, acessTokenSecret)
        api = tweepy.API(auth)

        # Create StreamListener instance
        streamListener = MyStreamListener()

        # Try to open stocks.txt
        try:
            stocksFile = open("stocks.txt", "r")

        except:
            print("ERROR: Unable to open/read stocks.txt")
            sys.exit(1)

        # Read all tickers from stocks.txt into class attribute list
        stocksFile.seek(0)

        for line in stocksFile:
            streamListener.stocks.append("$" + line.strip())

        stocksFile.close()

        # Connect to twitter stream and filter by stocks list
        stream = tweepy.Stream(auth = api.auth, listener=streamListener)
        stream.filter(languages=["en"], track=streamListener.stocks, is_async=True)

        # is_async parameter sets stream filter to its own thread, allowing execution to continue
        
if __name__ != "__main__"
MyStreamListener.start()