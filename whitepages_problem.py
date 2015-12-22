#! /usr/bin/env python3
#
#
import socket
import os

TYPE="TYPE"
ENABLE="ENABLE"
VOLUME="VOLUME"
OPTIONS="OPTIONS"


# Return the table as a dictionary key'd by host name.  The values of the
# dictionary are a dictionary with keys for enable, link, volume, and options
table = get_table("file_mounts.tsv")
my_hostname = socket.gethostname()

for node in table.keys():
# Volumes should only be mounted on a node if there is an entry in the input
# file for that node
    if my_hostname == node :
# mountpoint is the form /mnt/[TYPE]/[FILERNAME]/[VOLUME]
# Note there is a point of confusion between VOLUME which is what the
# requirements document says and what the key name is in table, and volume.
        filername, volume = table[VOLUME].split(":") 
        mountpoint = "/mnt/%s/%s/%s" % ( table[TYPE], filername, volume )        

# if the ENABLE field is marked N, then the volume should be unmounted and
# commented out in in fstab.  This should be completed in 1 hour
        if table[node][ENABLE] == "N" :
            umount( table[node][volume] )
        elif table[node][ENABLE] == "Y" :
# do not assume that the mountpoint exists
            if not os.path.isfile(mountpoint) :
                create_mountpoint(mountpoint)
# Check to see if the volume is already mounted and linked, and change the state
# if not (I assume this means mount it and link it if it is not mounted or if
# the symlink is wrong)
                if not mounted(mountpoint) :
                    mount( table[VOLUME] 
        
        
