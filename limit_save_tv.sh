#!/bin/sh

interface=wlp3s0
range=78.152.40.0-78.152.40.254
limit=5Mbit

sudo iptables -t mangle -L POSTROUTING | grep --quiet $range
if [[ $? -ne 0 ]]; then
    sudo iptables -t mangle -A POSTROUTING -o $interface -p tcp -m iprange --dst-range $range -j CLASSIFY --set-class 2:11
fi

sudo tc qdisc delete dev $interface root handle 2:0
sudo tc qdisc add dev $interface root handle 2:0 htb default 99
sudo tc class add dev $interface parent 2:0 classid 2:1 htb rate 100Mbit ceil 100Mbit
sudo tc class add dev $interface parent 2:1 classid 2:11 htb rate $limit ceil $limit prio 2
sudo tc qdisc add dev $interface parent 2:11 handle 20: sfq perturb 10
