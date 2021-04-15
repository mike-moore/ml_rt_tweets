
# This is Main function.
# Extracting streaming data from Twitter, pre-processing, and loading into MySQL
import os, sys
this_files_dir = os.path.abspath(os.path.dirname(__file__))
configs_dir = os.path.abspath(os.path.join(this_files_dir, os.pardir, 'config'))
sys.path.append(configs_dir)
modules_dir = os.path.abspath(os.path.join(this_files_dir, os.pardir, 'src'))
sys.path.append(modules_dir)
import credentials
import re, time, csv
import tweepy
import pandas as pd
from textblob import TextBlob
from NaiveBayesTwitter import predict_tweet_sentiment as predict_nb_sentiment
from LstmTwitter import predict_tweet_sentiment as predict_lstm_sentiment


# Streaming With Tweepy 
# http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html#streaming-with-tweepy

# Override tweepy.StreamListener to add logic to on_status
class TwitterScraper(tweepy.StreamListener):
    '''
    Tweets are known as “status updates”. So the Status class in tweepy has properties describing the tweet.
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
    '''
    tweet_info = {
        'id_str' : 0,
        'created_at' : 0,
        'text' : '',
        'sentiment_obj_tb' : 0.0,
        'subjectivity_tb' : 0.0,
        'sentiment_tb' : 0.0,
        'sentiment_nb' : 0.0,
        'sentiment_lstm' : 0.0,
        'user_created_at' : 0,
        'user_location' : '',
        'user_description' : '',
        'user_followers_count' : 0,
        'longitude' : 0.0,
        'latitude' : 0.0,
        'retweet_count' : 0,
        'favorite_count' : 0,
    }

    def __init__(self, output_csv_file=None,time_limit_seconds=60):
        self.csv_file_name = output_csv_file
        self.start_time = time.time()
        self.limit = time_limit_seconds
        with open(self.csv_file_name, 'w') as csvfile:
            self.csv_writer = csv.DictWriter(csvfile, fieldnames=self.tweet_info.keys())
            self.csv_writer.writeheader()
            csvfile.close()
        super(TwitterScraper, self).__init__()
    
    def on_status(self, status):
        '''
        Extract info from tweets
        '''
        if (time.time() - self.start_time) < self.limit:
            if status.retweeted and 'RT @' in status.text:
                # Avoid retweeted info, and only original tweets will be received
                return True
            # Extract attributes from each tweet
            self.tweet_info['id_str'] = status.id_str
            self.tweet_info['created_at'] = status.created_at
            self.tweet_info['text'] = deEmojify(status.text)    # Pre-processing the text  
            self.tweet_info['sentiment_obj_tb'] = TextBlob(status.text).sentiment
            self.tweet_info['sentiment_tb'] = self.tweet_info['sentiment_obj_tb'].polarity
            self.tweet_info['subjectivity_tb'] = self.tweet_info['sentiment_obj_tb'].subjectivity
            self.tweet_info['sentiment_nb'] = predict_nb_sentiment(self.tweet_info['text'])
            self.tweet_info['sentiment_lstm'] = predict_lstm_sentiment(self.tweet_info['text'])
            self.tweet_info['user_created_at'] = status.user.created_at
            self.tweet_info['user_location'] = deEmojify(status.user.location)
            self.tweet_info['user_description'] = deEmojify(status.user.description)
            self.tweet_info['user_followers_count'] = status.user.followers_count
            self.tweet_info['longitude'] = None
            self.tweet_info['latitude'] = None
            if status.coordinates:
                self.tweet_info['longitude'] = status.coordinates['coordinates'][0]
                self.tweet_info['latitude'] = status.coordinates['coordinates'][1]
            self.tweet_info['retweet_count'] = status.retweet_count
            self.tweet_info['favorite_count'] = status.favorite_count
            if self.csv_file_name:
                self.write_to_csv()
        else:
            return False

    def write_to_csv(self):
        with open(self.csv_file_name, 'a+', newline='') as csvfile:
            print(self.tweet_info)
            dictwriter_object = csv.DictWriter(csvfile, fieldnames=self.tweet_info.keys())
            dictwriter_object.writerow(self.tweet_info)
            csvfile.close()

    def write_to_db(self):
        print("TODO: Implement DB connection")
        # # Store all data in Heroku PostgreSQL
        # cur = conn.cursor()
        # sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(settings.TABLE_NAME)
        # val = (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, \
        #     user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count)
        # cur.execute(sql, val)
        # conn.commit(

    
    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, stop srcraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False

def start_stream(listener, languages=["en"], track_topics=[""]):
        myStream = tweepy.Stream(auth = api.auth, listener = listener)
        myStream.filter(languages=["en"], track = track_topics)


def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None


auth  = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)