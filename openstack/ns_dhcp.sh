#!/bin/sh

# author: Christian Berendt <berendt@b1-systems.de>

for ns in $(ip netns show | grep qdhcp); do
  echo -n "$ns : "
  ip netns exec $ns ip a s | grep ns- | grep inet | grep -v 169 | awk '{ print $2 }'
done
