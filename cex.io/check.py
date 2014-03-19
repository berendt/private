#!/usr/bin/python

# author: Christian Berendt <mail@cberendt.de>

import bigfloat
import cexio
import logging
import os
import time
import yaml
import sys

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

from bigfloat import *
precision(8)

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configuration.yaml')) as configuration_file:
    configuration = yaml.load(configuration_file)

PANIC = float(configuration.get('panic'))
SELL = float(configuration.get('sell'))
STEP_SELL = float(configuration.get('step_sell'))
BUY = float(configuration.get('buy'))
STEP_BUY = float(configuration.get('step_buy'))
MINIMUM_BTC = float(configuration.get('minimum_btc'))
MINIMUM_GHS = float(configuration.get('minimum_ghs'))

logging.info("PANIC\t= %.8f" % PANIC)
logging.info("SELL\t= %.8f" % SELL)
logging.info("BUY\t= %.8f" % BUY)

try:
    conn = cexio.api(configuration.get('username'),
                     configuration.get('access_key'),
                     configuration.get('secret')
    )
except:
    logging.error("connecting to cex.io failed")
    sys.exit(1)

balance = conn.balance()
BALANCE_GHS = float(balance['GHS']['available'])
BALANCE_BTC = float(balance['BTC']['available'])

logging.info("GHS\t= %.8f" % BALANCE_GHS)
logging.info("BTC\t= %.8f" % BALANCE_BTC)

if BALANCE_BTC > MINIMUM_BTC or BALANCE_GHS > MINIMUM_GHS:
    asks = conn.order_book('GHS/BTC')['asks']
    ask = float(asks[0][0])
    bids = conn.order_book('GHS/BTC')['bids']
    bid = float(bids[0][0])
    logging.info("ASK\t= %.8f" % ask)
    logging.info("BID\t= %.8f" % bid)

    if bid > SELL or bid < PANIC:
        volume = float(bids[0][1])
        if volume > STEP_SELL:
            volume = STEP_SELL

        logging.info("selling appr. %.8f GHS for %.8f BTC at %.8f BTC/GHS" % (volume, volume * bid, bid))
        order = conn.place_order('sell', volume - 0.00001, bid, 'GHS/BTC')
        logging.info("order executed: %s" % order)

    elif ask > PANIC and ask < BUY:
        volume = float(asks[0][1])
        if volume > STEP_BUY:
            volume = STEP_BUY

        if volume * ask > BALANCE_BTC:
            volume = BALANCE_BTC / ask

        logging.info("buying appr. %.8f GHS for %.8f BTC at %.8f BTC/GHS" % (volume, volume * ask, ask))
        order = conn.place_order('buy', volume - 0.00001, ask, 'GHS/BTC')
        logging.info("order executed: %s" % order)

    else:
        logging.info("nothing to do")
