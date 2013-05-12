import sys
import socket
import json
import time
from datetime import datetime
from gluster import *
"""Send metrics of every request to a central collector server

This is to enable intelligent diagnostics and reporting cluster wide.
"""

# GlusterFlow Server
# This needs to be changed into a .vol file option
glusterflow_json_server = ('192.168.1.68', 13373)

# Protocol string to send
# This also needs to be changed into a .vol file option
protocol = 'nfs'

# Debug on or off
debug = 0

# Work out the hostname
this_host = str(socket.getfqdn())


def send_message(operation, file_name):

    # Get timestamp
    start_time = datetime.now()

    # Create connection to GlusterFlow server
    global msg
    try:
        msg = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg.connect(glusterflow_json_server)

    except socket.error, e:
        # Something went wrong when creating the connection
        print 'ERROR: socket error occurred: ', e

    else:
        # Create GlusterFlow message to send
        # It would be good to also include the hostname of the client too later on (if possible)
        gf_message = {'server': this_host, 'protocol': protocol, 'operation': operation, 'file': file_name, 'start':str(start_time)}

        # Send message to GlusterFlow server
        json_message = json.dumps(gf_message)
        try:
            msg.sendall(json_message)
        except socket.error, e:
            print 'ERROR: Error received at msg.sendall() time: ', e
        else:
            msg.close()


class xlator (Translator):

    def __init__ (self, c_this):
        self.hostname = socket.getfqdn()

        # Run normal translator init
        Translator.__init__(self,c_this)


    def lookup_fop (self, frame, this, loc, xdata):
#        print "loc->path : ", repr(loc.contents.path)
#        print "loc->name : ", repr(loc.contents.name)
#        print "loc->inode : ", repr(loc.contents.inode)
#        print "loc->parent : ", repr(loc.contents.parent)
#        print "loc->gfid : ", repr(loc.contents.gfid)
#        print "loc->pargfid : ", repr(loc.contents.pargfid)

        # Send GlusterFlow JSON message to collector
        send_message('lookup', loc.contents.path)

        # Continue on to the next translator
        dl.wind_lookup(frame,POINTER(xlator_t)(), loc, xdata)
        return 0


    def create_fop (self, frame, this, loc, flags, mode, umask, fd, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('create', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, flags, mode, umask, fd,
                       xdata)
        return 0


    def open_fop (self, frame, this, loc, flags, fd, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('open', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, flags, fd, xdata)
        return 0


    def readv_fop (self, frame, this, fd, size, offset, flags, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('readv', 'fd')

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), fd, size, offset, flags,
                       xdata)
        return 0


    def writev_fop (self, frame, this, fd, vector, count, offset, flags,
                    iobref, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('writev', 'fd')

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), frame, this, fd, vector,
                       count, offset, flags, iobref, xdata)
        return 0


    def opendir_fop (self, frame, this, loc, fd, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('opendir', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, fd, xdata)
        return 0


    def readdir_fop (self, frame, this, fd, size, offset, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('readdir', 'fd')

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), fd, size, offset, xdata)
        return 0


    def readdirp_fop (self, frame, this, fd, size, offset, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('readdirp', 'fd')

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), fd, size, offset, xdata)
        return 0


# Something wrong here.  Getting errors about "TypeError: this function takes at least 8 arguments (4 given)"
#    def stat_fop (self, frame, this, loc, xdata):

#        # Send GlusterFlow JSON message to collector
#        send_message('stat', loc.contents.path)

#        # Continue on to the next translator
#        dl.wind_create(frame, POINTER(xlator_t)(), loc, xdata)
#        return 0


    def fstat_fop (self, frame, this, fd, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('fstat', 'fd')

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), fd, xdata)
        return 0


    def statfs_fop (self, frame, this, loc, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('statfs', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, xdata)
        return 0


    def setxattr_fop (self, frame, this, loc, dictionary, flags, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('setxattr', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, dictionary, flags,
                       xdata)
        return 0


    def getxattr_fop (self, frame, this, loc, name, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('getxattr', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, name, xdata)
        return 0


    def fsetxattr_fop (self, frame, this, fd, dictionary, flags, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('fsetxattr', 'fd')

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), fd, dictionary, flags,
                       xdata)
        return 0


    def fgetxattr_fop (self, frame, this, fd, name, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('fgetxattr', 'fd')

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), fd, name, xdata)
        return 0


    def removexattr_fop (self, frame, this, loc, name, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('removexattr', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, name, xdata)
        return 0


    def fremovexattr_fop (self, frame, this, fd, name, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('fremovexattr', 'fd')

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), fd, name, xdata)
        return 0


    def link_fop (self, frame, this, oldloc, newloc, xdata):
# Probably need new fields in the database for this function

        # Send GlusterFlow JSON message to collector
        send_message('link', oldloc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), oldloc, newloc, xdata)
        return 0


    def symlink_fop (self, frame, this, linkname, loc, umask, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('symlink', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), linkname, loc, umask,
                       xdata)
        return 0


    def unlink_fop (self, frame, this, loc, xflags, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('unlink', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, xflags, xdata)
        return 0


    def readlink_fop (self, frame, this, loc, size, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('readlink', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, size, xdata)
        return 0


    def mkdir_fop (self, frame, this, loc, mode, umask, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('mkdir', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, mode, umask, xdata)
        return 0


    def rmdir_fop (self, frame, this, loc, xflags, xdata):

        # Send GlusterFlow JSON message to collector
        send_message('rmdir', loc.contents.path)

        # Continue on to the next translator
        dl.wind_create(frame, POINTER(xlator_t)(), loc, xflags, xdata)
        return 0
