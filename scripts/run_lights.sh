#!/bin/bash

source /development/env/bp/bin/activate
bp -v projects/christmas.json -d=base.yml -d=strips.yml
