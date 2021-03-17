import tweepy
import sys

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        print("Error")


try:
    secretsFile = open("secrets.txt", 'r')
    APIKey = secretsFile.readline().strip()
    APISecretKey = secretsFile.readline().strip()
    accessToken = secretsFile.readline().strip()
    acessTokenSecret = secretsFile.readline().strip()
except:
    print("ERROR: Unable to open/read secrets.txt")
    sys.exit(1)

auth = tweepy.OAuthHandler(APIKey, APISecretKey)
auth.set_access_token(accessToken, acessTokenSecret)
api = tweepy.API(auth)

streamListener = MyStreamListener()
stream = tweepy.Stream(auth = api.auth, listener=streamListener)

stream.filter(languages=["en"], track=["$AMC", "$GME", "$TSLA"])