#!/bin/bash

source /development/env/bp/bin/activate
bp -v projects/christmas.yml -d=base.yml -d=strips.yml
