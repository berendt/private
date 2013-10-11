#!/bin/sh
ceph-deploy install ceph001 ceph002 ceph003
sudo mkdir /etc/ceph
ssh ceph002 'sudo mkdir /etc/ceph'
ssh ceph003 'sudo mkdir /etc/ceph'
sudo chown -R ceph:ceph /etc/ceph
ssh ceph002 'sudo chown -R ceph:ceph /etc/ceph'
ssh ceph003 'sudo chown -R ceph:ceph /etc/ceph'
ceph-deploy new ceph001 ceph002 ceph003
sleep 2
ceph-deploy mon create ceph001 ceph002 ceph003
sleep 2
ceph-deploy gatherkeys ceph001
ceph-deploy disk zap ceph001:vdb
ceph-deploy disk zap ceph001:vdc
ceph-deploy disk zap ceph002:vdb
ceph-deploy disk zap ceph002:vdc
ceph-deploy disk zap ceph003:vdb
ceph-deploy disk zap ceph003:vdc
ceph-deploy osd create ceph001:vdb:/dev/vdb
ceph-deploy osd create ceph002:vdb:/dev/vdb
ceph-deploy osd create ceph003:vdb:/dev/vdb
ceph-deploy osd create ceph001:vdc:/dev/vdc
ceph-deploy osd create ceph002:vdc:/dev/vdc
ceph-deploy osd create ceph003:vdc:/dev/vdc
ceph-deploy mds create ceph001
ceph-deploy admin ceph001
sudo stop ceph-all
ssh ceph002 'sudo stop ceph-all'
ssh ceph003 'sudo stop ceph-all'
sudo start ceph-all
ssh ceph002 'sudo start ceph-all'
ssh ceph003 'sudo start ceph-all'
