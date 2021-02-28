import tweepy
import sys

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

tweets = api.user_timeline(screen_name = "elonmusk", count=200)

for tweet in tweets:
    print(tweet.text)