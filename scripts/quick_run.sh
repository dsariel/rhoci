#!/bin/bash
rm -rf .venv
virtualenv .venv && source .venv/bin/activate
pip install .
rhoci-server --conf /etc/rhoci/staging-server.conf --debug -p 5000
