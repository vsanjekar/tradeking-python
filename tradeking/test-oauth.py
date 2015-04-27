__author__ = 'vsanjekar'

from rauth import OAuth1Service

service = OAuth1Service(
           name='tradeking',
           consumer_key='',
           consumer_secret='',
           request_token_url='https://developers.tradeking.com/oauth/request_token',
           access_token_url='https://developers.tradeking.com/oauth/access_token',
           authorize_url='https://developers.tradeking.com/oauth/authorize',
           base_url='https://api.tradeking.com/v1/')

request_token, request_token_secret = service.get_request_token()
print request_token
print request_token_secret

#authorize_url = service.get_authorize_url(request_token)
