#!/bin/sh

sudo stop ceph-all
ssh ceph002 'sudo stop ceph-all'
ssh ceph003 'sudo stop ceph-all'
ceph-deploy purge ceph001 ceph002 ceph003
sudo rm -rf /var/lib/ceph
sudo rm -rf /etc/ceph
sudo rm -rf /var/log/ceph
ssh ceph002 'sudo rm -rf /var/lib/ceph'
ssh ceph002 'sudo rm -rf /etc/ceph'
ssh ceph002 'sudo rm -rf /var/log/ceph'
ssh ceph003 'sudo rm -rf /var/lib/ceph'
ssh ceph003 'sudo rm -rf /etc/ceph'
ssh ceph003 'sudo rm -rf /var/log/ceph'
ssh ceph002 'sudo reboot'
ssh ceph003 'sudo reboot'
sudo reboot
