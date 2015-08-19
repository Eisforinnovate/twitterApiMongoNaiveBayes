import json
import io
import pymongo
import tweepy
import OAuth
from tweepy.auth import OAuthHandler


def oauth_login():
    
    CONSUMER_KEY = '###w'
    CONSUMER_SECRET = '###'
    OAUTH_TOKEN = '####'
    OAUTH_TOKEN_SECRET = '###'
    
    #auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
     #                          CONSUMER_KEY, CONSUMER_SECRET)
    
    #auth = tweepy.OAuthHandler(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,

    dir(tweepy)
    auth= tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    return tweepy.API(auth)
    #twitter_api = twitter.Twitter(auth=auth)
    #return twitter_api

def twitter_search(twitter_api, q, max_results=10, **kw):
 
    #search_results = twitter_api.search.tweets(q=q, count=100, max_results=max_results)
    
    search_results = twitter_api.search(q=q)

    texts = [s.text.encode('utf8') for s in search_results]
    return texts

    return

    statuses = search_results['statuses']

    max_results = min(1000, max_results)
    tweet_count = 0

    for _ in range(10):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: 
            break
            
        kwargs = dict([ kv.split('=') 
                        for kv in next_results[1:].split("&") ])
        
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        
        tweet_count += 100
        print tweet_count
        
        if len(statuses) > max_results: 
            break
            
    return statuses

def save_to_mongo(data, mongo_db, mongo_db_coll, **mongo_conn_kw):
    
    client = pymongo.MongoClient(**mongo_conn_kw)
    db = client[mongo_db]
    coll = db[mongo_db_coll]
    
    return coll.insert(data)


tweep = oauth_login()
print "Authed to Twitter. Searching now..."

q = '%23%3A('

results = twitter_search(twitter_api, q, max_results=10)
p = '#:('
save_to_mongo(results, 'search_results', q)

results2 = twitter_search(twitter_api, p, max_results=10)
print "Results retrieved. Saving to MongoDB..." 
save_to_mongo(results2, 'search_results', p)