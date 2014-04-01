#!/usr/bin/python2

# author: Christian Berendt <mail@cberendt.de>

import logging
from mechanize import Browser
import os
import re
from random import randint
import urllib
import yaml

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

def getIdent():
    ident = "%04d_%013d" % (randint(1, 9999), randint(1, 9999999999999))
    return ident

def initialize(username, password):
    browser = Browser()
    browser.open('https://www.save.tv')
    browser.select_form(nr=0)
    browser.form["sUsername"] = username
    browser.form["sPassword"] = password
    browser.submit()
    return browser

def getAllTids(browser, number):
    logging.debug("fetching TIDs from the first %d index pages" % number)
    tids = []
    for number in xrange(1, number + 1):
        logging.debug("requesting index page %d" % number)
        url = "/STV/M/obj/user/usShowVideoArchive.cfm?iPageNumber=%d&bLoadLast=1" % number
        response = browser.open(url)
        logging.debug("extracting TIDs of movies on index page %d" % number)
        tids = tids + getAllMovies(response.get_data())
        logging.debug("extracting names of series on index page %d" % number)
        tids = tids + getAllEpisodes(browser, response.get_data())

    logging.debug("found %d TIDs" % len(tids))
    return set(tids)

def getAllMovies(data):
    tids = []
    for tid in re.findall(r'TelecastID=(\d+)', data):
        if not tid in tids:
            tids.append(tid)

    return tids

def getAllEpisodes(browser, data):
    tids = []
    for serie in re.findall(r'data-title="(.*)"', data):
        logging.debug("requesting episodes of serie %s" % serie)
        url = ('/STV/M/obj/user/usShowVideoArchiveLoadEntries.cfm?null.GetVideoEntries&ajax=true&clientAuthenticationKey=&callCount=1&c0-scriptName=null'
               '&c0-methodName=GetVideoEntries&c0-id=' + getIdent() + '&c0-param0=string:1&c0-param1=string:&c0-param2=string:1&c0-param3=string:999999'
               '&c0-param4=string:1&c0-param5=string:0&c0-param6=string:1&c0-param7=string:0&c0-param8=string:1&c0-param9=string:'
               '&c0-param10=string:' + serie + '&c0-param11=string:6&c0-param12=string:toggleSerial&xml=true'
              )

        url = url.replace(' ', '%20')
        response_episodes = browser.open(url)

        logging.debug("extracting TIDs of episodes of serie %s" % serie)
        for tid in re.findall(r'TelecastID=(\d+)', response_episodes.get_data()):
            if not tid in tids:
                tids.append(tid)

    return tids

def getUrlAndFilenameByTid(browser, tid):
    logging.debug("requesting url, filename and filesize of TID %s" % tid)
    url = ('/STV/M/obj/cRecordOrder/croGetAdFreeAvailable.cfm?null.GetAdFreeAvailable&=&ajax=true&c0-id='
           '' + getIdent() + '&c0-methodName=GetAdFreeAvailable&c0-param0=number%3A'
           '' + tid + '&c0-scriptName=null&callCount=1&clientAuthenticationKey=&xml=true'
          )
    response = browser.open(url)
    status = re.search("_\d+_\d+ = '(\d)';", response.get_data()).group(1)
    if not int(status) == 1:
        logging.debug("skipping TID %s, no advertise-free version available at the moment" % tid)
        return(None, None, None)

    url = ('/STV/M/obj/cRecordOrder/croGetDownloadUrl.cfm?null.GetDownloadUrl&ajax=true&c0-id='
           '' + getIdent() + '&c0-methodName=GetDownloadUrl&c0-param0=number%3A'
           '' + tid + '&c0-param1=number%3A0&c0-param2=boolean%3Atrue&c0-scriptName=null&callCount=1&clientAuthenticationKey=&xml=true'
          )
    response = browser.open(url)
    url = re.search("(http://[^']*?m=dl[^']*)", response.get_data()).group()
    d = urllib.FancyURLopener().open(url)
    filename = d.headers['Content-Disposition'].split("filename=")[1]
    filesize = d.headers['Content-Length']
    d.close()
    logging.debug("TID=%s, URL=%s" % (tid, url))
    logging.debug("TID=%s, FILENAME=%s" % (tid, filename))
    logging.debug("TID=%s, FILESIZE=%s" % (tid, filesize))
    return (url, filename, filesize)

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configuration.yaml')) as configuration_file:
    configuration = yaml.load(configuration_file)

browser = initialize(configuration.get('username'), configuration.get('password'))

result = {}
for tid in getAllTids(browser, 3):
    try:
        url, filename, filesize  = getUrlAndFilenameByTid(browser, tid)
    except:
        continue
    if not url is None:
        print "%s %s %s" % (filename, url, tid)
