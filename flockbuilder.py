# Import twitter, import relevant authentication codes from password file
import tweepy
from passwords import key, secret_key, token, secret_token

#Authenticate to Twitter
auth = tweepy.OAuthHandler(key, secret_key)
auth.set_access_token(token, secret_token)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
