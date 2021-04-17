from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk import FreqDist, classify, NaiveBayesClassifier

import sys
import sqlite3
from sqlite3 import Error

import re, string, random


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
       
    
def evaluate(tweet):
    
    symbol = tweet.getSymbol()
    current_tokens = remove_noise(word_tokenize(tweet.getText()))

    # Result is "Postive" or "Negative"
    result = classifier.classify(dict([token, True] for token in current_tokens))
    #print(result)

    # Update database accordingly
    updateDatabase(result, tweet.getStock_id(), tweet.getSymbol(), tweet.getID())


def connection(db):
    try:
        connection = sqlite3.connect(db)

    except:
        print("ERROR: Failed to connect to database")
        sys.exit(1)

    return connection


def updateDatabase(result, stock_id, symbol, tweet_id):


    conn = connection(r"StockEye/StockEye/db.sqlite3")
    cursor = conn.cursor()

    # Check if row exists in database
    query = "SELECT EXISTS(SELECT 1 FROM app_stocklist WHERE stock_id = ?)"

    cursor.execute(query, (str(stock_id),))
    exists = cursor.fetchone()[0]
    #print(exists)

    if (exists):
        # Update sentiment
        if (result == "Positive"):
            query = "UPDATE app_stocklist SET positiveSentimentCount = positiveSentimentCount + 1 WHERE stock_id = ?"

        else:
            query = "UPDATE app_stocklist SET negativeSentimentCount = negativeSentimentCount + 1 WHERE stock_id = ?"

        cursor.execute(query, (str(stock_id),))

        # Update tweet_id
        query = "UPDATE app_stocklist SET tweet_id = ? WHERE stock_id = ?"
        params = (str(tweet_id), str(stock_id))
        cursor.execute(query, params)

    else:
        # Insert new row into table
        query = """INSERT INTO app_stocklist(stock_id, symbol, positiveSentimentCount, negativeSentimentCount, value, tweet_id) VALUES(?, ?, ?, ?, ?, ?)"""

        if (result == "Positive"):
            params = (str(stock_id), symbol, "1", "0", "0.0", str(tweet_id))

        else:
            params = (str(stock_id), symbol, "0", "1", "0.0", str(tweet_id))

        cursor.execute(query, params)

    conn.commit()
    conn.close()

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
