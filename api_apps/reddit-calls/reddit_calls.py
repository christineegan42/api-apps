import sys
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

from datetime import datetime

import praw
from praw.models import MoreComments

import json

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
user_agent = os.getenv('user_agent')

reddit = praw.Reddit(
     client_id=client_id,
     client_secret=client_secret,
     user_agent=user_agent)


def get_submissions(submissions: list) -> (dict):
    '''Accepts a list of submissions from a subreddit and 
    stores the data fom each submission in a dictionary.
    ''' 
    results_dict = {}
    for submission in submissions:
        sub = str(submission.id)
        results_dict[sub] = {}
        results_dict[sub]['title'] = submission.title
        results_dict[sub]['selftext'] = submission.selftext
        results_dict[sub]['subreddit'] = str(submission.subreddit)
        results_dict[sub]['utc'] = submission.created_utc    
        
        results_dict[sub]['comments'] = {}
        for Comment in list(submission.comments):
            comment = reddit.comment(Comment)
            try:
                results_dict[sub]['comments'][str(comment.id)] = comment.body
            except:
                pass
            
        return results_dict
    
    
def make_api_calls(limit: int, subred: str, param: str) -> (dict):
    '''Accepts limit, a subreddit, and a search parameter (top, hot,
    or new) and retrieves the corresponding submissions.
    '''
    if param == 'top':
        submissions = reddit.subreddit(subred).top(limit=limit)
        return get_submissions(submissions)
    
    elif param == 'hot':
        submissions = reddit.subreddit(subred).hot(limit=limit)
        return get_submissions(submissions)
    
    else:
        submissions = reddit.subreddit(subred).new(limit=limit)
        return get_submissions(submissions)
    
    
def get_subred(subred: str, limit: int, param: str) -> (None):
    '''Accepts,a subreddit, a result limit, and a search parameter.
    If no data directory exists, a directory is generated. Then,
    calls are made to the reddit API and saved in a timestamped
    directory as a json. If no subreddit is found, pass.
    '''
    timestamp = str(datetime.now().time())[:8]
    datestamp = str(datetime.now().date())
    
    data_dir = make_dir('data/')
    subred_dir = make_dir(data_dir + '/' + subred + '/')
    date_dir = make_dir(subred_dir + datestamp + '/')
    file_name = date_dir + timestamp + '.json'
    
    try:
        results_dict = make_api_calls(limit, subred, param)
        print('Results obtained for r/' + subred, '.')        
        with open(file_name, 'w') as outfile:
            json.dump(results_dict, outfile)
            print('Results saved to:')
            print(file_name, '\n')
    except:
        print(subred, 'not found.\n')
        pass

    return
    


def get_subred_results(subreds: list, limit: int, param: str) -> (None):
    '''Accepts a list of subreddits, destination directory, a limit
    for search results, and the search parameter (top, hot, or new).
    API calls are made to Reddit based on those inputs. A json file
    of the results is saved to the directory.
    '''
    
    print('='*70)
    print('Retrieving Results')
    print('-'*70)
    
    for subred in subreds:
        get_subred(subred, limit, param)
        
    answers = ['Y', 'N']
    answer = input('Retrieve more results? '+ str(answers) + ': ')
    
    if answer.upper() not in answers:
        print('Input not recognized. Please enter', answers)

    elif answer.upper() == 'Y':
        subreds, limit, param = collect_inputs()
        make_query(subreds, limit, param)
        
    else:
        print('Done.')

    return


def make_query(subreds: list, limit: int, param: str) -> (None):
    '''
    Accepts a list of subreddits, a result limit, and a search param.
    The user is asked to review these query parameters. If the user 
    is satisfied, the parameters are passed on to retrieve results. 
    If not, the user is directed to re-enter.
    '''
    print('='*70)
    print('Review Your Query')
    print('-'*70)
    
    print('Subreddits:')
    print(subreds)
    print('Limit:', limit)
    print('Search Parameter:', param)
    
    answers = ['Y', 'N']
    answer = input('Are you happy with your query? '+ str(answers) + ': ')
    
    if answer.upper() not in answers:
        print('Input not recognized. Please enter', answers)

    elif answer.upper() == 'Y':
        get_subred_results(subreds, limit, param)
        
    else:
        print('\nPlease re-enter your query.\n')
        subreds, limit, param = collect_inputs()
        get_subred_results(subreds, limit, param)
        
    return 
        

def collect_inputs():
    '''Prompts the user to enter a list of subreddits, a result limit,
    and a search parameter. These query parameters are normalized and
    then passed on to generate a query.
    '''
    print('Enter a subreddit.')
    print('For multiple subreddits, seperate with a comma.')
    print('Do not include "r/" when entering.')
    subreds = input()
    subreds = subreds.replace(' ', '')
    subreds = subreds.split(',')
    
    limit = input('Enter the number of results: ')
    if limit.isalpha():
        print('Input not recognized. Please enter an integer.')
        limit = input()
    elif limit.isalpha() == False:
        limit = int(limit)
        
    params = {'1': 'top', '2': 'hot', '3': 'new'}
    print(params)
    param = input('Choose a parameter: ')           
    if param.isalpha() or int(param) not in [1,2,3]:
        print('Input not recognized. Please enter an integer.')
        param = input()
    elif param.isalpha() == False:
        param = params[param]
              
    return make_query(subreds, limit, param)
    
    
def make_dir(directory: str) -> (str):
    '''Accepts a directory name and checks the system to see if
    that directory exists. If it does not, the directory is created.
    Returns the name of the directory.
    '''
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    return str(directory)


if __name__ == '__main__':
              
    print('='*70)
    print('Make Reddit API Calls with PRAW')
    print('-'*70)

    collect_inputs()