#!/usr/bin/env bash

echo "Running the controller"

sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
