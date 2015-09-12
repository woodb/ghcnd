#!/bin/bash

i=0
tox_args=()
for tox_env in $(tox -l); do
  if [ $(($i % $CIRCLE_NODE_TOTAL)) -eq $CIRCLE_NODE_INDEX ]
  then
    tox_args+=" -e$tox_env"
  fi
  ((i=i+1))
done

tox ${tox_args[@]}
