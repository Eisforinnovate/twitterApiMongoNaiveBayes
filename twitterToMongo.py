import base64
import requests
import json

CONSUMER_KEY="####"
CONSUMER_SECRET="####"

payload = CONSUMER_KEY + ":" + CONSUMER_SECRET
payload64 = base64.encodestring(payload).replace('\n','')

body = "grant_type=client_credentials"
url = "https://api.twitter.com/oauth2/token"
headers = {'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                      'Authorization': "Basic %s" % payload64}
result = requests.post(url, data=body, headers=headers)

bearer_token = json.loads(result.text)['access_token']

result_happy = requests.get(
    'https://api.twitter.com/1.1/search/tweets.json',
    params={'q':'#:)'},
    headers={'Authorization': "Bearer %s" % bearer_token}
)
result_depressed = requests.get(
    'https://api.twitter.com/1.1/search/tweets.json',
    params = {'q': '#:('},
    headers={'Authorization', 'Bearer %s' % bearer_token}
)
import pymongo
import json
dbc=pymongo.MongoClient('localhost', 27017)
db = dbc['twits']
col=db['positive']
depressed=db['depressed']
jshappy = json.loads(result_happy.text)
jssad = json.loads(result_depressed.text)

for status in jshappy['statuses']:
    txt = status.text
    col.insert_one({'text':txt})
for status in jssad['statuses']:
    txt = status.text
    depressed.insert_one({'text':txt})