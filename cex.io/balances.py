#!/usr/bin/python

# author: Christian Berendt <info@cabtec.net>

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

try:
    conn = cexio.api(configuration.get('username'),
                     configuration.get('access_key'),
                     configuration.get('secret')
    )
except Exception, e:
    logging.error("connecting to cex.io failed: %s" % e)
    sys.exit(1)

balance = conn.balance()

BALANCE_GHS = float(balance['GHS']['available'])
BALANCE_BTC = float(balance['BTC']['available'])

logging.info("GHS\t= %.8f" % BALANCE_GHS)
logging.info("BTC\t= %.8f" % BALANCE_BTC)
