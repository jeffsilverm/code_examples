#! /usr/bin/env python3
#
#
import socket
import os
# sh is a relative new module
from sh import mount, umount



TYPE="TYPE"
ENABLE="ENABLE"
VOLUME="VOLUME"
OPTIONS="OPTIONS"
MOUNTPOINT="MOUNTPOINT"
LINK="LINK"


def get_table(filename):
    """This function opens file filename and reads it.  The first line is a
header and may be ignored.  The remaining lines are tab separated variables
NODE, ENABLE, TYPE, VOLUME, OPTIONS
    """
    d = {}
    f = open(filename, "r")
    contents = f.read()
    f.close()
    lines = contents.split("\n")
# skip the line, which is a header
    for l in lines[1:] :
# for some reason, the file is picking up the last line as a null string, which
# causes an exception.  This fix is a little more general.
        if len(l) == 0 :
            continue
        ( node, enable, link, fs_type, volume, options ) = l.split("\t")
# Return the table as a dictionary key'd by host name (NODE).  The values of the
# dictionary are a dictionary with keys for enable, link, volume, and options        
        d[node] = { ENABLE: enable, LINK:link, TYPE: fs_type, VOLUME:volume, OPTIONS:options }
    return d

    
 
def string_in_file ( string, filename ):
    """This function opens file filename and reads until it comes to a line
that contains string string.  Then it returns the line that contains the
string.  If the string does not occur in the file, then it returns an empty
string.  The function returns only the first occurance of the string.  This is
basically fgrep in python"""
    f = open(filename, "r")
    contents = f.read()
    f.close()
    lines = contents.split("\n")
    for l in lines :
        if string in l:
            return l
    return ""


def create_mountpoint( mountpoint ) :
    """Checks to see if the mountpoint exists.  If not, then it creates the
mountpoint."""  
    
    if os.path.isfile(mountpoint) :
        if os.path.isdir(point) :
            return  # Mount point exists and it is a directory.
        else :
            raise ValueError("mountpoint %s exists and is not a directory") % \
                  mountpoint
    else :
        return  # mount point has been created


 

def handle_symlink ( mountpoint, symlink ):
    """Detects if the symlink points to the mountpoint.  If so, then no
action is taken.  Otherwise, it creates the symlink"""
    try :
        os.symlink( symlink, mountpoint,  )
    except FileExistsError:
        print(("The symlink %s already exists and points to %s") % ( symlink, mountpoint ))
    except FileNotFoundError:
        print(("The mountpoint %s doesn't exist and should be created") % mountpoint )
        raise

# Return the table as a dictionary key'd by host name.  The values of the
# dictionary are a dictionary with keys for enable, link, volume, and options
table = get_table("my_file_mounts.tsv")
my_hostname = socket.gethostname()

for node in table.keys():
# Volumes should only be mounted on a node if there is an entry in the input
# file for that nodetable[node]
    if my_hostname == node :
# mountpoint is the form /mnt/[TYPE]/[FILERNAME]/[VOLUME]
# Note there is a point of confusion between VOLUME which is what the
# requirements document says and what the key name is in table, and volume.
        filername, volume = table[node][VOLUME].split(":") 
        mountpoint = "/mnt/%s/%s%s" % ( table[node][TYPE], filername, volume )
# This is new in Python 3.  I can create the directory without throwing an
# exception if it already exists
        os.makedirs(mountpoint, exist_ok=True)

# if the ENABLE field is marked N, then the volume should be unmounted and
# commented out in in fstab.  This should be completed in 1 hour
        if table[node][ENABLE] == "N" :
# This isn't portable to non-linux systems, but the requirements document
# didn't say anything about portability.  If the volume is mounted, then
# it should appear in /proc/mounts
            if string_in_file (volume, "/proc/mounts") != "" :
                umount( table[node][volume] )
        elif table[node][ENABLE] == "Y" :
# do not assume that the mountpoint exists.  Since exist_ok is true, this call
# will not throw an exception if the 
            os.makedirs(mountpoint,exist_ok=True)
# Check to see if the volume is already mounted and linked, and change the state
# if not (I assume this means mount it and link it if it is not mounted or if
# the symlink is wrong)
            if not mounted(mountpoint) :
#                mount( table[node][VOLUME], table[node][TYPE], mountpoint, table[node][OPTIONS] )
# Mounts device of file system type fs_type at mountpoint mountpoint,
# with options options.  Reads /proc/mounts (the requirements don't say anything about which
# operating system this software has to run on.  If running on something other
# than linux, this subroutine will throw a FileNotFoundError) to see if the
# file system is mounted.  It assumes that the mountpoint exists."""

# mount is from module sh
                mount( table[node][VOLUME], mountpoint, "-t " + fs_type, "-o "+options )
        else :
            raise ValueError(("Invalid value of ENABLE %s") % table[node][ENABLE] )

# The entry in the LINK column should be symlinked to the mount point.
        handle_symlink ( mountpoint, table[node][LINK] )
        
