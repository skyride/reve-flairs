#!/bin/bash

# Activate virtualenv

# Run commands
../bin/python manage.py fetchallalliances
../bin/python manage.py setallianceactive
../bin/python manage.py updatereddit
../bin/python manage.py collectflairstats
