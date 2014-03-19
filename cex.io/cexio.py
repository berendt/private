# -*- coding: utf-8 -*-

## Author:	t0pep0
## e-mail:	t0pep0.gentoo@gmail.com
## Jabber:	t0pep0@jabber.ru
## BTC   :	1ipEA2fcVyjiUnBqUx7PVy5efktz2hucb
## donate free =)

#  source: https://github.com/matveyco/cex.io-api-python
# license: The MIT License (MIT) (https://github.com/matveyco/cex.io-api-python/blob/master/LICENSE)

import hashlib
import hmac
import json
import random
import time
import urllib
import urllib2

class api:
    __username = None;
    __api_key = None;
    __api_secret = None;
    __nonce_v = None;

    def __init__(self, username, api_key, api_secret):
        self.__username = username
        self.__api_key = api_key
        self.__api_secret = api_secret

    def __nonce(self):
        if not self.__nonce_v:
            self.__nonce_v = int(str(time.time()).split('.')[0])
        else:
            self.__nonce_v += 1

    def __signature(self):
        string = str(self.__nonce_v) + self.__username + self.__api_key
        signature = hmac.new(self.__api_secret, string, digestmod=hashlib.sha256).hexdigest().upper()
        return signature

    def __post(self, url, param):
        params = urllib.urlencode(param)
        req = urllib2.Request(url, params, {'User-agent': 'bot-cex.io-'+self.__username})
        page = urllib2.urlopen(req).read()
        return page;
 
    def api_call(self, method, param = {}, private = 0, couple = ''):
        url = 'https://cex.io/api/'+method+'/'

        if couple != '': 
            url = url + couple + '/'
        if private == 1:
            self.__nonce()

        param.update({
            'key' : self.__api_key,
            'signature' : self.__signature(),
            'nonce' : str(self.__nonce_v)}
        )

        return json.loads(self.__post(url, param))
 
    def ticker(self, couple = 'GHS/BTC'):
        return self.api_call('ticker', {}, 0, couple)

    def order_book(self, couple = 'GHS/BTC'):
        return self.api_call('order_book', {}, 0, couple)

    def trade_history(self, since = 1, couple = 'GHS/BTC'):
        return self.api_call('trade_history', {"since" : str(since)}, 0, couple)

    def balance(self):
        return self.api_call('balance', {}, 1)

    def current_orders(self, couple = 'GHS/BTC'):
        return self.api_call('open_orders', {}, 1, couple)

    def cancel_order(self, order_id):
        return self.api_call('cancel_order', {"id" : order_id}, 1)
 
    def place_order(self, ptype = 'buy', amount = 1, price = 1, couple = 'GHS/BTC'):
        return self.api_call('place_order', {"type" : ptype, "amount" : str(amount), "price" : str(price)}, 1, couple)
