GlusterFlow
===========

A cluster wide profiling and analysis web app for GlusterFS

Status
------

This is in very early stages of development, but making good progress already

Screenshots
-----------

![Usage Graph](https://github.com/justinclift/glusterflow/raw/master/screenshots/glusterflow_usage_graph.png "Usage Graph")
![Most Used Files](https://github.com/justinclift/glusterflow/raw/master/screenshots/glusterflow_most_used_files.png "Most Used Files")
![Most Common Operations](https://github.com/justinclift/glusterflow/raw/master/screenshots/glusterflow_common_operations.png "Most Common Operations")

Requirements
------------

* Glupy (part of Gluster 3.5 and above, but can be installed manually on Gluster 3.4)
* Python 2.7.x
* ElasticSearch 0.90.x
* Kibana 3
* LogStash 1.3.3 or above

Supported Platforms
-------------------

Linux for the GlusterFS nodes:
* RHEL/CentOS 6.x is known to work
* Fedora 19 is known to work
* Debian/Ubuntu should work (but untested so far)

For the LogStash, ElasticSearch, and Kibana nodes, anything
supported by those platforms should be good enough.


Installation
------------

__1. Ensure you have a working LogStash, ElasticSearch, & Kibana 3 cluster__

The instructions on the [LogStash](http://logstash.net) website should get you started.

__2. Install the Logstash Formatter for Python__

At present, we pass information to LogStash using a file based approach, so
need to install the "logstash_formatter" Python module.

On a new minimal install of CentOS 6.5, the normal pip installation command
doesn't work out of the box so you'll need to run this first:

    $ sudo yum install python-pip
    $ sudo pip install --upgrade pip setuptools
    $ sudo pip install Distribute

After that, the normal pip installation commands should work:

    $ sudo pip install logstash_formatter

__3. Ensure you have Glupy on your GlusterFS nodes__

GlusterFlow depends on Glupy being installed on your GlusterFS nodes first:

* If you're using a recent version of GlusterFS (3.5 and above), then Glupy is
already a part of it.
* If you're using GlusterFS 3.3 or 3.4, then you'll need to install Glupy from
the external project repository:

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; https://github.com/justinclift/glupy

__4. Install the GlusterFlow filter__

Follow the README instructions in the filter/ directory

__5. Install the GlusterFlow Translator__

Instructions still To Be Written.
    

Running it
----------

With the GlusterFlow filter active, GlusterFlow messages should automatically
be sent to ElasticSearch on the local host, for viewing in Kibana.


To Do
-----

* Update for multi-node operation (hopefully not hard)
* Write instructions for using the Kibana Dashboard
* Ensure the "Most Used Files" panel only shows files (not dir names)
* Add a "Most Used Directories" panel
* Add authentication
* Consider adding thresholds and alerting
* Investigate replacing the filter script with the Python code jdarcy mentioned
