#!/usr/bin/env python

import sys
import json
import psycopg2
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
"""GlusterFlow JSON Server

Very simple JSON server, catching GlusterFlow JSON data
then sticking it in a database.

Very proof-of-concept / experimental :)
"""

#  Set various constants
gf_json_server_ver = '0.0.2'
db_host = 'localhost'
db_name = 'glusterflow'
debug = 0


class MyUDPServerHandler(DatagramProtocol):
    def datagramReceived(self, data, (host, port)):
        try:
            # Receive JSON message
            gl_data = json.loads(data.strip())

            # Display the JSON message (for now only)
            if debug == 1:
                if gl_data:
                    print 'DEBUG: ' + repr(gl_data)

            try:

                # Insert the JSON message contents into database
                cur = conn.cursor()
                insert_string = 'INSERT into ui_flowdata(server, protocol, operation, filename, start_time) VALUES (%s, %s, %s, %s, %s)'
                cur.execute(insert_string, (gl_data['server'], gl_data['protocol'], gl_data['operation'], gl_data['file'], gl_data['start']))
                conn.commit()

            except psycopg2.DatabaseError, e:

                # Something went wrong with the insert
                if conn:
                    conn.rollback()

                # Display the error
                print 'DEBUG: Error %s' % e

        except Exception, e:
            print 'ERROR: Exception encountered when receiving JSON message: ', e


# Display startup banner
print "GlusterFlow JSON Server " + gf_json_server_ver

# Enable debug mode, if it was requested on the command line
for param in sys.argv[1:]:
    if param == '--debug':
        debug = 1

# Create database connection
try:
    conn = psycopg2.connect("dbname='" + db_name + "' host='" + db_host + "'")
    if debug == 1:
        print 'DEBUG: Connected to database'

except:
    if debug == 1:
        print 'DEBUG: Unable to connect to database'

# Start JSON server listening
if debug == 1:
    print 'DEBUG: Starting JSON listener'
reactor.listenUDP(13373, MyUDPServerHandler())
reactor.run()
if debug == 1:
    print 'DEBUG: Exiting GlusterFlow JSON Server'
