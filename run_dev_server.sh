#!/bin/bash -e

export GAE_SDK=~/google_appengine
PATH=$PATH:$GAE_SDK
dev_appserver.py .
