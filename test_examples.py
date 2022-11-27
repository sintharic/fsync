#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2022 https://github.com/sintharic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""



import os, sys
sys.path.append("examples")
import futil
import fsync
from time import sleep



directories = ["examples"+os.sep+"external", "examples"+os.sep+"local",
"examples"+os.sep+"external"+os.sep+".Projects",
"examples"+os.sep+"external"+os.sep+"Program Files",
"examples"+os.sep+"external"+os.sep+"Projects",
"examples"+os.sep+"local"+os.sep+"Data Source",
"examples"+os.sep+"local"+os.sep+"AppData",
"examples"+os.sep+"local"+os.sep+"Program Files",
"examples"+os.sep+"local"+os.sep+"Projects",
"examples"+os.sep+"local"+os.sep+"Data Source"+os.sep+"Folder0",
"examples"+os.sep+"local"+os.sep+"Data Source"+os.sep+"Folder1",
"examples"+os.sep+"local"+os.sep+"AppData"+os.sep+"Program0",
"examples"+os.sep+"local"+os.sep+"AppData"+os.sep+"Program1",
"examples"+os.sep+"local"+os.sep+"Program Files"+os.sep+"Program0",
"examples"+os.sep+"local"+os.sep+"Program Files"+os.sep+"Program1",
"examples"+os.sep+"local"+os.sep+"Program Files"+os.sep+"Program_special",
"examples"+os.sep+"local"+os.sep+"Projects"+os.sep+"Project0",
"examples"+os.sep+"local"+os.sep+"Projects"+os.sep+"Project1",
"examples"+os.sep+"local"+os.sep+"Projects"+os.sep+"Project_old",
"examples"+os.sep+"local"+os.sep+"AppData"+os.sep+"Program0"+os.sep+"Projects",
"examples"+os.sep+"local"+os.sep+"AppData"+os.sep+"Program1"+os.sep+"Projects",
"examples"+os.sep+"local"+os.sep+"Program Files"+os.sep+"Program0"+os.sep+"Presets",
"examples"+os.sep+"local"+os.sep+"Program Files"+os.sep+"Program0"+os.sep+"Templates",
"examples"+os.sep+"local"+os.sep+"Program Files"+os.sep+"Program1"+os.sep+"Presets",
"examples"+os.sep+"local"+os.sep+"Program Files"+os.sep+"Program1"+os.sep+"Templates",
"examples"+os.sep+"local"+os.sep+"Program Files"+os.sep+"Program_special"+os.sep+"Presets",
"examples"+os.sep+"local"+os.sep+"Program Files"+os.sep+"Program_special"+os.sep+"Templates",
"examples"+os.sep+"local"+os.sep+"Projects"+os.sep+"Project0"+os.sep+"Data",
"examples"+os.sep+"local"+os.sep+"Projects"+os.sep+"Project1"+os.sep+"Data"]

files = [folder+os.sep+"file0.dat" for folder in directories if folder.split(os.sep)[1]=="local"]
files += [folder+os.sep+"file1.dat" for folder in directories if folder.split(os.sep)[1]=="local"]

def update_files(i=0):
  for file in files:
    with open(file, "w") as fid: 
      fid.write("this is version %i\n" % i)

def reset():
  futil.removetree("examples"+os.sep+"local", ignore_errors=True)
  futil.removetree("examples"+os.sep+"external", ignore_errors=True)
  futil.mkdirtree(directories)
  update_files(0)

def sync_data():
  data = fsync.job("data")
  data.SRC = "examples"+os.sep+"local"+os.sep+"Data Source"
  data.DST = "examples"+os.sep+"external"+os.sep+"Data" # does not exist yet!
  data.BAK = None
  data.sync_directory()

def sync_root_data():
  data = fsync.job("data")
  data.SRC = "examples"+os.sep+"local"+os.sep+"Data Source"
  data.DST = "examples"+os.sep+"external"+os.sep+"Data" # does not exist yet!
  data.BAK = "examples"+os.sep+"external"+os.sep+".Data" # does not exist yet!
  data.num_bak = 2
  data.sync_root()

def test_data():
  reset()
  for i in range(2):
    update_files(i)
    sync_data()
    sleep(2)

def test_root_data():
  reset()
  for i in range(4):
    update_files(i)
    sync_root_data()
    sleep(2)

def sync_projects():
  projects = fsync.job("projects")
  projects.SRC = "examples"+os.sep+"local"+os.sep+"Projects"
  projects.DST = "examples"+os.sep+"external"+os.sep+"Projects" # already exists!
  projects.BAK = "examples"+os.sep+"external"+os.sep+".Projects"
  projects.num_bak = 2
  projects.sync_individual(exclude="Project_old")

def test_projects():
  reset()
  for i in range(4):
    update_files(i)
    sync_projects()
    sleep(2)
