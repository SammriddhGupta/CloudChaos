#!/usr/bin/env bash

# This script will be run when Terraform pack your code

# Install dependencies
cd `dirname $0`
pip install -r requirements.txt -t ./package/
pip install https://pypi.python.org/packages/source/r/requests/requests-2.9.1.tar.gz
