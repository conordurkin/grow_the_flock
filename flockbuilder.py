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

# Create a list of people we have already followed. Do I need to flag the initial guys somehow? Probably.
already_followed = initial_followers.copy()







What we want to do:
1. Pull the top 100 'top targets' available.
    See if they are in the already followed list.
        if so, delete them and skip.
        if not, follow them. Add their names to the already_followed list (along with date, screenname, user info, target list it came from).
        if we can't follow them, throw them on an 'error' list of some kind.
        Add them to a 'today' list as well

2. Check our 'already followed' list for any names that are at least 14 days old.
        Check to see if they are our friend.
            If so, log them as a 'followed back!' somewhere.
            If not -> unfollow them.

3. Pull all the IDs for the 'today' list friends + followers. Make sure we don't have too many names! Skip if over 100k.
    Whittle this down to only things we haven't included in any target list or previous follows.
    Pull all bios for whatever's left. Sort them into the appropriate target lists and append them onto the end.
    Reset the 'today' list to a blank list.

4. Sleep until tomorrow morning.
