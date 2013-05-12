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
db_host = '/tmp'  # '/tmp' instead of a hostname means "connect to localhost using unix domain sockets"
                  # Feel free to change this to a hostname if you need :)
db_port = 5432
db_name = 'glusterflow'
db_user = ''
db_passwd = ''
debug = 0


class MyUDPServerHandler(DatagramProtocol):
    def datagramReceived(self, data, (host, port)):

        # Receive JSON message
        gl_data = json.loads(data.strip())

        # Display the JSON message (for now only)
        if debug == 1:
            if gl_data:
                print 'DEBUG: ' + repr(gl_data)

        try:

            # Insert the JSON message contents into the database
            cur = conn.cursor()
            insert_string = 'INSERT into ui_flowdata(server, protocol, operation, filename, start_time) VALUES (%s, %s, %s, %s, %s)'
            cur.execute(insert_string, (gl_data['server'], gl_data['gf_protocol'], gl_data['operation'], gl_data['file'], gl_data['start']))
            conn.commit()

        except psycopg2.DatabaseError, e:

            # Something went wrong with the insert
            if conn:
                conn.rollback()

            # Display the error
            print 'DEBUG: Error %s' % e

# Display startup banner
print "GlusterFlow JSON Server " + gf_json_server_ver

# Enable debug mode if it was requested on the command line
for param in sys.argv[1:]:
    if param == '--debug':
        debug = 1

# Construct the database connection string
# (seems like an ugly approach, but it works)
connection_string = ''
if db_host:
    connection_string = '{0} host={1}'.format(connection_string, db_host)
if db_port:
    connection_string = '{0} port={1}'.format(connection_string, db_port)
if db_name:
    connection_string = '{0} dbname={1}'.format(connection_string, db_name)
if db_user:
    connection_string = '{0} user={1}'.format(connection_string, db_user)
if db_passwd:
    connection_string = '{0} password={1}'.format(connection_string, db_passwd)
connection_string = connection_string.strip()
if debug == 1:
    print 'DEBUG: Database connection string: ', connection_string

# Connect to the database
try:
    conn = psycopg2.connect(connection_string)

except psycopg2.OperationalError, e:
    # Database connection error.  Display the error and exit
    print 'ERROR: Unable to connect to database -', e
    sys.exit(1)

else:
    if debug == 1:
        print 'DEBUG: Connected to database'

# Start JSON server listening
if debug == 1:
    print 'DEBUG: Starting JSON listener'
reactor.listenUDP(13373, MyUDPServerHandler())
reactor.run()
if debug == 1:
    print 'DEBUG: Exiting GlusterFlow JSON Server'
