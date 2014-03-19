#!/usr/bin/python

## copyright: B1 Systems GmbH   <info@b1-systems.de>,    2013.
##    author: Christian Berendt <berendt@b1-systems.de>, 2013.
##   license: Apache License, Version 2.0

from gerritlib.gerrit import *
import pyratemp

ACCOUNT = 'YOUR_GERRIT_ACCOUNT'
KEY = '/path/to/your/ssh.key'

accounts = [
    'LIST',
    'OF',
    'WATCHED',
    'ACCOUNTS'
]

gerrit = Gerrit('review.openstack.org', ACCOUNT, 29418, KEY)

reviews = []

for account in accounts:
    for review in gerrit.bulk_query("owner:%s status:open limit:50" % account):
        if 'open' in review:
            reviews = reviews + [review]

t = pyratemp.Template(filename='open_reviews.tmpl')
result = t(reviews=reviews)
print result
