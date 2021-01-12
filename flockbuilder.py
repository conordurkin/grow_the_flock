# Import twitter, import relevant authentication codes from password file
import tweepy
from passwords import key, secret_key, token, secret_token
import pandas

#Authenticate to Twitter
auth = tweepy.OAuthHandler(key, secret_key)
auth.set_access_token(token, secret_token)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Create lists of initial friends + followers
initial_followers = []
initial_friends = []
for follower in tweepy.Cursor(api.followers).items():
    initial_followers.append(follower.screen_name)

blacklist = ['condurkin', 'shopify','johnnyphonecall', 'pontifex', 'mgdurkin', 'pcallahan91']

# add some logic skipping an account if follower/followed count is > 100k 





for friend in tweepy.Cursor(api.friends).items():
    initial_friends.append(friend.screen_name)

# Create lists of 'priority keywords'
bio_top = ['chaplain', 'fr.', 'pastor', 'seminarian', 'priest', 'vicar', 'diocese']
bio_mid = ['friar', 'brother', 'catholic', 'jesuit', 'dominican', 'franciscan', 'parish']

targets = []
# Create list of all followers of followers:
for follower in tweepy.Cursor(api.followers).items():
    for grand_follower in tweepy.Cursor(follower.followers).items():
        targets.append(grand_follower)



# THINGS TO DO:
#DONE   1. Store my 'base' list of followers and followed accounts.

                # 2. Generate a list of the people I'd like to try following.
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
