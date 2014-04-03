#!/bin/sh

# author: Christian Berendt <berendt@b1-systems.de>

ip netns exec $1 ping -c 3 $2
