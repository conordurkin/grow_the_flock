# This is going to be the file that runs daily and logs lots of info for me.


### First Section: Basic Setup ###

# Import twitter, import relevant authentication codes from password file
import tweepy
from passwords import key, secret_key, token, secret_token
import pandas as pd
from datetime import datetime as dt
today = dt.today().strftime("%Y-%m-%d")


#Authenticate to Twitter and get API connected
auth = tweepy.OAuthHandler(key, secret_key)
auth.set_access_token(token, secret_token)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


### Second Section: Getting today's targets and following them ###

# Read in our followed log (CSV / DataFrame) and our lists of potential targets (Pickles / Lists of Lists)
followed_log = pd.read_csv('followed_log.csv')
with open('mid_targets.pickle', 'rb') as f:
    mid_targets = pickle.load(f)
with open('top_targets.pickle', 'rb') as f:
    top_targets = pickle.load(f)
with open('low_targets.pickle', 'rb') as f:
    low_targets = pickle.load(f)

# Select today's targets and remove them from the lists.
today_top_targets_temp = top_targets[0:50]
today_mid_targets_temp = mid_targets[0:50]
top_targets = top_targets[50:]
mid_targets = mid_targets[50:]
today_targets = []

for target in today_top_targets_temp:
    if target[0] in list(followed_log.id):
        pass
    else:
        today_targets.append(target + ['top_target', today, ''])

for target in today_mid_targets_temp:
    if target[0] in list(followed_log.id):
        pass
    else:
        today_targets.append(target + ['mid_target', today, ''])

# Connect to Twitter and follow today's targets. Log them if we are able follow them.
for target in today_targets:
    try:
        api.create_friendship(target[0])
        new_row = pd.Series(target, index=followed_log.columns)
        follower_log.append(new_row)

    except:
        pass


### Third Section: Replenishing our Target Lists by pulling followers/friends from Today's Targets ###

# Get list of follower IDs / friend IDs for the new people we're pulling.
new_targets = []
for target in today_targets:
    name = target[0]
    try:
        user = api.get_user(name)
        if user.followers_count <= 5000:
            for follower in api.followers_ids(name):
                new_targets.append(follower)
        elif user.followers_count <= 100000:
            call = tweepy.Cursor(api.followers_ids, id = name)
            for page in call.pages():
                for follower_id in page:
                    new_targets.append(follower_id)
        else:
            pass

        if user.friends_count <= 5000:
            for friend in api.friends_ids(name):
                new_targets.append(friend)
        elif user.friends_count <= 100000:
            call = tweepy.Cursor(api.friends_ids, id = name)
            for page in call.pages():
                for friend_id in page:
                    new_targets.append(friend_id)
        else:
            pass

    except:
        pass

# Filter down that list of new target IDs. Eliminate anyone we already have seen.
new_targets = list(set(new_targets))
old_targets = [target[0] for target in low_targets] + [target[0] for target in mid_targets] + [target[0] for target in top_targets]
brand_new_targets = [target for targets in new_targets if target not in old_targets]

# Keywords to classify accounts into one of the good lists.
bio_top = ['chaplain', 'fr.', 'pastor', 'seminarian', 'priest', 'vicar', 'diocese']
bio_mid = ['friar', 'catholic', 'jesuit', 'dominican', 'franciscan', 'parish']

# Pull bios for anyone on the brand_new_targets lists.
def divide_list(list, n):
    for i in range(0, len(list), n):
        yield list[i:(i+n)]

chunky_new_targets = list(divide_list(brand_new_targets, 100))
new_target_info = []

for chunk in chunky_new_targets:
    try:
        users = api.lookup_users(chunk)
        for user in users:
            new_target_info.append(user.id, user.description)
    except:
        pass

# Now determine which accounts go into which list.
for account in new_target_info:
    if any(word in account.description.lower() for word in bio_top):
        top_targets.append(account)
    elif any(word in account.description.lower() for word in bio_mid):
        mid_targets.append(account)
    else:
        low_targets.append(account)

# And store these target lists down as pickle files.
with open('top_targets.pickle', 'wb') as f:
    pickle.dump(top_targets, f)
with open('mid_targets.pickle', 'wb') as f:
    pickle.dump(mid_targets, f)
with open('low_targets.pickle', 'wb') as f:
    pickle.dump(low_targets, f)


### Fourth Section: Unfollowing Accounts if they never follow us back ###
lookback = (dt.today() - timedelta(14)).strftime("%Y-%m-%d")

unfollow_candidates = followed_log.loc[followed_log.date == lookback]

follower_list = []
for follower in tweepy.Cursor(api.followers).items():
    follower_list.append(follower.id)



########################################################
Still to do:

        Check to see if they are our friend.
            If so, log them as a 'followed back!' somewhere.
            If not -> unfollow them.
