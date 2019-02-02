import json
import tweepy

API_KEY = 'kEgIQct9vhC3VI81CzA018LCP'
API_KEY_SECRET = 'aWZB24sCd4YmCYJT8EstnPLIJemRinWYQ3SHcR8dnETJlp0RLJ'

ACCESS_TOKEN = '817167849357615104-sTE4VvShmAbxyVNOFqdngfu8pl1onRT'
ACCESS_TOKEN_SECRET = '14MlBjPpNUy1IjFpv7RwksgJTOae6DVlac8fNbduY9S9E'

# Setup authorization
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

search_q = input("Enter the search query: ")
search_results = api.search(q=search_q)

for content in search_results:
    print(content.text)
