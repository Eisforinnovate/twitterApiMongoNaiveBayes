import twitter
import json
import io
import pymongo

def oauth_login():
    
    CONSUMER_KEY = 'NQE0xRVln0KXbuNd1NJZ1cxVf'
    CONSUMER_SECRET = 'O4tjl8okFTuq70H83ovOCa7ZfKnAtcHxg2lx0rsXDSEBGUi7ag'
    OAUTH_TOKEN = '340011029-Q3AS0aXwaLihZP2emmGVnMPioCev78lPr5AHTn9t'
    OAUTH_TOKEN_SECRET = 'gQzh70Lc3eDFdsImicXOpAe36gc10ZXyqwsWd2NJb8g8K'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

def twitter_search(twitter_api, q, max_results=1000, **kw):
 
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)
    
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

twitter_api = oauth_login()
print "Authed to Twitter. Searching now..."

q = "#:("

results = twitter_search(twitter_api, q, max_results=1000)
p = "#:("
save_to_mongo(results, 'search_results', q)

results2 = twitter_search(twitter_api, p, max_results=1000)
print "Results retrieved. Saving to MongoDB..." 
save_to_mongo(results2, 'search_results', p)