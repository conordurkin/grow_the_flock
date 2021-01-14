# Import twitter, import relevant authentication codes from password file
import tweepy
from passwords import key, secret_key, token, secret_token
import pandas as pd

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


# Read in information on our targets - this is a big list! We're going to pull bio information to classify them.
initial_targets = pd.read_csv('initial_targets.csv')

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







# THINGS TO DO:
#DONE   1. Store my 'base' list of followers and followed accounts.

                #     - Ideas: Suggested accounts, followers of followers, followers of followed, followed of followed, followed of followers, specific hashtags, specific bios?
                # 3. Record list of those people.
                # 4. Follow top 50 in a day
                # 5. Store the 50 new follows along with the date.
                # 6. Sleep for a day.
                # 7. Follow another 50, store in list, sleep.
                # 8. After [N] days, check list of followers for guys from step 5.
                #     If no -> unfollow. Log as unsuccessful.
                #     If yes -> stay following.
                # 9. Logic for who to follow should now check against the unsuccessful list too - don't wanna refollow anytime soon.
#
