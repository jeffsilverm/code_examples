#! /bin/bash
#
# This script diagnosis a problem with a network.  You might run it after system startup
# to verify that the network started properly.
#
# The tests, in order:
# 
# Can I ping myself using localhost?
# Can I get a list of IP addresses that I have, using the ifconfig or ip commands?
# Can I ping all of the IP address that I know about?
# Do I know what my default gateway is?
# Can I ping my default gateway?
# If not, do I know what my default gateway's MAC address is?
# If not, do I know what 


if [ "x$1" == "x" ]; then
  REMOTE_HOST="www.google.com"
else
  REMOTE_HOST=$1
fi

if nc $REMOTE_HOST 80; then
  echo "Network appears to be working to the extent this script can test it to $REMOTE_HOST 80"
fi


default_gateway=`ip route list | fgrep default | cut -d " " -f 3`
echo -n "The default gateway $default_gateway is "
ping -c 4 $default_gateway
status=$?
if [status == 0 ]; then
  echo "pingable: your local area network is at least partly working"
elif [status == 2]; then
  echo "NOT pingable due to a problem resolving the gateway name to an IP address, which is odd.  Look at the output of the 'ip route list' command"
else
  echo "NOT pingable: your local area network is broken.  Perhaps the default router is not working or perhaps there is a DHCP error"
fi


dig @${NAME_SERVER} $REMOTE_HOST
status=$?
if [ $status -eq 9 ]; then
  echo "Problem: name server $NAME_SERVER could not be reached"
fi


