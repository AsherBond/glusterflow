#!/usr/bin/env python

import sys
import SocketServer
import json
import psycopg2
"""GlusterFlow JSON Server

Very simple JSON server, catching GlusterFlow JSON data
then sticking it in a database.

Very proof-of-concept / experimental :)
"""

#  Set various constants
gf_json_server_ver = '0.0.1'
db_host = 'localhost'
db_name = 'glusterflow'
debug = 0


class MyUDPServer(SocketServer.ThreadingUDPServer):
    allow_reuse_address = True


class MyUDPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            # Receive JSON message
            gl_data = json.loads(self.request[0].strip())

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
server = MyUDPServer(('0.0.0.0', 13373), MyUDPServerHandler)

try:
    if debug == 1:
        print "DEBUG: Starting JSON listener"
    server.serve_forever()

except KeyboardInterrupt, e:

    # Close database connection
    if conn:
        conn.close()
        if debug == 1:
            print "\nDEBUG: Database connection closed"
