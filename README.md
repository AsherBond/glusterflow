GlusterFlow
===========

A cluster wide profiling and analysis web app for GlusterFS.

Screenshot
----------

![GlusterFlow Screenshot](https://github.com/justinclift/glusterflow/raw/master/ui/static/ui/screenshots/glusterflow_screenshot_0.0.1.png "GlusterFlow Screenshot")

Status
------

This is in very early stages of development, but making good progress already.

Requirements
------------

* Python 2.7.x, Django 1.5.x, and PostgreSQL 8/9+ for the web application front end
* Python 2.7.x and PostgreSQL for the JSON server (receives/collects data in JSON format)
* Python 2.x on the GlusterFS nodes, for the JSON client

Supported Platforms
-------------------

Linux for the Gluster nodes
* RHEL/CentOS 6.x are known to work
* Debian/Ubuntu should work (but untested so far)
* Others should work too.  The JSON client is extremely simple code. :)

Linux and MacOS X for the web app and JSON server
* MacOS X 10.7 (Lion) is known to work (10.8 may work but is untested)
* RHEL/CentOS 6.x should work
* Debian/Ubuntu should work
* Others may work (untested)

Installation
------------

__1. Install Glupy on your GlusterFS nodes__

GlusterFlow depends on Glupy being installed on your GlusterFS nodes first.

If you're using a recent version of Gluster (3.5 and above), then Glupy should
already be installed as part of it.

If you're using Gluster 3.3 or 3.4, then you'll need to install Glupy from the
external project repository:

  https://github.com/jdarcy/glupy

Generally you can git clone it, then do the standard make, make install.

__2. Install the JSON client on your GlusterFS nodes__

If you're using Glupy from the above GitHub repository, then the
glusterflowclient.py file needs to be in your PYTHONPATH.

Your PYTHONPATH can be found using:

    $ python -c "import sys; print sys.path"

Copy the glusterflowclient.py file to any of the directories there. eg:

    $ sudo cp json/glusterflowclient.py /usr/lib64/python2.6/site-packages/

If you are using GlusterFS 3.5 or a recent version of GlusterFS compiled from
git, the glusterflowclient.py file goes into the "glupy" subdirectory of the
installation instead:

    $ sudo cp json/glusterflowclient.py /usr/lib64/glusterfs/3git/xlator/features/glupy/

The "3git" part of the above string is a version number, and may be different
for you. (it's ok if it is)

__3. Point the JSON client at the JSON server__

With a text editor, open up the glusterflowclient.py file you just installed.
Change the IP address near the top of the file to point at your JSON server
(installed in the next step).

__4. Install the JSON server__

First install the Twisted Framework:

    $ pip install twisted

Then update the database connection string in the json server .py file.  It
needs working connection details to store the received json messages in the
web applications database:

    $ vi json/server.py

The server.py file doesn't depend on anything else from the GlusterFlow repo.
So, if you want, you can copy it to any other location in your filesystem.
(eg ~/bin/)

Personally, I just leave it in the GlusterFlow repo and run it from there. :)

__5. Install the GlusterFlow web application__

First, install Django:

    $ pip install Django

Then update the database connection details in glusterflow/settings.py.

    'HOST': 'my-database-server.example.org',
    'PORT': '',
    'NAME': 'databasename',
    'USER': 'databaseuser',
    'PASSWORD': 'somepassword',

Running it
----------

_To be written_

To Do
-----

* Expand the JSON client and server code (Python + Glupy) for more file operations.  Preferably all of them.  Shouldn't be too hard, just a bit time consuming.
* Add real interactivity to the bar graph and busiest files list, to enable refinement and drilling down into data sets.
* Add support for displaying data from multiple gluster hosts and clients (with appropriate selectors).
* Fix the bar graph display, so it shows scale, values, real time frame, and everything else useful.
* Add authentication
