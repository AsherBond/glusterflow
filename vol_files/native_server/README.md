GlusterFS Native Server example
-------------------------------

The files in this directory show adding GlusterFlow to your native GlusterFS
server's .vol file.

Where to find yours
-------------------

On RHEL/CentOS 6.x, the GlusterFS server creates its native .vol files in
directories under:

    /var/lib/glusterd/vols/[volumename]/[volumename].[hostname].[full-path-name-of-brick].vol

For example:

    /var/lib/glusterd/vols/examplevolume/examplevolume.examplehost.export-brick1-glusterfs.vol

Adding GlusterFlow to yours
---------------------------

In the same directory as the README.md you're reading now, there's an example
of an untouched (no GlusterFlow) .vol file:

* 00_examplevolume.examplehost.export-brick1-glusterfs.vol_before_glusterflow

There's also a file with the text you need to add:

* 01_glusterflow.snippet

Lastly, there's an example showing the result, after
the text has been added to the untouched .vol file:

* 02_examplevolume.examplehost.export-brick1-glusterfs.vol_with_glusterflow_added

Notice that in addition to just adding the text, the __subvolumes__ option for
_examplevolume-index_ has been changed to point to
__examplevolume-glusterflowclient__?

That part is important, as it inserts the GlusterFlow client into the volume
translator chain.

Starting the native server with your .vol file
----------------------------------------------

To use the native GlusterFS server with your own .vol file, you have to
overwrite the GlusterFS generated one, then start _glusterfsd_ manually.

The command to overwrite the existing file will be similar to this:

    $ sudo cp -f my-native-server.vol /var/lib/glusterd/vols/examplevolume/examplevolume.examplehost.export-brick1-glusterfs.vol

You'll need to adjust the destination path and filename to match your
particular configuration.

The command to start glusterfsd manually is fairly long and complex.  I
normally cheat by doing a _ps -ef | grep glusterfsd_, killing the existing
process, then copying the command line arguments that ps -ef showed (adding
__--debug__ or __-N__ if I want to run it in the foreground):

    $ ps -ef|grep glusterfsd
    root      3579     1  0 03:48 ?        00:00:00 /usr/sbin/glusterfsd -s examplehost --volfile-id examplevolume.examplehost.export-brick1-glusterfs -p /var/lib/glusterd/vols/examplevolume/run/examplehost-export-brick1-glusterfs.pid -S /var/run/87eacd14412121245dd51e106f68ded9.socket --brick-name /export/brick1/glusterfs -l /var/log/glusterfs/bricks/export-brick1-glusterfs.log --xlator-option *-posix.glusterd-uuid=f44aa556-8404-4aca-9369-15fba8b72270 --brick-port 49154 --xlator-option examplevolume-server.listen-port=49154
    $ sudo kill 3579
    $ sudo /usr/sbin/glusterfsd -s examplehost --volfile-id examplevolume.examplehost.export-brick1-glusterfs -p /var/lib/glusterd/vols/examplevolume/run/examplehost-export-brick1-glusterfs.pid -S /var/run/87eacd14412121245dd51e106f68ded9.socket --brick-name /export/brick1/glusterfs -l /var/log/glusterfs/bricks/export-brick1-glusterfs.log --xlator-option *-posix.glusterd-uuid=f44aa556-8404-4aca-9369-15fba8b72270 --brick-port 49154 --xlator-option examplevolume-server.listen-port=49154 --debug
    [2013-05-13 02:52:30.554779] I [glusterfsd.c:1878:main] 0-/usr/sbin/glusterfsd: Started running /usr/sbin/glusterfsd version 3git ...
