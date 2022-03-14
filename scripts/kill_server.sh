#! /bin/bash

lsof -i tcp:4258 | grep -v PID | awk '{print $2}' | xargs kill