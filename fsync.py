#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
--------------------------------------------------
 One-Way Sync (Folder Backup) with Version Memory
--------------------------------------------------

CAUTION: sync_deleted not recommended if multiple devices or backup jobs use DST
TODO: use existing halt condition to allow safely cancelling a sync job



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



DEBUG = False



import os, sys
import futil
from datetime import datetime
import logging, traceback

TIMESIG = datetime.now().strftime("%Y-%m-%d_%Hh%M")
USR = os.getlogin()



# ----- Main Functions ----- #

def copy2bak(rel_filepath, bak_path, num_bak=1e85, logger=logging):



def sync_directory(src_path, dst_path, bak_path, num_bak=5, sync_deleted=False, logger=logging):

  # gather all absolute file paths for the project
  _,project = os.path.split(src_path)
  if not os.path.isdir(src_path): raise ValueError("Invalid SRC directory "+src_path)
  if os.path.isdir(bak_path):
    prev_bak_versions = sorted([obj for obj in os.listdir(bak_path) if os.path.isdir(bak_path+os.sep+obj)])
  else:
    prev_bak_versions = []
  bak_path = bak_path+os.sep+TIMESIG+"-"+USR

  #DEBUG
  #logger.info(" SRC = "+src_path)
  #logger.info(" DST = "+dst_path)
  #logger.info(" BAK = "+bak_path+"\n")

  # copy whole folder if directory is completely new
  if not os.path.isdir(dst_path):
    logger.info(" mirroring SRC's whole directory to DST\n")
    if not DEBUG: futil.copytree(src_path, dst_path)
    return

  # get contents of existing directories
  src_folders, src_files = futil.relDirsFiles(src_path)
  _, dst_files = futil.relDirsFiles(dst_path)
  src_time = [os.path.getmtime(src_path+os.sep+obj) for obj in src_files]
  dst_time = [os.path.getmtime(dst_path+os.sep+obj) for obj in dst_files]

  # find files that have been changed or deleted
  changed_files = []
  deleted_files = []
  for i_dst, file in enumerate(dst_files):
    i_src = futil.find(file, src_files)
    if i_src>=0: 
      if src_time[i_src] > dst_time[i_dst]+1:
        changed_files.append(file)
      elif sync_deleted: deleted_files.append(file)

  # create new backup version if files have changed / were deleted
  if (len(changed_files) > 0) or (len(deleted_files) > 0):
    logger.info(" creating BAK"+os.sep+bak_path.split(os.sep)[-1])
    if not DEBUG: os.makedirs(bak_path, exist_ok=True)

  # move deleted files to BAK
  if len(deleted_files) > 0:
    for file in deleted_files: 
      logger.info(" (deleted) '"+file+"' moving from DST to BAK")
      my_bak_path,name = os.path.split(bak_path+os.sep+file)
      if not DEBUG: 
        os.makedirs(my_bak_path, exist_ok=True)
        futil.movefile(dst_path+os.sep+file, my_bak_path+os.sep+name)

  # copy changed files to BAK
  if len(changed_files) > 0:
    for file in changed_files: 
      logger.info(" (changed) '"+file+"' moving from DST to BAK")
      my_bak_path,name = os.path.split(bak_path+os.sep+file)
      if not DEBUG: 
        os.makedirs(my_bak_path, exist_ok=True)
        futil.movefile(dst_path+os.sep+file, my_bak_path+os.sep+name)

  # copy the SRC's directory tree to DST
  dst_tree = [dst_path+os.sep+obj for obj in src_folders]
  if (len(dst_tree) > 0) and not DEBUG: 
    for path in dst_tree: os.makedirs(path, exist_ok=True)

  # copy changed files
  for file in changed_files:
    logger.info(" (changed) '"+file+"' mirroring from SRC to DST")
    if not DEBUG: futil.copyfile(src_path+os.sep+file, dst_path+os.sep+file)

  # copy new files
  for file in src_files:
    if not os.path.isfile(dst_path+os.sep+file):
      logger.info(" (new) '"+file+"' mirroring from SRC to DST")
      if not DEBUG: futil.copyfile(src_path+os.sep+file, dst_path+os.sep+file)

  # clean up oldest backup version(s)
  if len(changed_files) > 0:
    if len(prev_bak_versions) >= num_bak:
      for iBak in range(len(prev_bak_versions)-num_bak+1):
        logger.info(" deleting oldest backup "+prev_bak_versions[iBak])
        if not DEBUG: 
          futil.removetree(BAK+os.sep+prev_bak_versions[iBak])
  
  logger.info("")



def sync_files(src_path, dst_path, bak_path, num_bak=5, sync_deleted=False, logger=logging):
  """
  Copy ONLY the contained files in [src_path] to [dst_path]. Any subdirectories 
  in src_path are skipped!
  For all files that have been changed/deleted since last sync, backups are kept
  in [bak_path]. If there are more than [num_bak] backups, the oldest one is deleted.
  """

  _,project = os.path.split(src_path)
  if not os.path.isdir(src_path): raise ValueError("Invalid SRC directory.")
  if not os.path.isdir(bak_path):
    logger.info(" creating %s\n" % bak_path)
    if not DEBUG: os.makedirs(bak_path)
  if not os.path.isdir(dst_path):
    logger.info(" creating %s\n" % dst_path)
    if not DEBUG: os.makedirs(dst_path)
  prev_bak_versions = sorted([bak_path+os.sep+obj for obj in os.listdir(bak_path) if os.path.isdir(bak_path+os.sep+obj)])
  bak_path = bak_path+os.sep+TIMESIG+"-"+USR
  os.makedirs(bak_path, exist_ok=True)
  src_files = [obj for obj in os.listdir(src_path) if os.path.isfile(src_path+os.sep+obj)]
  dst_files = [obj for obj in os.listdir(dst_path) if os.path.isfile(dst_path+os.sep+obj)]

  #DEBUG
  #logger.info(project+":")
  #logger.info(" SRC = "+src_path)
  #logger.info(" DST = "+dst_path)
  #logger.info(" BAK = "+bak_path+"\n")
  
  changed_files = []
  for file in src_files:

    # file already existed
    if file in dst_files:
      src_time = os.path.getmtime(src_path+os.sep+file)
      dst_time = os.path.getmtime(dst_path+os.sep+file)

      # file has changed
      if (src_time > dst_time+1):
        changed_files.append(file)
        logger.info(" (changed) '"+file+"' moving from DST to BAK")
        if not DEBUG: 
          futil.movefile(dst_path+os.sep+file, bak_path+os.sep+file)
        logger.info(" (changed) '"+file+"' mirroring from SRC to DST")
        if not DEBUG: futil.copyfile(src_path+os.sep+file, dst_path+os.sep+file)

    # file is new
    else:
      logger.info(" (new) '"+file+"' mirroring from SRC to DST")
      if not DEBUG: futil.copyfile(src_path+os.sep+file, dst_path+os.sep+file)

  # clean up oldest backup versions
  if len(changed_files) > 0:
    if len(prev_bak_versions) >= num_bak:
      for iBak in range(len(prev_bak_versions)-num_bak+1):
        logger.info(" deleting oldest backup "+prev_bak_versions[iBak])
        if not DEBUG: futil.removetree(prev_bak_versions[iBak])

  logger.info("")



class job:
  name = "fsync_job"
  SRC = "__invalid__"
  DST = "__invalid__"
  BAK = "__invalid__"
  num_bak = 5
  sync_deleted = False
  INCLUDE = []
  EXCLUDE = []
  LOG = logging

  def __init__(self, src_path, dst_path, bak_path, num_bak=5, sync_deleted=False, name="fsync_job"):
    global TIMESIG
    TIMESIG = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    
    self.SRC = src_path
    self.DST = dst_path 
    self.BAK = bak_path 
    self.num_bak = num_bak
    self.sync_deleted = sync_deleted
    self.name = name+"_"+TIMESIG+"_"+USR

  def check_single(self):
    # Sanity checks
    if self.SRC[-1] == os.sep: self.SRC = self.SRC[:-1]
    if self.DST[-1] == os.sep: self.DST = self.DST[:-1]
    if self.BAK[-1] == os.sep: self.BAK = self.BAK[:-1]
    if not os.path.isdir(self.SRC): raise ValueError("Invalid SRC directory: "+self.SRC)
    if not os.path.isdir(self.DST): raise ValueError("Invalid DST directory: "+self.DST)
    if not os.path.isdir(self.BAK): raise ValueError("Invalid BAK directory: "+self.BAK)
    if self.sync_deleted: print("[WARNING] sync_deleted is NOT recommended if multiple machines or backup jobs use DST!\n")

  def start(self):
    # init log file
    self.LOG = logging.getLogger('logtest')
    self.LOG.setLevel(logging.DEBUG)
    logname = self.DST+"_fsync.log"
    if not os.path.isfile(logname): 
      with open(logname,"w") as f: pass
    logfile = logging.FileHandler(logname)
    logfile.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')#'%(name)s: %(asctime)s [%(levelname)s] %(message)s', datefmt='%y-%m-%d %H:%M:%S')
    logfile.setFormatter(formatter)
    self.LOG.addHandler(logfile)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')#('[%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    self.LOG.addHandler(console)

    if DEBUG: 
      self.LOG.info("+---------------------- DEBUG MODE ----------------------+")
      self.LOG.info("| None of the actions below have actually been performed |")
      self.LOG.info("| The log shows what would happen if DEBUG was False     |")
      self.LOG.info("+---------------------- DEBUG MODE ----------------------+\n")
    self.LOG.info("JOB = "+self.name)
    self.LOG.info("SRC = '"+self.SRC+"'")
    self.LOG.info("DST = '"+self.DST+"'")
    self.LOG.info("BAK = '"+self.BAK+"'")
    self.LOG.info("EXCLUDE = "+str(self.EXCLUDE))
    self.LOG.info("INCLUDE = "+str(self.INCLUDE)+"\n")
    self.LOG.info("num_bak = "+str(self.num_bak)+"")
    self.LOG.info("sync_deleted = "+str(self.sync_deleted)+"\n\n")

  def finish(self):
    self.LOG.info("\n__________________________________________________\n\n\n")
    self.LOG.handlers.clear()

  def sync_folder(self):
    self.check_single()
    self.start()
    
    sync_directory(self.SRC, self.DST, self.BAK, num_bak=self.num_bak, 
                   sync_deleted=self.sync_deleted, logger=self.LOG)
    
    self.finish()

  def sync_subfolders(self):
    self.check_single()
    self.start()

    # root directory
    sync_files(self.SRC, self.DST, self.BAK, num_bak=1e85, sync_deleted=self.sync_deleted, logger=self.LOG)
    
    # subdirectories
    src_projects = [self.SRC+os.sep+obj for obj in os.listdir(self.SRC) if os.path.isdir(self.SRC+os.sep+obj)]
    bak_projects = [self.BAK+os.sep+os.path.split(obj)[-1] for obj in src_projects]

    if len(self.INCLUDE) > 0:
      print("[WARNING] include option not thoroughly tested yet!")
      src_projects = [obj for obj in src_projects if os.path.split(obj)[-1] in self.INCLUDE]
      bak_projects = [obj for obj in bak_projects if os.path.split(obj)[-1] in self.INCLUDE]
    if len(self.EXCLUDE) > 0:
      print("[WARNING] updated skip option not thoroughly tested yet!")
      src_projects = [obj for obj in src_projects if os.path.split(obj)[-1] not in self.EXCLUDE]
      bak_projects = [obj for obj in bak_projects if os.path.split(obj)[-1] not in self.EXCLUDE]

    for src_project,bak_project in zip(src_projects,bak_projects):
      _,project = os.path.split(src_project)
      dst_project = self.DST+os.sep+project

      self.LOG.info(project+":")
      sync_directory(src_project, dst_project, bak_project,
                     sync_deleted=self.sync_deleted, logger=self.LOG)

    self.finish()

