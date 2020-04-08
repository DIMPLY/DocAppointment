#!/bin/bash

# Start the first process
echo "going to start db..."
service postgresql start
#/usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c config_file=/etc/postgresql/9.3/main/postgresql.conf
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start postgresql: $status"
  exit $status
fi
echo "ok."

python3 db_init.py

echo "going to start doctor appointment api..."
python3 docapp.py
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start doctor appointment api: $status"
  exit $status
fi
echo "ok."

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

while sleep 60; do
  ps aux | grep postgre |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux | grep docapp | grep -q -v grep
  PROCESS_2_STATUS=$?
  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 ] -o $PROCESS_2_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi
done
