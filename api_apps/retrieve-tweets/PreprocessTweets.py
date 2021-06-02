import pandas as pd
import numpy as np
import string
import re

import nltk
from nltk import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')

df = pd.read_csv('data/twitter_data.csv')

def remove_emojis(tweet):
    '''Accepts a tweet (string), matches unicode for
    emoticons, symbols and pictographs, transport and
    map symbols, iOS flags, and removes them. Returns
    a modifided tweet as a string.'''
    
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    
    return regrex_pattern.sub(r'',tweet)


def remove_stopwords(tweet, stopwords):
    '''Accepts a tweet (string) and stopwords (list).
    It splits the Tweet into a list of strings, and
    returns the items in the string that are not found
    in stopwords.'''
    
    tweet = tweet.split(' ')
    return [t for t in tweet if t not in stopwords]
    

def remove_all(tweet):
    '''Accepts a tweet as a string, splits it into tokens,
    and removes any tokens that starts with @. Returns a
    new tokenized tweet minues any user names.'''
    
    users = [t for t in tweet if '@' in t] # select usernames
    hashes = [t for t in tweet if '#' in t] # select hashtags
    http = [t for t in tweet if 'http' in t] # web addresses
    
    drop_items = users + hashes + http
    new_tweet = [t for t in tweet if t not in drop_items]
    
    return new_tweet


def preprocess_tweets(df):
    '''Accepts a pd.Dataframe retrieved from RetrieveTweets.py,
    drop unnecessary columns, drops usernames, removes stopwords 
    and punctuaation from text, tokenizes. Returns a transformed
    pd.DataFrame'''
    
    # drop unnecessary columns
    drop_cols = [col for col in df.columns if col != 'text']
    df = df.drop(drop_cols, axis=1)
    
    df['cleaned_text'] = df.text.apply(lambda x: remove_emojis(x))
    
    from nltk.corpus import stopwords
    stopwords_list = stopwords.words('english')
    stopwords_list += list(string.punctuation)
    df['cleaned_text'] = df.cleaned_text.apply(lambda x: remove_stopwords(x, stopwords_list))
    
    df['cleaned_text'] = df.cleaned_text.apply(lambda x: remove_all(x))
    df['cleaned_text'] = df.cleaned_text.apply(lambda x: ' '.join(x)).str.replace('\W+ ', '')
    df['retweet'] = df.cleaned_text.apply(lambda x: 1 if x.upper().startswith('RT') else 0)
    df['cleaned_text'] = df.cleaned_text.str.replace('RT', '')
    df['cleanted_text'] = df.cleaned_text.apply(lambda x: x.lower())
    
    return pd.DataFrame(df[['text', 'cleaned_text']])


