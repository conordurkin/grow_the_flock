# grow_the_flock

This repo contains the code to build and run a Twitter bot.
The twitter bot is intended to help my e-commerce website by following potential customers (getting their attention).
My intended use is to simply schedule this to run as a cron job every morning, but one could find other ways to deploy.

We have two setup files: initial_list_setup_1.py and initial_list_setup_2.py.

*Setup 1* reads in two CSV files (initial friends + initial followers), which are lists of the IDs of current friends/followers on Twitter.
It then pulls all friends + follower IDs of those IDs (unless an account has more than 100,000 followers, since that would take too long a time. This is the "Pope Francis" rule.)
We dedup the list, then pull user info for all of those new IDs and store them in a pickle file.

*Setup 2* reads in the pickle file, generates the keywords we're looking for in users' bios to be deemed a 'potential customer' (or 'target'), and stores the target lists as pickle files.

*Flockbuilder* is the file that runs the ongoing Twitter bot.
It reads in the target list pickle files plus one additional CSV for logging info (followed_log.csv).
It then follows 100 accounts from the target lists, pulls all of their friends + followers and classifies them as potential targets appropriately, and finally unfollows any account we followed 14 days prior who has not followed us back. It saves down information on who we have followed in the followed_log.csv file.

*API Testing* was the file I used to check whether I could get on Twitter appropriately with my credentials. It doesn't serve any purpose in the actual app.

Beyond these three files, there are two other files one needs to make the bot run:
1. A password file, entitled 'password.py', containing the appropriate Twitter credentials.
2. A CSV file, entitled 'followed_log.csv', which stores info about followed accounts. I think this could be initialized with a blank file and only headings, if desired.
   It has five columns: ID (from Twitter)
                        Description (from Twitter)
                        List (source of target)
                        Date (date followed)
                        Flag (blank at first, 1/0 after 14 days based on if they followed back)
