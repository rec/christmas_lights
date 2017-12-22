#!/bin/bash
ROOT=/development/christmas_lights
SCRIPT=$ROOT/scripts/run_lights.sh
LOG=$ROOT/log/log.txt

cd $ROOT
source $SCRIPT &>$LOG
