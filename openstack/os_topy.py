#!/usr/bin/python

# author: Christian Berendt <berendt@b1-systems.de>

# Based on the idea of 'Topy' written by Marti Raudsepp <marti@juffo.org>. 
# Topy is available on Github at https://github.com/intgr/topy.

import argparse
import cPickle as pickle
import logging
import os
import regex
import shutil
import sys
import urllib
from bs4 import BeautifulSoup

def download_listing(dest):
    logger = logging.getLogger('os_topy')
    url = 'https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos?action=raw'
    logger.debug("downloading latest RETF listing from %s into %s" % (url, dest))
    urllib.urlretrieve (url, dest)

def soupify_listing(src):
    return BeautifulSoup(open(src))

def write_listing_to_cache(listing, dest):
    logger = logging.getLogger('os_topy')
    logger.debug("dumping listing into cache file %s" % dest)
    pickle.dump(listing, open(dest, 'wb'))

def load_listing_from_cache(src):
    logger = logging.getLogger('os_topy')
    logger.debug("loading listing from cache file %s" % src)
    result = pickle.load(open(src, 'rb'))
    logger.debug("%d rules loaded from %s" % (len(result), src))
    return result

def generate_listing(src):
    logger = logging.getLogger('os_topy')
    listing = []

    soup = soupify_listing(src)

    for typo in soup.findAll('typo'):
        word = typo.attrs.get('word').encode('utf8')
        find = typo.attrs.get('find').encode('utf8')
        replace = typo.attrs.get('replace').encode('utf8')
        replace = replace.replace(b'$', b'\\')

        logger.debug("compiling regular expression: %s" % find)
        r = regex.compile(find, flags=regex.V1)

        entry = {
            'description': word,
            'find': find,
            'replace': replace,
            'regex': r
        }

        listing.append(entry)

    logger.debug("compiled %d regular expression" % len(listing))

    return listing

def load_text_from_file(src):
    logger = logging.getLogger('os_topy')
    logger.debug("loading text from file %s" % src)
    with open(src, 'rb') as f:
        text = f.read()

    return text

def write_text_to_file(dest, text):
    logger = logging.getLogger('os_topy')
    logger.debug("writing text to file %s" % dest)
    with open(dest, 'wb') as f:
        f.write(text)

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="print debugging messages",
                    action="store_true", default=False)
parser.add_argument("--verbose", help="be verbose",
                    action="store_true", default=False)
parser.add_argument("--no-backup", help="don't backup files",
                    action="store_true", default=False)
parser.add_argument("--not-in-place", help="don't change files in place",
                    action="store_true", default=False)
parser.add_argument("--only-check", help="only check for errors",
                    action="store_true", default=False)
parser.add_argument("--cache", help="location of the pickle cache file",
                    type=str, default="/tmp/retf.p")
parser.add_argument("--listing", help="location of the RETF listing file",
                    type=str, default="/tmp/retf.lst")
parser.add_argument("file", nargs='+', type=str,
                    help="file to check for typographical errors")
args = parser.parse_args()

logger = logging.getLogger(name='os_topy')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

if args.verbose:
    logger.setLevel(logging.INFO)

if args.debug:
    logger.setLevel(logging.DEBUG)

if not os.path.isfile(args.listing):
    download_listing(args.listing)

if os.path.isfile(args.cache):
    listing = load_listing_from_cache(args.cache)
else:
    listing = generate_listing(args.listing)
    write_listing_to_cache(listing, args.cache)

# some rules are not working with regex or are not useful
disabled = [
    'of xxx of xxx',
    'Apache',
    'Arabic',
    'Etc.',
    'Currency symbol before number'
]

for x in disabled:
    logger.debug("rule '%s' is disabled" % x)

for src in args.file:
    logger.info("checking file %s for typographical errors" % src)
    text = load_text_from_file(src)
    findings = 0

    for entry in listing:
        if entry.get('description') in disabled:
            continue
        logger.debug("%s: checking rule '%s'" % (src, entry.get('description')))
        r = entry.get('regex')
        logger.debug(entry.get('find'))
        newtext, count = r.subn(entry.get('replace'), text)
        if count > 0:
            logger.warning("%d match(s) in file %s : %s" % (count, src, entry.get('description')))
            findings += count
        text = newtext

    logger.info("%s findings in file %s" % (findings, src))

    if findings > 0 and not args.only_check:
        if args.not_in_place:
            write_text_to_file("%s.topy" % src, text)
        else:
            if not args.no_backup:
                logger.debug("copying %s to backup file %s.orig" % (src, src))
                shutil.copy2(src, "%s.orig" % src)

            write_text_to_file(src, text)
