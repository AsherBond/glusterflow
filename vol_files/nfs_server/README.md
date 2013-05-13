GlusterFS NFS Server example
----------------------------

The files in this directory show adding GlusterFlow to your GlusterFS NFS
server's .vol file.

Where to find yours
-------------------

On RHEL/CentOS 6.x, the GlusterFS NFS server creates its .vol file at:

    /var/lib/glusterd/nfs/nfs-server.vol

Adding GlusterFlow to yours
---------------------------

In the same directory as the README.md you're reading now, there's an example
of an untouched (no GlusterFlow) .vol file:

* 00_nfs-server.vol_before_glusterflow

There's also a file with the text you need to add:

* 01_glusterflow.snippet

Lastly, there's an example showing the result, after the text has been added
to the untouched .vol file:

* 02_nfs-server.vol_with_glusterflow_added

Notice that in addition to just adding the text, the __subvolumes__ option
for _examplevolume_ has been changed to point to
__examplevolume-glusterflowclient__?

That part is important, as it inserts the GlusterFlow client into the volume
translator chain.

Starting the NFS server with your .vol file
-------------------------------------------

To use the GlusterFS NFS server with your own .vol file, you have to start
_glusterfs_ manually:

    $ sudo glusterfs -f my-nfs-server.vol --debug

If the output from __--debug__ is too verbose, you can run it in the
foreground with __-N__ instead of __--debug__.  This will still display any
stdout/stderr messages from the GlusterFlow client (useful if you're
debugging), but won't show the copious messages from other translators.

Alternatively, if you run glusterfs with neither __--debug__ nor __-N__, then
glusterfs will run in the background as a daemon.
