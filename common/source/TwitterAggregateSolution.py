# For Twitter API
import tweepy

# For Dataframe
import json
import pandas as pd

# For loading the model
import pickle
from sklearn.feature_extraction.text import CountVectorizer as CV

# For OS related operations
import os

from Access import Tokens

# Authorization Keys - Dolcevice
API_KEY = Tokens.API_KEY
API_KEY_SECRET = Tokens.API_KEY_SECRET
ACCESS_TOKEN = Tokens.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = Tokens.ACCESS_TOKEN_SECRET
# Variables when acquiring the data from Twitter API
MAX_TWEETS = 1000
s_query = 'Cats'
# Create API instance
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


# Method for cleaning a dataframe
def clean_twitter_dataframe(frame):
    frame.columns.str.rstrip('.!? \n\t')
    frame.replace('\n', '', regex=True, inplace=True)
    frame.replace('tco.{10}', '', regex=True, inplace=True)
    frame.replace('tco', '', regex=True, inplace=True)
    frame.replace('https:.{13}', '', regex=True, inplace=True)
    frame.replace('https:', '', regex=True, inplace=True)
    frame.replace('[,\.!?/|_]', '', regex=True, inplace=True)
    frame.replace(r'RT.*:', '', regex=True, inplace=True)
    frame.replace(r'\b\w{1,2}\b', '', regex=True, inplace=True)
    frame.replace('@.* \s', '', regex=True, inplace=True)


def drop_dfcolumns(frame):
    frame = frame.drop(
        ['contributors', 'coordinates', 'entities', 'extended_entities', 'favorited', 'geo', 'id', 'id_str',
         'in_reply_to_screen_name', 'in_reply_to_status_id'
            , 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'is_quote_status',
         'possibly_sensitive', 'quoted_status_id',
         'quoted_status_id_str', 'retweeted', 'source', 'user', 'place', 'retweeted_status'], axis=1)
    frame.drop_duplicates(subset='text', keep='first', inplace=True)


if __name__ == "__main__":
    # Create a search cursor
    search_cursor = tweepy.Cursor(api.search, q=s_query, lang='en').items(MAX_TWEETS)

    # Create a temporary JSON file
    for tweet in search_cursor:
        with open('tweet_dump.json', 'a') as file:
            file.write(json.dumps(tweet._json))
            file.write('\n')

    # Create a dataframe by opening the temporary json file
    tweet_df = pd.read_json('tweet_dump.json', lines=True)
    drop_dfcolumns(tweet_df)
    clean_twitter_dataframe(tweet_df)

    str_dump = tweet_df['text'].to_string()
    str_dump_clean = []
    for line in str_dump:
        str_dump_clean.append(line)

    # Remove temporary file
    os.remove('tweet_dumps.json')

    # Load a model
    # LogReg
    logreg_in = open('logreg.model.sav', 'rb')
    logreg_model = pickle.load(logreg_in)

    # Test it on the dump
    Y_test = CV.transform(str_dump_clean)
    result = logreg_model.predict(Y_test)
    result_df = pd.DataFrame({'Value': result})

    # Take its average
    result_average = result_df.mean(axis=0)
    result_average = round(float(result_average), 3)

    print('Analysis of %s : %s find it favorable', (s_query, result_average))
