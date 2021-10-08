#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

nohup mongod --dbpath /data --port 27017&
pipeml --db-host 127.0.0.1 --db-port 27017 --host 0.0.0.0 --port 80 --artifacts_dir /artifacts