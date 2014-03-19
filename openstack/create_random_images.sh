#!/bin/sh

## copyright: B1 Systems GmbH   <info@b1-systems.de>,    2013.
##    author: Christian Berendt <berendt@b1-systems.de>, 2013.
##   license: Apache License, Version 2.0

for i in $(seq -w 1 $1); do
        dd if=/dev/urandom of=/tmp/testing.img bs=1k count=1024
        glance image-create --name random_image_$i --disk-format raw --container-format bare --file /tmp/testing.img
done

rm -f /tmp/testing.img
