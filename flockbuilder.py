# Import twitter, import relevant authentication codes from password file
import tweepy
from passwords import key, secret_key, token, secret_token

#Authenticate to Twitter
auth = tweepy.OAuthHandler(key, secret_key)
auth.set_access_token(token, secret_token)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)








# THINGS TO DO:
# 1. Store my 'base' list of followers and followed accounts.
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
