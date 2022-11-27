#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
In this example, the whole SRC folder is synchronized with the destination.
This includes any files and folders contained in subdirectories.
Only files that have changed are going to be copied, overwriting a potentially
already existing version in the destination.
Old versions are NOT stored for roll-back in the future.
"""

import os, sys
sys.path.append("..")
import fsync
from test_examples import reset
reset()

# initialization of the sanc job with a representative name
data = fsync.job("data")

# update source and destination(s) of the sync job
data.SRC = "examples"+os.sep+"local"+os.sep+"Data Source"
data.DST = "examples"+os.sep+"external"+os.sep+"Data" # does not exist yet!
data.BAK = None

# to then start the synchronization, simply run the following:
#data.sync_directory()