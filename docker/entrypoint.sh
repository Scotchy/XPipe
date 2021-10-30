#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

mkdir -p /data/artifacts && mkdir -p /data/mongodb

nohup mongod --dbpath /data/mongodb --port 27017&
pipeml --db-host 127.0.0.1 --db-port 27017 --host 0.0.0.0 --port 80 --artifacts-dir /data/artifacts
