# Setup File Number 2
# This processes and sorts the lists pulled from initial_lists.py

# Import twitter, import relevant authentication codes from password file
import tweepy
from passwords import key, secret_key, token, secret_token
import pandas as pd
from datetime import datetime as dt


#Authenticate to Twitter
auth = tweepy.OAuthHandler(key, secret_key)
auth.set_access_token(token, secret_token)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Import lists of initial friends and followers
initial_followers = pd.read_csv('initial_followers.csv')
initial_friends = pd.read_csv('initial_friends.csv')

initial_followers.columns = ['name']
initial_friends.columns = ['name']

initial_followers = list(initial_followers['name'])
initial_friends = list(initial_friends['name'])


##### Creating initial target set.

# First create lists of 'priority keywords' in Twitter bios/descriptions to classify potential targets.
bio_top = ['chaplain', 'fr.', 'pastor', 'seminarian', 'priest', 'vicar', 'diocese']
bio_mid = ['friar', 'catholic', 'jesuit', 'dominican', 'franciscan', 'parish']


# Read in information on our targets - this is a big dataset! We're going to pull bio information to classify them.
with open('unique_targets_ids_info.pickle', 'rb') as f:
    initial_targets = pickle.load(f)

top_targets = []
mid_targets = []
low_targets = []

for account in initial_targets:
    if any(word in account.description.lower() for word in bio_top):             # !!! Note: Need to get the syntax right to pull the account descriptions here...
        top_targets.append(account)
    elif any(word in account.description.lower() for word in bio_mid):
        mid_targets.append(account)
    else:
        low_targets.append(account)
