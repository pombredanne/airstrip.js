#!/bin/sh
read -p "Are you sure you updated package.json and __init__.py version strings? Did you push a matching local tag as well?"
python setup.py register
python setup.py sdist upload
