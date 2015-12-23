#! /usr/bin/env python3
#
#
import socket
import os


TYPE="TYPE"
ENABLE="ENABLE"
VOLUME="VOLUME"
OPTIONS="OPTIONS"


def get_table(filename):
    """This function opens file filename and reads it.  The first line is a
header and may be ignored.  The remaining lines are tab separated variables
NODE, ENABLE, TYPE, VOLUME, OPTIONS
    """
    raise NotImplemented

def string_in_file ( string, filename ):
    """This function opens file filename and reads until it comes to a line
that contains string string.  Then it returns the line that contains the
string.  If the string does not occur in the file, then it returns an empty
string.  The function returns only the first occurance of the string.  This is
basically fgrep in python"""
    f = open(filename, "r")
    contents = f.open()
    f.close()
    lines = contents.split("\n")
    for l in lines :
        if string in l:
            return l
    return ""


def create_mountpoint( mountpoint ) :
    """Checks to see if the mountpoint exists.  If not, then it creates the
mountpoint."""  
    """Reads /proc/mounts (the requirements don't say anything about which
operating system this software has to run on.  If running on something other
than linux, this subroutine will throw a FileNotFoundError) to see if the
file system is mounted.  If not, then it checks to see if the mountpoint
exists."""
    raise NotImplemented

def mount ( device, fs_type, mountpoint, options ):
    """Mounts device of file system type fs_type at mountpoint mountpoint,
with options."""
    raise NotImplemented

def handle_symlink ( mountpoint, symlink ):
    """Detects if the symlink points to the mountpoint.  If so, then no
action is taken.  Otherwise, it creates the symlink"""
    


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
                create_mountpoint( mountpoint)
# Check to see if the volume is already mounted and linked, and change the state
# if not (I assume this means mount it and link it if it is not mounted or if
# the symlink is wrong)
            if not mounted(mountpoint) :
                mount( table[VOLUME], table[TYPE], mountpoint, table[OPTIONS] )
# The entry in the LINK column should be symlinked to the mount point.
            handle_symlink ( mountpoint, table[LINK] )
        
        
