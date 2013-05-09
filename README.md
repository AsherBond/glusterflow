GlusterFlow
===========

Gluster cluster wide profiling and analysis web app.

Uses Django 1.5 and Python 2.7 for the web application component.

Data is sent from the Gluster nodes (using UDP) via a simple JSON client, using Glupy and Python 2.x.

This is in very early stages of development, but making good progress already.


Screenshot
----------

![GlusterFlow Screenshot](https://github.com/justinclift/glusterflow/raw/master/ui/static/ui/screenshots/glusterflow_screenshot_0.0.1.png "GlusterFlow Screenshot")


To Do
-----

* Expand the JSON client and server code (Python + Glupy) for more file operations.  Preferably all of them.  Shouldn't be too hard, just a bit time consuming.
* Add real interactivity to the bar graph and busiest files list, to enable refinement and drilling down into data sets.
* Add support for displaying data from multiple gluster hosts and clients (with appropriate selectors).
* Fix the bar graph display, so it shows scale, values, real time frame, and everything else useful.


Installation
------------

1. Install Glupy on your GlusterFS nodes

GlusterFlow depends on Glupy being installed on your GlusterFS nodes first.

If you're using a recent version of Gluster (3.5 and above), then Glupy
should already be installed as part of it.

If you're using Gluster 3.3 or 3.4, then you'll need to install Glupy from
the external project repository:

  https://github.com/jdarcy/glupy

Generally you can git clone it, then do the standard make, make install.

2. Install the JSON client on your GlusterFS nodes

If your using Glupy from the above GitHub repository
    $ sudo cp json/glusterflowclient.py /usr/lib64/glusterfs/3git/xlator/features/glupy/


3. The JSON server 


4. The GlusterFlow web application 











