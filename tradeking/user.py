#!/usr/bin/python

import json

class TKUser:
  def load_user(self, filename):
    json_fp = open(filename)
    user_data = json.load(json_fp)
    self.acc_no = user_data['user']['acc_no'].decode('utf-8')
    self.consumer_key = user_data['user']['consumer_key'].decode('utf-8')
    self.consumer_secret = user_data['user']['consumer_secret'].decode('utf-8')
    self.oauth_token = user_data['user']['oauth_token'].decode('utf-8')
    self.oauth_token_secret = user_data['user']['oauth_token_secret'].decode('utf-8')
    json_fp.close()

