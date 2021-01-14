#!/bin/bash

set -eE

trap 'write_exit_code $?' EXIT
trap 'exit 1' ERR
trap 'echo "Terminating ..."; exit 1' SIGHUP SIGINT SIGQUIT SIGTERM
trap 'echo "Error in line $LINENO"; exit 1' SIGFPE

function write_exit_code {
  CODE_FILE=/home/scripts/codes

  echo "$1" > $CODE_FILE
}

count=0
while [ $count -lt 5 ]
do
  sleep 1
  (( count++ )) || true
  echo $count
done
