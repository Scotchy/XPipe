#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

nohup mongod --dbpath /data --port 27017&
pipeml --db-host 127.0.0.1 --db-port 27017 --port $PIPEML_PORT