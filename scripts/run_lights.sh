#!/bin/bash

source /development/env/bp/bin/activate
bp -v projects/christmas.json -d base.json -d strips.json
