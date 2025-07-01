#!/bin/sh
# wait-for-it.sh — чекає поки порт буде доступним

hostport=$1
shift

timeout=30

# парсинг timeout -t
while getopts t: opt; do
  case $opt in
    t) timeout=$OPTARG ;;
  esac
done

wait_for() {
  for i in $(seq $timeout) ; do
    nc -z $(echo $hostport | sed 's/:/ /')
    if [ $? -eq 0 ] ; then
      return 0
    fi
    sleep 1
  done
  return 1
}

if wait_for ; then
  exec "$@"
else
  echo "Timeout occurred waiting for $hostport"
  exit 1
fi
