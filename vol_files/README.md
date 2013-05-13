GlusterFlow .vol file examples
------------------------------

This directory contains example GlusterFS .vol files and .vol file snippets
for GlusterFlow.

* [native_client](https://github.com/justinclift/glusterflow/tree/master/vol_files/native_client) - The GlusterFS client (uses FUSE)
* [native_server](https://github.com/justinclift/glusterflow/tree/master/vol_files/native_server) - The GlusterFS server
* [nfs_server](https://github.com/justinclift/glusterflow/tree/master/vol_files/nfs_server) - The GlusterFS NFS server

Each subdirectory has its own README.md file, explaining what's needed.

You __can't__ generally just copy one of the full .vol files from here into
your installation, because the embedded username/password pieces won't match
yours.

But, the files here should demonstrate how you can modify your own .vol files
to make things work.
