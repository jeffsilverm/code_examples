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

LOGFILE="/tmp/`date +%Y-%m-%d_%H-%M`_diagnose_net.log"


if [ "x$1" == "x" ] ; then
  REMOTE_HOST="www.google.com"
else
  REMOTE_HOST=$1
fi

if nc $REMOTE_HOST 80 < /dev/null >>$LOGFILE ; then
  echo "Network appears to be working to the extent this script can test it to $REMOTE_HOST 80"
fi


default_gateway=`ip route list | fgrep default | cut -d " " -f 3`
if [ ${#default_gateway} -eq 0 ]; then
  echo "Problem: the default gateway is not known.  Probably nothing else on the network is going to work either"
# The default gateway might not be known because the network was configured manually and incorrectly, or because
# DHCP isn't working, or perhaps there is a hardware problem that's keeping DHCP from working properly.
else
  echo -n "The default gateway $default_gateway is "
  ping -c 4 $default_gateway  >>$LOGFILE
  status=$?
  if [ $status -eq 0 ]; then
    echo "pingable: your local area network is at least partly working"
  elif [ $status -eq 2 ]; then
    echo "NOT pingable due to a problem resolving the gateway name to an IP address, which is odd.  Look at the output of the 'ip route list' command"
  else
    echo "NOT pingable: your local area network is broken.  Perhaps the default router is not working or perhaps there is a DHCP error"
  fi


  for NAME_SERVER in `fgrep nameserver /etc/resolv.conf | cut -d " " -f 2`; do
    dig @${NAME_SERVER} $REMOTE_HOST  >>$LOGFILE
    status=$?
# See http://linux.die.net/man/1/dig for the closest thing I can find to a description of what the return codes mean
# 0: Everything went well, including things like NXDOMAIN
# 1: Usage error
# 8: Couldn't open batch file
# 9: No reply from server
#10: Internal error
    if [ $status -eq 9 ]; then
      echo "Problem: name server $NAME_SERVER could not be reached - look in /etc/resolv.conf"
    elif [ $status -ne 0 ]; then
      echo "Problem with the dig command, probably a software error and not your fault.  Please report this problem to jeffsilverm@gmail.com"
    else
      echo "name server $NAME_SERVER is working"
# The advantage of the host command over dig is that dig will return 0 on an NXDOMAIN error, host won't.
      if host $REMOTE_HOST $NAME_SERVER  >>$LOGFILE; then
        echo "Resolution of remote host $REMOTE_HOST by name server $NAME_SERVER is working"
      else
        echo "Name server $NAME_SERVER cannot resolve $REMOTE_HOST, perhaps try picking a different remote host name?"
      fi
    fi
  done
fi

