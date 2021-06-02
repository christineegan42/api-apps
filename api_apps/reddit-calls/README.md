# reddit-calls
A CLI app to make Reddit API calls using PRAW.

### About
Use reddit-calls to make API calls to Reddit from the command line using PRAW. Once installed, reddit-calls will allow you to retrieve results from subreddits of your choice. Simply enter the list of subreddits, the number of results that you wish to retrieve, and a search parameter (hot, top, or new) and a JSON file of the results will saved to the directory.

### Before installation:
Create a Reddit account and request credentials. Keep this information handy, because you will need it for installation.

### Installation:
1. Clone this repository.
2. Establish a virtual environment in the reddit_calls directory.
3. Install requirements.txt.
4. Open the file called 'example_creds.txt'. Replace the hashes with your Reddit API credentials. Rename the file '.env'. 

### Making API Calls
1. Launch reddit_calls.py OR open reddit_calls.ipynb and "Run all."
2. Respond to the prompts to generate your query.
  * subreddits: one or more subreddits
  * limit: the number of submissions (posts) to return from each subreddit
  * search parameter: top (most popular), new (most recent), hot (most activity)
3. Your results will be saved in reddit_calls/data. A new folder will be created for each subreddit. Results will be saved in a time-stamped file in a date-stamped directory in the subreddit folder.

### Coming Soon
Expanded search parameters.
Additional functionality to unpack the results.
