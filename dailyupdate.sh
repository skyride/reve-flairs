#!/bin/bash

# Activate virtualenv
source ../bin/activate

# Run commands
./manage.py fetchallalliances
./manage.py setallianceactive
./manage.py updatereddit
./manage.py collectflairstats
