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



import os
import futil
import fsync


# test directories
SRC = fsync.SRC #"test"+os.sep+"SRC"
DST = fsync.DST #"test"+os.sep+"DST"
BAK = fsync.BAK #"test"+os.sep+"BAK"
folders = ["Folder0", "Folder1", 
  "Folder1"+os.sep+"Subfolder0", "Folder1"+os.sep+"Subfolder1", 
  "Folder1"+os.sep+"Subfolder1"+os.sep+"Datafolder"
]
folders = [SRC + os.sep + folder for folder in folders]
files = [folder + os.sep + "file0.dat" for folder in folders]
files += [folder + os.sep + "file1.dat" for folder in folders]

# set up folders and files in SRC
for path in [SRC,DST,BAK]: futil.mkdirtree(path)
for path in folders: futil.mkdirtree(path)

def update_test_files(i):
  for file in files:
    with open(file, "w") as fid: 
      fid.write("this is version %i\n" % i)

# create sync job
def main(i):
  update_test_files(i)
  JOB = fsync.job(src_path=SRC, dst_path=DST, bak_path=BAK, 
                  num_bak=2, name="test")
  JOB.sync_folder()

if __name__=="__main__": main()