#!/bin/bash

# Exist if any command fails
set -eux pipefail

pip install -t lib -r requirement.txt
(cd lib; zip ../my_deployment_package.zip -r .)
zip my_deployment_package.zip -u todo.py

# clean up 
rm -rf lib