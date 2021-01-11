# This is a file just to test whether we can log in on Twitter properly. 

import tweepy

# Save a file containing the Key, Secret Key, and Token for Twitter access. Contains these variables and nothing else.
from passwords import key, secret_key, token, secret_token

# Testing authentication to Twitter
auth = tweepy.OAuthHandler(key, secret_key)
auth.set_access_token(token, secret_token)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
