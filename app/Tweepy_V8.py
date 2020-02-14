#!/usr/bin/env

"""
Usage: run in terminal as 'python twitterspeaks.py' and follow instructions.
Requirements: tweepy

"""
import tweepy
import re
import time
import sys


# define the Twitter API parameters
class twitterAPI:
    auth = tweepy.AppAuthHandler('e2eYadHOgyP1HeYqnifGDv2za', 'JeW6SQB5tSdzol8McIPR09vzbLepQXogkf0XoTwgZY7TMzt7Dl')
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    def __init__(self, auth, api):
        self.auth = auth
        self.api = api
    # if api is not online or deactivated, throw error and exit
    if (not api):
        print("Can't Authenticate")
        sys.exit(-1)

# define our search parameters for tweets, users, or keywords
class userInput:
    # we can also predefine the search terms with this line (below)
    # searchQuery = 'trump -filter:retweets'  # this is what were searching for

    # ask user for an input, append a filter to remove retweets, which are excessive
    searchQuery = input('Enter a search term, such as a hashtag, username, or keyword: ')
    searchQuery += '-filter:retweets' + '\n'

    def __init__(self, searchQuery):
        self.searchQuery = searchQuery

# tweet info - required for tweepy to continue skimming
class tweetInfo:
    tweetCount = 0
    maxTweets = 10000000  # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1
    def __init__(self, tweetCount, maxTweets, tweetsPerQry, sinceID, max_id):
        self.tweetCount = tweetCount
        self.maxTweets = maxTweets
        self.tweetsPerQry = tweetsPerQry
        self.sinceId = sinceID
        self.max_id = max_id

# the main function
class main(object):
    def run(self):
        while tweetInfo.tweetCount < tweetInfo.maxTweets:
            try:
                if (tweetInfo.max_id <= 0):
                    # run api search using Twitter's terms for the text we want
                    if (not tweetInfo.sinceId):
                        # using extended tweet ensures we see everything beyond 140 characters (240 max)
                        new_tweets = twitterAPI.api.search(q=userInput.searchQuery, count=tweetInfo.tweetsPerQry, tweet_mode='extended')
                    else:
                        new_tweets = twitterAPI.api.search(q=userInput.searchQuery, count=tweetInfo.tweetsPerQry,
                                                    since_id=sinceId, tweet_mode='extended')
                else:
                    if (not sinceId):
                        new_tweets = twitterAPI.api.search(q=userInput.searchQuery, count=tweetInfo.tweetsPerQry,
                                                    max_id=str(tweetInfo.max_id - 1), tweet_mode='extended')
                    else:
                        new_tweets = twitterAPI.api.search(q=userInput.searchQuery, count=tweetInfo.tweetsPerQry,
                                                    max_id=str(tweetInfo.max_id - 1),
                                                    since_id=sinceId, tweet_mode='extended')
                # if there are no more tweets to display, end the stream
                if not new_tweets:
                    print("No tweets found")
                    break
                # initialize the tweet list
                tweet_list = []
                for tweet in new_tweets:
                    tweet_list.append(tweet._json)
                    # tweet.user gets ALL the data
                    name = str(tweet.user.screen_name)
                    date = str(tweet.user.created_at)
                    for i in range(len(tweet_list)):
                        full_stream = tweet_list[i].get("full_text") + '\n'
                        results = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|(\r\n|\r)', '', full_stream)
                    final = "At " + date + '\n' + name + " said:" + '\n' + results
                    print(final)
                    time.sleep(2)

                tweetInfo.tweetCount += len(new_tweets)

                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:  
                print("Error: " + str(e))
                break
            except KeyboardInterrupt:
                # Or however you want to exit this loop
                print('\n' + 'User ended stream')
                break
            except (EOFError, SyntaxError, ValueError):
                print('\n')
                break


if __name__ == '__main__':
    main().run()
