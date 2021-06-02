import pandas as pd
import numpy as np

import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

import re

from twython import Twython

def language_block(languages):
    '''Prints language information for the user so that a language option
    can be chosen.'''
    
    print('\nChoose one of the following languages:')
    print([l.title() for l in list(languages.keys())])
    print('Note: To chose another language hit RETURN.')
    print('You will be prompted to enter the two character language code.')
    print('To obtain language codes please see the following:')
    print('https://developer.twitter.com/en/docs/twitter-api/v1/developer-utilities/supported-languages')
    
    pass


def tweet_params():
    '''A script that collects user input to generate parameters for the 
    Twitter API Recent Search endpoint. User will enter search query (q), 
    result type (result_type), langauge (lang), and number of results (count). 
    Will process and return the parameters: q, result_type, lang, and count. '''
    
    # query
    print('What do terms do you wish to search?')
    q = input('Query: ')
    q = q.replace(' ', '+').lower()

    # result type
    result_types = ['recent', 'popular']
    print('\nHow do you want to sort your results?')
    print('Choose one of the following: ', result_types)
    result_type = input('Result Type: ')
    print(result_types)
    result_type = result_type.lower()
    
    if result_type not in result_types:
        print('Result type not recognized, please try again.')

    # language
    languages = {'french': 'fr', 'english': 'en', 'arabic': 'ar', 
             'japanese': 'ja', 'spanish': 'es', 'german': 'de'}
    
    language_block(languages)
    
    lang_raw = input('Language: ')
    lang = str(languages[lang_raw.lower()])
    
    while lang_raw.lower() not in list(languages.keys()):
        
        if lang_raw == '':
            lang = input('Enter langauge code: ')
            lang = lang_raw.lower()
            
            break
        
        elif lang_raw != '':
            language_block(languages)
            lang_raw = input('Language: ')
            
            break
            
    # number of results
    print('\nHow many results would you like returned?')
    print('Note: Check your Twitter developer account to see you call limit.')
    count = input('Number of Results: ')
    count = int(count)
    while count > 50000:
        print('Too many. Enter a smaller number.')
    
    return q, result_type, lang, count


def make_twython_query(q, result_type, lang, count):
    '''Accepts argument q (search term(s)), result_type ('popular', 'recent', 'mixed'), 
    lang (language code),and count (number of results), and structures a Twitter API query.
    Returns a dictionary with the query.'''
    
    query = {'q': q,
             'result_type': result_type,
             'lang': lang,
             'count': count
            }
    
    return query


def tweet_query_summary(q, result_type, lang, count):
    '''Accepts Twitter API Recent Search parameters: q (string), result_type (string), 
    lang (string), and count (int). Prints a summary of these parameters. Confirms with
    the user that the query is acceptable. If confirmed, query is returned. If not
    confirmed, user is prompted to re-enter parameters.
    '''
    print('='*30)
    print('Summary of Query')
    print('-'*30)
    print('Check your responses carefully to avoid wasting API calls.')

    print('Query term: ', q.replace('+', ' ').lower())
    print('Result type: ', result_type)
    print('Language: ', lang)
    print('Number of results:', count)
    

    answers = ['Y','N']
    print('\nAre you happy with your query?', answers)
    answer = input()
    
    while answer not in answers:
        print('Response not recogized. Please try again.')
        answer = input()
        
    if answer.upper() == answers[0]:
        query = make_twython_query(q, result_type, lang, count)
        print('\nGenerating Query...')
        return query
    
    elif answer.upper() == answers[1]:
        print('\nPlease re-enter your parameters.')
        q, result_type, lang, count = tweet_params()
        
        pass


def twython_script(api_key, api_key_secret, query):
    '''Accepts the arguments 'api_key' and 'api_key_secret' and a query (as a dictionary)
    and returns a pd.Dataframe containing tweets that match the query parameters.'''

    twitter = Twython(api_key, api_key_secret)
    auth = twitter.get_authentication_tokens()

    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}

    for status in twitter.search(**query)['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['text'])
        dict_['favorite_count'].append(status['favorite_count'])
    
    results = pd.DataFrame(dict_)

    return results


def generate_tweet_csv(results):
    '''Accepts a pd.DataFrame of results from Twitter API Recent Search API
    endpoint and prompts the user to choose a directory and filename. The
    pd.Dataframe is then saved to a CSV file using the selected filename.'''
    
    # choose directory
    print('Type the name of the directory where your results will be stored: ')
    print('Non-alphanumeric characters including spaces will be removed.')
    print('Hit ENTER to use the current directory.')
    directory = input()
    directory = re.sub(r'\W+', '', directory)
    
    # choose filename
    print('Type a filename for your results: ')
    print('Non-alphanumeric characters including spaces will be removed.')
    filename = input()
    filename = re.sub(r'\W+', '', filename)
    
    # generate CSV name
    csv_name = directory + '/' + filename + '.csv'

    # save results
    print('\nSaving results to ', csv_name)
    results.to_csv(str(csv_name))

def retrieve_tweets():
    print('')
    print('='*30)
    print(' Retrieve Tweets with Twython')
    print('-'*30)
    print('Enter parameters:')
    q, result_type, lang, count = tweet_params()
    print('')
    query = tweet_query_summary(q, result_type, lang, count)
    print(query)
    print('Accessing credentials...')
    CONSUMER_KEY = os.getenv('twitter_api_key')
    CONSUMER_KEY_SECRET = os.getenv('twitter_api_secret_key')

    print('\nRetrieving results...')
    results = twython_script(CONSUMER_KEY, CONSUMER_KEY_SECRET, query)
    generate_tweet_csv(results)

retrieve_tweets()
