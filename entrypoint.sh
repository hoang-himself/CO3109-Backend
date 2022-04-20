#!/bin/bash

set -e

./manage.py migrate
./manage.py runserver "$@"
