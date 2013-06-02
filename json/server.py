#!/usr/bin/env python

import sys
import json
from datetime import datetime
import psycopg2
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet import error
"""GlusterFlow JSON Server

Very simple JSON server, catching GlusterFlow JSON data
then sticking it in a database.

Very proof-of-concept / experimental :)
"""

#  Set various constants
gf_json_server_ver = '0.0.3'
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

            # Insert the raw JSON message contents into the database
            cur = conn.cursor()
            json_msg = 'INSERT into ui_flowdata_new(' \
                       'server, protocol, operation, filename, start_time)' \
                       ' VALUES (%s, %s, %s, %s, %s)'

            if debug == 1:
                print 'DEBUG: ' + repr(json_msg)

            cur.execute(json_msg, (gl_data['server'], gl_data['gf_protocol'],
                                   gl_data['operation'], gl_data['file'],
                                   gl_data['start']))

            # Create a timestamp with minute level accuracy
            summary_time = datetime.now().replace(second=0, microsecond=0)

            # Find out if a summary row with the "# of operations this
            # minute" already exists for the current time period
            sel_sum = 'SELECT count FROM ui_fop_summaries WHERE ' \
                      'server = %s AND operation = %s AND summary_time = %s'
            cur.execute(sel_sum, (gl_data['server'], gl_data['operation'],
                                  summary_time))

            # Create one if it doesn't exist, or update one if it does
            if cur.rowcount == 0:
                # It doesn't so create a new operation summary for the current
                # time period
                ins_sum = 'INSERT into ui_fop_summaries(' \
                          'server, operation, summary_time, count)' \
                          ' VALUES (%s, %s, %s, 1)'
                cur.execute(ins_sum, (gl_data['server'], gl_data['operation'],
                                      summary_time))
            else:
                # An operation summary already exists, so update it
                upd_sum = 'UPDATE ui_fop_summaries SET count = count + 1 ' \
                          'WHERE server = %s AND operation = %s ' \
                          'AND summary_time = %s'
                cur.execute(upd_sum, (gl_data['server'], gl_data['operation'],
                                      summary_time))

            # Find out if a summary row with the "# of operations on this file
            # this minute" already exists for the current time period
            sel_sum = 'SELECT count FROM ui_filename_summaries WHERE ' \
                      'server = %s AND filename = %s AND summary_time = %s'
            cur.execute(sel_sum, (gl_data['server'], gl_data['file'],
                                  summary_time))

            if cur.rowcount == 0:
                # It doesn't so create a new operation summary for the current
                # time period
                ins_sum = 'INSERT into ui_filename_summaries(' \
                          'server, filename, summary_time, count)' \
                          ' VALUES (%s, %s, %s, 1)'
                cur.execute(ins_sum, (gl_data['server'], gl_data['file'],
                                      summary_time))
            else:
                # An operation summary already exists, so update it
                upd_sum = 'UPDATE ui_filename_summaries SET count = count + 1 ' \
                          'WHERE server = %s AND filename = %s ' \
                          'AND summary_time = %s'
                cur.execute(upd_sum, (gl_data['server'], gl_data['file'],
                                      summary_time))

            # If everything worked, commit the transaction
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
conn_str = ''
if db_host:
    conn_st = '{0} host={1}'.format(conn_str, db_host)
if db_port:
    conn_str = '{0} port={1}'.format(conn_str, db_port)
if db_name:
    conn_str = '{0} dbname={1}'.format(conn_str, db_name)
if db_user:
    conn_str = '{0} user={1}'.format(conn_str, db_user)
if db_passwd:
    conn_str = '{0} password={1}'.format(conn_str, db_passwd)
conn_str = conn_str.strip()
if debug == 1:
    print 'DEBUG: Database connection string:', conn_str

# Connect to the database
try:
    conn = psycopg2.connect(conn_str)

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
