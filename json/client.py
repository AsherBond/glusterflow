import sys
import socket
import json
import time
from datetime import datetime
from gluster import *
"""Send metrics of every request to a central collector server

This is to enable intelligent diagnostics and reporting cluster wide.
"""

# GlusterFlow Server - obviously, the hard coding needs to be fixed
glusterflow_json_server = ('192.168.1.68', 13373)

# Debug on or off
debug = 1

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
            gf_message = {'server': str(self.hostname), 'protocol':'nfs', 'operation':'lookup', 'file':loc.contents.path, 'start':str(start_time)}

            # Send message to GlusterFlow server
            json_message = json.dumps(gf_message)
            try:
                msg.sendall(json_message)
            except socket.error, e:
                print 'ERROR: Error received at msg.sendall() time: ', e
            else:
                msg.close()

        # Continue on to the next translator
        dl.wind_lookup(frame,POINTER(xlator_t)(),loc,xdata)
        return 0


    def lookup_cbk (self, frame, cookie, this, op_ret, op_errno, inode, buf, xdata, postparent):

        # Log the operation and full path name
        # Ugh, can't seem to access any useful file info in the callback (so far) :(
        # ...

        # Log request finish time
        # ...

        # Continue on to the next translator
        dl.unwind_lookup(frame,cookie,this,op_ret,op_errno,inode,buf,xdata,postparent)
        return 0


    def create_fop (self, frame, this, loc, flags, mode, umask, fd, xdata):

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
            gf_message = {'server': str(self.hostname), 'protocol':'nfs', 'operation':'create', 'file':loc.contents.path, 'start':str(start_time)}

            # Send message to GlusterFlow server
            json_message = json.dumps(gf_message)
            try:
                msg.sendall(json_message)
            except socket.error, e:
                print 'ERROR: Error received at msg.sendall() time: ', e
            else:
                msg.close()

        # Continue on to the next translator
        dl.wind_create(frame,POINTER(xlator_t)(),loc,flags,mode,umask,fd,xdata)
        return 0


    def create_cbk (self, frame, cookie, this, op_ret, op_errno, fd, inode, buf, preparent, postparent, xdata):

        # Log the operation and full path name
        # Ugh, can't seem to access any useful file info in the callback (so far) :(
        # ...

        # Log request finish time
        # ...

        # Continue on to the next translator
        dl.unwind_create(frame,cookie,this,op_ret,op_errno,fd,inode,buf,preparent,postparent,xdata)
        return 0
