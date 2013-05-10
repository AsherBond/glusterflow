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

* Python 2.7, Django 1.5, and PostgreSQL for the web application front end
* Python 2.7 and PostgreSQL for the JSON server (receives/collects data in JSON format)
* Python 2.x on the GlusterFS nodes, for the JSON client

Supported Platforms
-------------------

Linux for the Gluster nodes
* RHEL/CentOS 6.x are known to work
* Debian/Ubuntu should work (but untested so far)
* Others should work too.  The JSON client is extremely simple code. :)

Linux and MacOS X for the web app and JSON server
* MacOS X Lion is known to work
* RHEL/CentOS 6.x should work
* Debian/Ubuntu should work
* Others may work (untested)

Installation
------------

__1. Install Glupy on your GlusterFS nodes__

GlusterFlow depends on Glupy being installed on your GlusterFS nodes first.

If you're using a recent version of Gluster (3.5 and above), then Glupy
should already be installed as part of it.

If you're using Gluster 3.3 or 3.4, then you'll need to install Glupy from
the external project repository:

  https://github.com/jdarcy/glupy

Generally you can git clone it, then do the standard make, make install.

__2. Install the JSON client on your GlusterFS nodes__

If your using Glupy from the above GitHub repository:

    $ sudo cp json/glusterflowclient.py /usr/lib64/glusterfs/3git/xlator/features/glupy/

__3. Install the JSON server__

_To be written_

__4. Install the GlusterFlow web application__

_To be written_

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
