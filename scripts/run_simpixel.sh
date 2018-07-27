#!/bin/bash

source /development/env/bp/bin/activate
bp -vs projects/christmas.json -d=base.yml -d=simpixel.yml
