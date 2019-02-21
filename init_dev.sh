#!/usr/bin/env bash

# Exposes the plugin (in it sources) to Deluge for development purposes.
mkdir temp

export PYTHONPATH=./temp
python setup.py build develop --install-dir ./temp
cp ./temp/WebAPI.egg-link ~/.config/deluge/plugins
rm -fr ./temp