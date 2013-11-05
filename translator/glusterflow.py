import sys
import socket
import time
from datetime import datetime

# For LogStash
import logging
import logstash_formatter

# Import Glupy
from gluster_glupy import *

'''Send metrics of every request to a central analytics server

This is to enable intelligent diagnostics and reporting cluster wide.
'''

# TODO: This should be changed into a .vol file option, or autoconfigure
# native_server = Gluster native server
# fuse_client = Gluster native client
# nfs_server = Gluster NFS server
# libgfapi = Libgfapi client
event_source = 'nfs_server'

# Debug on or off
debug = 1

# Determine the local hostname
this_host = str(socket.gethostname())

# Set up logging to go via LogStash
logger = logging.getLogger()
handler = logging.FileHandler('/var/log/glusterflow.log')
formatter = logstash_formatter.LogstashFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_message(operation, file_name):

    # Get timestamp
    start_time = datetime.now()

    # Create GlusterFlow event message
    # TODO: It would be good to also include the hostname of the client
    gf_message = {'server': this_host, 'source': event_source,
                  'operation': operation, 'file': file_name,
                  'start': str(start_time)}

    # If debugging, throw the message to the console
    if debug:
        print(gf_message)

    # Send message to ElasticSearch via LogStash
    logging.warning(gf_message)


class xlator (Translator):

    def __init__ (self, c_this):

        # Run normal translator init
        Translator.__init__(self, c_this)


    def lookup_fop (self, frame, this, loc, xdata):

        # Send GlusterFlow message
        send_message('lookup', loc.contents.path)

        # Continue on to the next translator
        dl.wind_lookup(frame, POINTER(xlator_t)(), loc, xdata)
        return 0


    def create_fop (self, frame, this, loc, flags, mode, umask, fd, xdata):

        # Send GlusterFlow message
        send_message('create', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, flags, mode, umask, fd,
                       xdata)
        return 0


    def open_fop (self, frame, this, loc, flags, fd, xdata):

        # Send GlusterFlow message
        send_message('open', loc.contents.path)

        # Continue on to the next translator
        dl.wind_open(frame, POINTER(xlator_t)(), loc, flags, fd, xdata)
        return 0


    def opendir_fop (self, frame, this, loc, fd, xdata):

        # Send GlusterFlow message
        send_message('opendir', loc.contents.path)

        # Continue on to the next translator
        dl.wind_opendir(frame, POINTER(xlator_t)(), loc, fd, xdata)
        return 0


    def stat_fop (self, frame, this, loc, xdata):

        # Send GlusterFlow message
        send_message('stat', loc.contents.path)

        # Continue on to the next translator
        dl.wind_stat(frame, POINTER(xlator_t)(), loc, xdata)
        return 0


    def statfs_fop (self, frame, this, loc, xdata):

        # Send GlusterFlow message
        send_message('statfs', loc.contents.path)

        # Continue on to the next translator
        dl.wind_statfs(frame, POINTER(xlator_t)(), loc, xdata)
        return 0


    def setxattr_fop (self, frame, this, loc, dictionary, flags, xdata):

        # Send GlusterFlow message
        send_message('setxattr', loc.contents.path)

        # Continue on to the next translator
        dl.wind_setxattr(frame, POINTER(xlator_t)(), loc, dictionary, flags,
                         xdata)
        return 0


    def getxattr_fop (self, frame, this, loc, name, xdata):

        # Send GlusterFlow message
        send_message('getxattr', loc.contents.path)

        # Continue on to the next translator
        dl.wind_getxattr(frame, POINTER(xlator_t)(), loc, name, xdata)
        return 0


    def removexattr_fop (self, frame, this, loc, name, xdata):

        # Send GlusterFlow message
        send_message('removexattr', loc.contents.path)

        # Continue on to the next translator
        dl.wind_removexattr(frame, POINTER(xlator_t)(), loc, name, xdata)
        return 0


    def link_fop (self, frame, this, oldloc, newloc, xdata):
        # TODO: Probably need new fields in the database for this function

        # Send GlusterFlow message
        send_message('link', oldloc.contents.path)

        # Continue on to the next translator
        dl.wind_link(frame, POINTER(xlator_t)(), oldloc, newloc, xdata)
        return 0


    def symlink_fop (self, frame, this, linkname, loc, umask, xdata):

        # Send GlusterFlow message
        send_message('symlink', loc.contents.path)

        # Continue on to the next translator
        dl.wind_symlink(frame, POINTER(xlator_t)(), linkname, loc, umask,
                        xdata)
        return 0


    def unlink_fop (self, frame, this, loc, xflags, xdata):

        # Send GlusterFlow message
        send_message('unlink', loc.contents.path)

        # Continue on to the next translator
        dl.wind_unlink(frame, POINTER(xlator_t)(), loc, xflags, xdata)
        return 0


    def readlink_fop (self, frame, this, loc, size, xdata):

        # Send GlusterFlow message
        send_message('readlink', loc.contents.path)

        # Continue on to the next translator
        dl.wind_readlink(frame, POINTER(xlator_t)(), loc, size, xdata)
        return 0


    def mkdir_fop (self, frame, this, loc, mode, umask, xdata):

        # Send GlusterFlow message
        send_message('mkdir', loc.contents.path)

        # Continue on to the next translator
        dl.wind_mkdir(frame, POINTER(xlator_t)(), loc, mode, umask, xdata)
        return 0


    def rmdir_fop (self, frame, this, loc, xflags, xdata):

        # Send GlusterFlow message
        send_message('rmdir', loc.contents.path)

        # Continue on to the next translator
        dl.wind_rmdir(frame, POINTER(xlator_t)(), loc, xflags, xdata)
        return 0
