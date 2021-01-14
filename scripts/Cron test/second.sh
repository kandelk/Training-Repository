#!/bin/bash

set -eE

trap 'catch_exit_code $?' EXIT
trap 'echo "Line $LINENO"; exit 1' ERR
trap 'echo "Terminating ..."; exit 1' SIGHUP SIGINT SIGQUIT SIGTERM
trap 'echo "Error in line $LINENO"; exit 1' SIGFPE

function catch_exit_code {
  case $1 in
  1)
    echo "Error"
    ;;
  0)
    echo "Success"
    ;;
  2)
    echo "Not started"
    ;;
  esac
}

PIDFILE=/home/scripts/second.pid
CODES_FILE=/home/scripts/codes

if [ -f $PIDFILE ]
then

  PID=$(cat $PIDFILE)

  if  ps -p "$PID" > /dev/null 2>&1
  then
    echo "Process exists! Exiting ..."
    exit 1
  else
    echo $$ > $PIDFILE
  fi
else
  echo $$ > $PIDFILE
fi

while [ ! -f $CODES_FILE ]; do
        sleep 1m
    done

    read -r code < $CODES_FILE
    rm $CODES_FILE

    if [ "$code" -eq 0 ]; then

      count=0
      while [ $count -lt 5 ]
      do
        sleep 1
        (( count++ )) || true
        echo $count
      done

    else
      exit 2
    fi

rm "$PIDFILE"