#! /bin/bash
#
# This script diagnosis a problem with a network.  You might run it after system startup
# to verify that the network started properly.


if [ "x$1" == "x" ]; then
  REMOTE_HOST="www.google.com"
else
  REMOTE_HOST=$1
fi

if nc $REMOTE_HOST 80; then
  echo "Network appears to be working to the extent this script can test it to $REMOTE_HOST 80"
fi


dig @${NAME_SERVER} $REMOTE_HOST
status=$?
if [ $status -eq 9 ]; then
  echo "Problem: name server $NAME_SERVER could not be reached"
fi


