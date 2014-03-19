#!/usr/bin/python

# author: Christian Berendt <info@cberendt.de>

import logging
from mechanize import Browser
import os
import sys
import urllib
import yaml

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

def initialize(username, password):
    browser = Browser()
    browser.open('https://www.save.tv')
    browser.select_form(nr=0)
    browser.form["sUsername"] = username
    browser.form["sPassword"] = password
    browser.submit()

    return browser

try:
    tid = sys.argv[1]
except IndexError:
    print("usage: %s TID" % sys.argv[0])
    sys.exit(1)

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configuration.yaml')) as configuration_file:
    configuration = yaml.load(configuration_file)

data = urllib.urlencode({'lTelecastID' : tid})
browser = initialize(configuration.get('username'), configuration.get('password'))
browser.open("/STV/M/obj/user/usShowVideoArchive.cfm", data)

logging.info("%s deleted" % tid)
