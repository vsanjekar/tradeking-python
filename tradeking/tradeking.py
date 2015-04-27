#!/usr/bin/python

from restkit import OAuthFilter, request
import oauth2
import oauth
import urllib
import json
import types
from clint.textui import colored

import user

class TradeKing:
  auth = None

  def __init__(self, filename):
    self.user = user.TKUser()
    self.user.load_user(filename)
    self.setup_urls()
    self.setup_oauth2()

  def setup_urls(self):
    self.watchlist_url = "https://api.tradeking.com/v1/watchlists/DEFAULT.json"
    self.watchlist_symbols_url = "https://api.tradeking.com/v1/watchlist/DEFAULT/symbols.json"
    self.quote_url = 'https://api.tradeking.com/v1/market/ext/quotes.json?symbols='
    self.accounts_url = 'https://api.tradeking.com/v1/accounts.json'
    self.balance_url = 'https://api.tradeking.com/v1/accounts/'+str(self.user.acc_no)+'/balances.json'
    self.history_url = 'https://api.tradeking.com/v1/accounts/'+str(self.user.acc_no)+'/history.json?range=all&transactions=all'
    self.holdings_url = 'https://api.tradeking.com/v1/accounts/'+str(self.user.acc_no)+'/holdings.json'
    self.orders_url = 'https://api.tradeking.com/v1/accounts/'+str(self.user.acc_no)+'/orders.json'
    return

  def setup_oauth2(self):
    # set up an OAuth Consumer
    myconsumer = oauth2.Consumer(key=self.user.consumer_key, secret=self.user.consumer_secret)
    # manually update the access token/secret.
    mytoken = oauth2.Token(key=self.user.oauth_token, secret=self.user.oauth_token_secret)
    # make an oauth request
    self.auth = OAuthFilter('*', consumer=myconsumer, token=mytoken, method=oauth2.SignatureMethod_HMAC_SHA1())
    return self.auth

  def post_data(self):
    values = {'symbols' : 'IBM'}
    # data = urllib.urlencode(values)
    # req = urllib2.Request(url, data)
    # response = urllib2.urlopen(req)
    # the_page = response.read()

    # set up an OAuth Consumer
    myconsumer = oauth.Consumer(key=self.user.consumer_key, secret=self.user.consumer_secret)
    # manually update the access token/secret.
    mytoken = oauth.Token(key=self.user.oauth_token, secret=self.user.oauth_token_secret)
    client = oauth.Client(myconsumer, mytoken)
    resp, content = client.request(
                'https://api.tradeking.com/v1/watchlists.json',
                method = "GET"
                #force_auth_header=True
                )
    print resp, content
    resp, content = client.request(
                self.watchlist_symbols_url,
                method = "POST",
                body=urllib.urlencode(values),
                headers={'Content-type': 'application/json'},
                #force_auth_header=True
                )
    print resp, content
    return


  def get_data(self, url):
    # auth = setup_oauth2()
    # get the response and return it
    queryresp = request(url, 'GET', filters=[self.auth])
    queryresult = json.loads(queryresp.body_string())
    return queryresult

  def get_acc_info(self):
    query_result = self.get_data(self.accounts_url)
    print '----------------------------------------------------------------'
    print 'Account value: \t' + query_result['response']['accounts']['accountsummary']['accountbalance']['accountvalue']
    print json.dumps(query_result['response']['accounts']['accountsummary']['accountbalance'], indent=2)
    print json.dumps(query_result['response']['accounts']['accountsummary']['accountholdings'], indent=2)
    print '----------------------------------------------------------------'
    return

  def get_acc_balance(self):
    query_result = self.get_data(self.balance_url)
    # print json.dumps(query_result['response'], indent=2)
    print colored.blue('Account Balance')
    print 'Account value: \t' + query_result['response']['accountbalance']['accountvalue']
    print colored.yellow('securities:')
    # print json.dumps(query_result['response']['accountbalance']['securities'], indent=2)
    securities = query_result['response']['accountbalance']['securities']
    print 'total:   \t' + securities['total']
    print 'stocks:  \t' + securities['stocks']
    print 'options: \t' + securities['options']
    print colored.yellow('money:')
    # print json.dumps(query_result['response']['accountbalance']['money'], indent=2)
    money = query_result['response']['accountbalance']['money']
    print 'total:   \t' + money['total']
    print 'cash:    \t' + money['cash']
    print 'marginbalance: \t' + money['marginbalance']
    print colored.yellow('buyingpower:')
    if 'buyingpower' in query_result['response']['accountbalance']:
      # print json.dumps(query_result['response']['accountbalance']['buyingpower'], indent=2)
      buyingpower = query_result['response']['accountbalance']['buyingpower']
      print 'cash:    \t' + buyingpower['cashavailableforwithdrawal']
      print 'stock:   \t' + buyingpower['stock']
      print 'options: \t' + buyingpower['options']

    print '----------------------------------------------------------------'
    return

  def get_acc_holdings(self):
    query_result = self.get_data(self.holdings_url)
    holdings = query_result['response']['accountholdings']['holding']
    print colored.blue('Account Holdings')
    unrealized_total_gl = 0
    # TODO bundle the data in JSON
    for holding in holdings:
      symbol = holding['instrument']['sym']
      costbasis = float(holding['costbasis'])
      marketvalue = float(holding['marketvalue'])
      quantity = int(float(holding['qty']))
      price = float(holding['price'])
      base_price = round((costbasis/quantity), 2)
      unrealized_gl = marketvalue-costbasis
      print colored.yellow(symbol)
      print 'cost-basis:  ',costbasis,'base price:   ', base_price,'shares:',quantity
      print 'market-value:',marketvalue,'current price:',price
      if (unrealized_gl >= 0):
        print 'gain/loss:   ', colored.green(unrealized_gl)
      else:
        print 'gain/loss:   ', colored.red(unrealized_gl)
      unrealized_total_gl += unrealized_gl
    if (unrealized_total_gl >= 0):
      print colored.yellow('Total unrealized gain/loss: '), colored.green(unrealized_total_gl)
    else:
      print colored.yellow('Total unrealized gain/loss: '), colored.red(unrealized_total_gl)
    print '----------------------------------------------------------------'
    return

  def get_acc_cash_basis(self):
    print '----------------------------------------------------------------'
    query_result = self.get_data(self.history_url)
    transactions = query_result['response']['transactions']['transaction']
    psum = 0
    for i in range(len(transactions)):
      if transactions[i]['activity']=='Bookkeeping':
        if "ACH" in transactions[i]['desc']:
          # print '#%3d: %12s %30s'%(i, transactions[i]['activity'], transactions[i]['desc']), colored.yellow(transactions[i]['amount'])
          psum = psum + float(transactions[i]['amount'])
    print colored.yellow('Portfolio cash basis:'), psum
    print '----------------------------------------------------------------'
    return

  def get_acc_history(self):
    print 'Account History:\n'
    query_result = self.get_data(self.history_url)
    transactions = query_result['response']['transactions']['transaction']
    for i in range(len(transactions)):
      print '#%3d: %12s %30s'%(i, transactions[i]['activity'], transactions[i]['desc']), colored.yellow(transactions[i]['amount'])
      # print json.dumps(transactions[i], indent=2)
    return

  def get_acc_orders(self):
    print 'Balance:\n'
    query_result = self.get_data(self.orders_url)
    result = json.dumps(query_result, indent=2)
    print result
    return

  def get_acc_watchlist(self):
    query_result = self.get_data(self.watchlist_url)
    print json.dumps(query_result['response'], indent=2)

    watchlist = query_result['response']['watchlists']['watchlist']['watchlistitem']
    # print json.dumps(watchlist, indent=2)
    for watch in watchlist:
      symbol = watch['instrument']['sym']
      print symbol
      # self.get_ticker_brief(symbol)

  def get_ticker_quote(self, tickers):
    quote_url1 = self.quote_url+tickers
    query_result = self.get_data(quote_url1)
    quotes = query_result['response']['quotes']['quote']
    if type(quotes) is types.DictType:
      result = json.dumps(quotes, indent=2)
      print result
    else:
      result = json.dumps(quotes, indent=2)
      print result
    return

  def get_ticker_brief(self, tickers):
    # print tickers
    quote_url1 = self.quote_url+tickers
    query_result = self.get_data(quote_url1)
    quotes = query_result['response']['quotes']['quote']
    #result = json.dumps(query_result, indent=2)
    #print result
    if type(quotes) is types.DictType:
        print colored.yellow(quotes['symbol'] +':  ' + quotes['name'])
        print 'ask = ' + quotes['ask'] + '\t\tbid = ' + quotes['bid'] + '\t\tlast= ' + quotes['last']
        print 'lo = ' + quotes['lo'] + '\t\thi = ' + quotes['hi']
        print 'wk52lo = ' + quotes['wk52lo'] + '\twk52hi = ' + quotes['wk52hi']
        print 'adp_50 = ' + quotes['adp_50'] 
        # print 'adp_100 = ' + quotes['adp_100']
        # print quotes
    else:
      for i in range(len(quotes)):
        print colored.yellow(quotes[i]['symbol'] +':  ' + quotes[i]['name'])
        print 'ask = ' + quotes[i]['ask'] + '\t\tbid = ' + quotes[i]['bid'] + '\t\tlast= ' + quotes[i]['last'] 
        print 'lo = ' + quotes[i]['lo'] + '\t\thi = ' + quotes[i]['hi'] 
        print 'wk52lo = ' + quotes[i]['wk52lo'] + '\twk52hi = ' + quotes[i]['wk52hi']
        print 'adp_50 = ' + quotes['adp_50'] 
        # print 'adp_100 = ' + quotes['adp_100']
        # print 'volatility12 ' + quotes[i]['volatility12']
        # print quotes[i]
    return
