import os
import pandas as pd


def read_tweets_from_file(filename):
    df = pd.read_csv(filename)
    # UTC for date time at default
    df['created_at'] = pd.to_datetime(df['created_at'])
    return df

