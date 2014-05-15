#!/bin/sh

for x in $(cat listing); do
    echo $x
    for result in $(pep8 --select E127 $x | awk -F: '{ print $1 ":" $2 }'); do
        FILE=$(echo $result | awk -F: '{ print $1 }')
        LINE=$(echo $result | awk -F: '{ print $2 }')
        sed -i "${LINE}s/^.//" $FILE
    done
    pep8 --select E127 $x
done
