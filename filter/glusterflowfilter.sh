#!/bin/env bash

# Change this to 1 to log into /var/log/glusterfs/filter.log
DEBUG=1

function addVolume {
  VOLUME_FILE="$1"
  VOLUME_NAME="$2"
  MATCH_TEXT="$3"
  NEXT_VOL_TEXT="$4"

  # Generate a new temporary file name
  TEMP_FILE=`mktemp --tmpdir nfstempXXXXXXXX`

  # Work out where to split the original file
  TOTAL_LINES=`wc -l $VOLUME_FILE | cut -d ' ' -f 1`
  SPLIT_LINE=`egrep -n "^\$MATCH_TEXT$" $VOLUME_FILE | cut -d ':' -f 1`
  HEAD_LINES=`expr $SPLIT_LINE - 1`
  TAIL_LINES=`expr $TOTAL_LINES - $SPLIT_LINE + 2`

  # Create the initial part of the new volume file
  head -n $HEAD_LINES $VOLUME_FILE > $TEMP_FILE

  # Add our custom volume text
  echo "volume ${VOLUME_NAME}-glusterflowclient" >> $TEMP_FILE
  echo "    type features/glupy" >> $TEMP_FILE
  echo "    option module-name glusterflowclient" >> $TEMP_FILE
  echo "    subvolumes ${VOLUME_NAME}-${NEXT_VOL_TEXT}" >> $TEMP_FILE
  echo "end-volume" >> $TEMP_FILE

  # Add the ending part of the volume file
  tail -n $TAIL_LINES $VOLUME_FILE | sed "s/$NEXT_VOL_TEXT/glusterflowclient/" >> $TEMP_FILE

  # Overwrite the original volume file with the new one
  mv -f $TEMP_FILE $VOLUME_FILE

  # Indicate everything went ok
  return 0
}

# Retrieve info used in this script
DATE=`date`
VOLUME_FILE=$1

# Adjust log file destination according to debug flag
[[ $DEBUG -eq 0 ]] && LOG_FILE=/dev/null || LOG_FILE=/var/log/glusterfs/filter.log

echo "New run: $DATE" >> $LOG_FILE
echo "VOLUME_FILE = $VOLUME_FILE" >> $LOG_FILE

# Determine which part of GlusterFS this volume
# file is for (eg fuse client, nfs server, native server, etc)
VOLUME_TYPE=UNKNOWN
if [ `expr match "$VOLUME_FILE" '.*nfs-server.vol$'` -ne 0 ]; then
  # This is an NFS server volume file
  VOLUME_TYPE=NFS-SERVER
elif [ `expr match "$VOLUME_FILE" '.*trusted-.*-fuse.vol$'` -ne 0 ]; then
  # This is a trusted fuse client volume file
  VOLUME_TYPE=TRUSTED-FUSE-CLIENT
elif [ `expr match "$VOLUME_FILE" '.*/.*-fuse.vol$'` -ne 0 ]; then
  # This is a standard fuse client volume file
  VOLUME_TYPE=FUSE-CLIENT
elif [ `expr match "$VOLUME_FILE" '.*/.*-glusterfs.vol$'` -ne 0 ]; then
  # This is a standard native server volume file
  VOLUME_TYPE=NATIVE-SERVER
fi
echo "VOLUME_TYPE = $VOLUME_TYPE" >> $LOG_FILE

# Determine the volume name
if [ "$VOLUME_TYPE" = "NATIVE-SERVER" ]; then
  VOLUME_NAME=`egrep "^volume (.*)-posix" $VOLUME_FILE | cut -d ' ' -f 2 | cut -d '-' -f 1`
else
  VOLUME_NAME=`egrep "^volume (.*)-client-0" $VOLUME_FILE | cut -d ' ' -f 2 | cut -d '-' -f 1`
fi
echo "VOLUME_NAME = $VOLUME_NAME" >> $LOG_FILE

# Process the volume file according to its type
case $VOLUME_TYPE in
  "NFS-SERVER")
    # We add our new volume between the default
    # "$VOLUME_NAME-write-behind" one and the "$VOLUME_NAME" one

    addVolume "$VOLUME_FILE" "$VOLUME_NAME" "volume $VOLUME_NAME" "write-behind"

    # Log the result
    if [ $? -eq 0 ]; then
      echo "RESULT = GlusterFlow client added to NFS server volume" >> $LOG_FILE
    else
      echo "RESULT = ERROR adding GlusterFlow client to NFS server volume" >> $LOG_FILE
    fi
    ;;

  "TRUSTED-FUSE-CLIENT")
    # To be done
    ;;

  "FUSE-CLIENT")
    # To be done
    ;;

  "NATIVE-SERVER")
    # We add our new volume between the default
    # "$VOLUME_NAME-io-threads" one and the "$VOLUME_NAME-index" one

    addVolume "$VOLUME_FILE" "$VOLUME_NAME" "volume $VOLUME_NAME-index" "io-threads"

    # Log the result
    if [ $? -eq 0 ]; then
      echo "RESULT = GlusterFlow client added to native server volume" >> $LOG_FILE
    else
      echo "RESULT = ERROR adding GlusterFlow client to native server volume" >> $LOG_FILE
    fi
    ;;

  *)
    # Unknown volume file type

    # If debugging is enabled, make a copy of it for analysis
    if [ $DEBUG -eq 1 ]; then
      cp $VOLUME_FILE /tmp/temp.vol
      echo "RESULT = Unknown type volume file copied to /tmp/temp.vol" >> $LOG_FILE
    fi
    ;;
esac

# Add a blank line between runs of this script
echo >> $LOG_FILE

