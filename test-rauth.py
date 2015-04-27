__author__ = 'vsanjekar'

from rauth import OAuth1Service
import json

service = OAuth1Service(
           name='tradeking',
           consumer_key='',
           consumer_secret='')

oauth_token = ''
oauth_token_secret = ''


oauth_session = service.get_session(token=(oauth_token, oauth_token_secret))

print "All watch lists:"
url = 'https://api.tradeking.com/v1/watchlists.json'
r = oauth_session.get(url)
# print type(r)
print r
print r.content

watchlist = 'test'
print "Create watchlist"
url = 'https://api.tradeking.com/v1/watchlists.json'
r = oauth_session.post(url, data={'id': watchlist, 'symbols': 'AAPL'})
print r
print r.content

print "Add symbols to watchlist"
url = 'https://api.tradeking.com/v1/watchlists/'+watchlist+'/symbols.json'
r = oauth_session.post(url, data={'symbols': 'FB'})
print r
print r.content

print "Watchlist contents"
url = 'https://api.tradeking.com/v1/watchlists/'+watchlist+'.json'
r = oauth_session.get(url)
print r
print r.content
# print json.dumps(json.loads(r.content), indent=2, sort_keys=True)

print "Delete watchlist"
url = 'https://api.tradeking.com/v1/watchlists/'+watchlist+'.json'
r = oauth_session.delete(url)
print r
print r.content

print "All watch lists:"
url = 'https://api.tradeking.com/v1/watchlists.json'
r = oauth_session.get(url)
print r
print r.content