Native GlusterFS client (FUSE) example
--------------------------------------

The files in this directory show adding GlusterFlow to your native GlusterFS
clients' .vol file.  You use this when you want GlusterFlow sending info 
from the client side instead of the server side.

Where to find yours
-------------------

On RHEL/CentOS 6.x, the GlusterFS server creates native client .vol files at:

    /var/lib/glusterd/vols/[volumename]/[volumename]-fuse.vol

Adding GlusterFlow to yours
---------------------------

In the same directory as the README.md you're reading now, there's an example
of an untouched (no GlusterFlow) .vol file:

* 00_examplevolume-fuse.vol_before_glusterflow

There's also a file with the text you need to add:

* 01_glusterflow.snippet

Lastly, there's an example showing the result, after the text has been added
to the untouched .vol file:

* 02_examplevolume-fuse.vol_with_glusterflow_added

Notice that in addition to just adding the text, the __subvolumes__ option
for _examplevolume_ has been changed to point to
__examplevolume-glusterflowclient__?

That part is important, as it inserts the GlusterFlow client into the volume
translator chain.

Using the native client with your .vol file
-------------------------------------------

To use the native GlusterFS client with your own .vol file, you run _glusterfs_
manually, passing it the .vol file and a directory to mount it on:

    $ sudo glusterfs -f myvolume-fuse.vol /some/mount/point

Your GlusterFS volume should now be mounted on the mount point, and usable as
per normal.

When doing development, I often also use the __--debug__ command line argument
to see what's happening:

    $ sudo glusterfs --debug -f myvolume-fuse.vol /some/mount/point

If the output from __--debug__ is too verbose, you can use __-N__ instead.
This will still display any stdout/stderr messages from the GlusterFlow client
(can be useful), but won't show the copious messages from other translators.
