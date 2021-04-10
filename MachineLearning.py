from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk import FreqDist, classify, NaiveBayesClassifier

import sqlite3
from sqlite3 import Error

import re, string, random


# TODO create sentiment class
"""class Sentiment():
    
    __weight = 0
    __message_ID = ""
    __stock_ID = -1
    __date = None
    __symbol = None
    
    def __init__(self, result, message, stock_ID, date, symbol):
    
        self.__weight = result
        self.__message_ID = message
        self.__stock_id = stock_ID
        self.__date = date
        self.__symbol = symbol
        
        return
    
    def getWeight(self):
        return self.__weight
    
    def getMessage(self):
        return self.__message_ID

    def getID(self):
        return self.__stock_id

    def getDate(self):
        return self.__date
    
    def getSymbol(self):
        return self.__symbol    
"""

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

    return cleaned_tokens


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)
       
def connection(db):

    connection = sqlite3.connect(db)

    return connection

def updateDatabase(connection, tweet, result):
    
    sql_code = ''' INSERT INTO stock(getID(tweet)), VALUES(getID(tweet),getSymbol(tweet), ?, result)
              ON CONFLICT(getID(tweet)) DO UPDATE SET sentiment = sentiment + result'''
    
    cursor = connection.cursor()
    cursor.execute(sql_code, sentiment)
    connection.commit()
    
    return cursor.lastrowid
    
def evaluate(tweet):
    
    symbol = tweet.getSymbol()
    current_tokens = remove_noise(word_tokenize(tweet.getText()))

    # result is "Postive" or "Negative"
    result = classifier.classify(dict([token, True] for token in current_tokens))
    
    #current_sentiment = Sentiment(result, getText(tweet), getID(tweet), getDate(tweet), getSymbol(tweet))
    current_connection = connection(r"StockEye\StockEye\db.sqlite3")
    
    updateDatabase(current_connection, tweet, result)

    #print(result)

    # TODO Create a sentiment object
    
    # TODO Pass sentiment object to function for updating database
    


if __name__ != "__main__":
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    #print("Accuracy is:", classify.accuracy(classifier, test_data))
