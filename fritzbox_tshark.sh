#!/bin/sh

# http://www.wehavemorefun.de/fritzbox/IP-Pakete_mitschneiden
# http://kvz.io/blog/2010/05/15/analyze-http-requests-with-tshark/

fritzbox="192.168.178.1"
password="password"
interface="3-0"
length=1600

challenge=$(curl -s http://$fritzbox/login_sid.lua | sed 's/.*<Challenge>\(.*\)<\/Challenge>.*/\1/')
CPSTR=$challenge-$password
MD5=$(echo -n $CPSTR | iconv -f ISO8859-1 -t UTF-16LE | md5sum -b | awk '{print substr($0,1,32)}')
RESPONSE="$challenge-$MD5"
POSTDATA="?username=&response=$RESPONSE"
SID=$(wget -O - --post-data="$POSTDATA" "http://$fritzbox/login_sid.lua" 2>/dev/null | sed 's/.*<SID>\(.*\)<\/SID>.*/\1/')

wget --quiet -O - "http://$fritzbox/cgi-bin/capture_notimeout?ifaceorminor=$interface&snaplen=$length&capture=Start&sid=$SID" | tshark -i - -S -l -N NnmtC '(tcp port 80 or tcp port 443) and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)' -R 'http.request.method == "GET" || http.request.method == "HEAD" || http.request.method == "POST"' -2
