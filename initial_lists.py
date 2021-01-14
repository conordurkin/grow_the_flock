# This is just a script to pull the initial list of followers / followed accounts, save them down, then pull the user info for the same.

from grow_the_flock.passwords import key, secret_key, token, secret_token
import tweepy
import pandas as pd
import pickle

auth = tweepy.OAuthHandler(key, secret_key)
auth.set_access_token(token, secret_token)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


initial_followers = pd.read_csv('grow_the_flock/initial_followers.csv')
initial_friends = pd.read_csv('grow_the_flock/initial_friends.csv')

initial_followers.columns = ['name']
initial_friends.columns = ['name']

initial_followers = list(initial_followers['name'])
initial_friends = list(initial_friends['name'])

target_ids = []


# Loop over all initial followers, saving down their followers' and friends' IDs.
    # Save this all to pickle files too in case something goes wrong.

for name in initial_followers:
    try:
        user = api.get_user(name)

        if user.followers_count <= 5000:
            for follower in api.followers_ids(name):
                target_ids.append(follower)
            print("Done with followers of " + name)

        elif user.followers_count <= 100000:
            call = tweepy.Cursor(api.followers_ids, id = name)
            for page in call.pages():
                for follower_id in page:
                    target_ids.append(follower_id)
            print("Done with followers of " + name)

        else:
            print("Skipping followers of " + name)
            pass

        if user.friends_count <= 5000:
            for friend in api.friends_ids(name):
                target_ids.append(friend)
            print("Done with friends of " + name)


        elif user.friends_count <= 100000:
            call = tweepy.Cursor(api.friends_ids, id = name)
            for page in call.pages():
                for friend_id in page:
                    target_ids.append(friend_id)
            print("Done with friends of " + name)

        else:
            print("Skipping friends of" + name)
            pass

    except:
        print("Skipping user " + name + " altogether")
        pass
    with open('target_ids.pickle', 'wb') as f:
        pickle.dump(target_ds, f)

# Now, let's do it again with initial friends....

for name in initial_friends:
    try:
        user = api.get_user(name)

        if user.followers_count <= 5000:
            for follower in api.followers_ids(name):
                target_ids.append(follower)
            print("Done with followers of " + name)

        elif user.followers_count <= 100000:
            call = tweepy.Cursor(api.followers_ids, id = name)
            for page in call.pages():
                for follower_id in page:
                    target_ids.append(follower_id)
            print("Done with followers of " + name)

        else:
            print("Skipping followers of " + name)
            pass

        if user.friends_count <= 5000:
            for friend in api.friends_ids(name):
                target_ids.append(friend)
            print("Done with friends of " + name)


        elif user.friends_count <= 100000:
            call = tweepy.Cursor(api.friends_ids, id = name)
            for page in call.pages():
                for friend_id in page:
                    target_ids.append(friend_id)
            print("Done with friends of " + name)

        else:
            print("Skipping friends of" + name)
            pass

    except:
        print("Skipping user " + name + " altogether")
        pass
    with open('target_ids.pickle', 'wb') as f:
        pickle.dump(target_ds, f)


# Great, now remove any duplicates, and save this deduped list down...
unique_target_ids = list(set(target_ids))
with open('unique_target_ids.pickle', 'wb') as f:
    pickle.dump(unique_target_ids, f)


#... and finally, let's get the actual user info for all of these de-duped names.
unique_target_ids_info = []
counter = 0

for name in unique_target_ids:
    try:
        user = api.get_user(name)
        unique_target_ids_info.append(user)
        counter += 1
    except:
        counter +=1

    if counter % 5000 == 0:
        print("done with "+ str(counter))
    else:
        pass
    with open('unique_target_ids_info.pickle', 'wb') as f:
        pickle.dump(unique_target_ids_info, f)
