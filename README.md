GlusterFlow
===========

A cluster wide profiling and analysis web app for GlusterFS

Screenshot
----------

![GlusterFlow Screenshot](https://github.com/justinclift/glusterflow/raw/master/ui/static/ui/screenshots/glusterflow_screenshot_0.0.1.png "GlusterFlow Screenshot")

Status
------

This is in very early stages of development, but making good progress already

Requirements
------------

* Glupy (part of Gluster 3.5 and above)
* Python 2.7.x
* ElasticSearch 0.90.x
* Kibana 3
* LogStash 1.2.x

Supported Platforms
-------------------

Linux for the Gluster nodes:
* RHEL/CentOS 6.x is known to work
* Debian/Ubuntu should work (but untested so far)

For the LogStash, ElasticSearch, and Kibana nodes, anything
supported by those platforms should be good enough.


Installation
------------

__1. Ensure you have a working LogStash, ElasticSearch, Kibana 3 cluster__

The instructions on the LogStash website should get you started.

__2. Install Glupy on your GlusterFS nodes__

GlusterFlow depends on Glupy being installed on your GlusterFS nodes first:

* If you're using a recent version of Gluster (3.5 and above), then Glupy is
already a part of it.
* If you're using Gluster 3.3 or 3.4, then you'll need to install Glupy from
the external project repository:

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; https://github.com/jdarcy/glupy

__3. Install the Gluster filter__

Follow the README instructions in the filter/ directory


Running it
----------

With the Glusterflow filter active, GlusterFlow messages should automatically
be sent to ElasticSearch on the local host, for viewing in Kibana.


To Do
-----

* Find out how to use "terms facets" to return facet counts, to establish the
  busiest files for each time period.
* Add authentication.
