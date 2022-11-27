#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
In this example, each immediate directory in the SRC root path ís synchronized 
individually into the DST directory.
If a file in SRC was modified since its last synchronization, the old version is
moved from the DST to the BAK directory.
Therefore, the BAK directory always keeps old versions of files to potentially
roll back changes in the future.
With these specific settings, exactly two older versions are kept for each file.
"""

import os, sys
sys.path.append("..")
import fsync
from test_examples import reset
reset()

# initialization of the sanc job with a representative name
projects = fsync.job("projects")

# update source and destination(s) of the sync job
projects.SRC = "examples"+os.sep+"local"+os.sep+"Projects"
projects.DST = "examples"+os.sep+"external"+os.sep+"Projects" # already exists!
projects.BAK = "examples"+os.sep+"external"+os.sep+".Projects"
projects.num_bak = 2

# to then start the synchronization, simply run the following:
#projects.sync_individual(exclude="Project_old")