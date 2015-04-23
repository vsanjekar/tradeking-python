#!/usr/bin/python

# CLI interface to tradking account and stock quotes.
# Author: Vinay Sanjekar

import sys
import os, argparse
from pprint import pprint

import tradeking.tradeking

argparser = argparse.ArgumentParser(description='tradeking-cli')
argparser.add_argument('-a','--all', help='All information', action="store_true", default=False)
argparser.add_argument('-b','--brief', help='Brief information', action="store_true", default=True)
argparser.add_argument('-l','--log', help='Account log', action="store_true", default=False)
argparser.add_argument('-o','--orders', help='Account log', action="store_true", default=False)
argparser.add_argument('-p','--portfolio', help='Portfolio information', action="store_true", default=False)
argparser.add_argument('-s','--symbol', help='Ticker symbol')
argparser.add_argument('-u','--user', help='User file')
argparser.add_argument('-w','--watchlist', help='Wishlists', action="store_true", default=False)
options = vars(argparser.parse_args())

print options

# TradeKing commands
# user config from command line
if options['user']:
  tk = tradeking.tradeking.TradeKing(options['user'])
else:
  tk = tradeking.tradeking.TradeKing('user.json')

# "./tradeking-cli.py.py -p"
if options['portfolio']:
  # tk.get_acc_info()
  tk.get_acc_cash_basis()
  tk.get_acc_balance()
  tk.get_acc_holdings()
# "./tradeking-cli.py.py -w"
elif options['watchlist']:
  tk.get_acc_watchlist()
# "./tradeking-cli.py.py -l"
elif options['log']:
  tk.get_acc_history()
# "./tradeking-cli.py.py tk -o"
elif options['orders']:
  tk.get_acc_orders()
elif options['symbol'] is not None:
  # "./tradeking-cli.py.py -s TRLA -a"
  if options['all']:
    tk.get_ticker_quote(options['symbol'])
  # "./tradeking-cli.py.py tk -s TRLA -b"
  elif options['brief']:
    tk.get_ticker_brief(options['symbol'])
