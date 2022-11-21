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

TIMESIG = datetime.now().strftime("%Y-%m-%d_%H%M%S")
USR = os.getlogin()

SRC = "test"+os.sep+"SRC"
DST = "test"+os.sep+"DST"
BAK = "test"+os.sep+"BAK"



# ----- Main Function ----- #

def sync_directory(src_path, dst_path, bak_path=None, num_bak=5, 
                   include_subdirs=True, sync_deleted=False, logger=logging):

  # sanity check for src_path:
  if not os.path.isdir(src_path): 
    raise ValueError("Invalid SRC directory "+src_path)
  _, project = os.path.split(src_path) #TODO: erase if not needed

  # sanity check for dst_path:
  if not os.path.isdir(dst_path):
    dst_stub, check = os.path.split(dst_path)
    if not os.path.isdir(dst_stub): 
      raise ValueError("Invalid DST directory "+dst_path)

  # sanity check for bak_path:
  if bak_path is not None:
    if not os.path.isdir(bak_path):
      bak_stub, _ = os.path.split(bak_path)
      if os.path.isdir(bak_stub): 
        futil.mkdirtree(bak_path)
      else: 
        bak_path = None

  # copy whole folder if directory is completely new
  if not os.path.isdir(dst_path):
    logger.info(" mirroring SRC's whole directory to DST\n")
    if not DEBUG: futil.copytree(src_path, dst_path, logger=logger)
    return

  # get contents and modification times of existing directories
  if include_subdirs:
    src_folders, src_files = futil.relDirsFiles(src_path)
    _, dst_files = futil.relDirsFiles(dst_path)
  else:
    src_folders = []
    src_files = [obj for obj in os.listdir(src_path) if os.path.isfile(src_path+os.sep+obj)]
    dst_files = [obj for obj in os.listdir(dst_path) if os.path.isfile(dst_path+os.sep+obj)]
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
      elif sync_deleted: 
        deleted_files.append(file)

  if bak_path is not None:
    # move deleted files to BAK
    if len(deleted_files) > 0:
      for file in deleted_files: 
        logger.info(" (deleted) '"+file+"' moving from DST to BAK")
        if not DEBUG: 
          bak_stub = bak_path + os.sep + os.path.split(file)
          os.makedirs(bak_stub, exist_ok=True)
          futil.movefile(dst_path+os.sep+file, bak_path+os.sep+file, logger=logger)

    # copy changed files to BAK
    if len(changed_files) > 0:
      for file in changed_files: 
        logger.info(" (changed) '"+file+"' moving from DST to BAK")
        file_stub, file_ext = os.path.splitext(os.path.split(file)[-1])
        bak_folder = bak_path + os.sep + os.path.split(file)[0]
        
        if (num_bak is not None) and os.path.isdir(bak_folder):
          # make list of previous backup versions
          prev_bak_versions = []
          for obj in os.listdir(bak_folder):
            full_obj = bak_folder+os.sep+obj
            check_stub, check_ext = os.path.splitext(obj)
            check_stub = obj[:len(file_stub)]
            if check_ext==file_ext and check_stub==file_stub:
              prev_bak_versions.append(full_obj)
          #print(len(prev_bak_versions))#DEBUG

          # remove oldest backup if there are more than num_bak
          if len(prev_bak_versions) > num_bak-1:
            #print("HERE")#DEBUG
            prev_bak_versions = sorted(prev_bak_versions)
            if not DEBUG:
              logger.info("           removing oldest BAK version(s)")
              for obj in prev_bak_versions[:-(num_bak-1)]: os.remove(obj)

        # move DST's previous version to bak
        if not DEBUG: 
          bak_stub = bak_path + os.sep + os.path.split(file)[0]
          os.makedirs(bak_stub, exist_ok=True)
          file_stub, file_ext = os.path.splitext(bak_path+os.sep+file)
          dest_file = file_stub+"_fsync"+TIMESIG+"_"+file_ext
          futil.movefile(dst_path+os.sep+file, dest_file, logger=logger)

  # copy the SRC's directory tree to DST
  dst_tree = [dst_path+os.sep+obj for obj in src_folders]
  if (len(dst_tree) > 0) and not DEBUG: 
    futil.mkdirtree(dst_tree)

  # copy changed files
  for file in changed_files:
    logger.info(" (changed) '"+file+"' mirroring from SRC to DST")
    if not DEBUG: 
      futil.copyfile(src_path+os.sep+file, dst_path+os.sep+file, logger=logger)

  # copy new files
  for file in src_files:
    if not os.path.isfile(dst_path+os.sep+file):
      logger.info(" (new) '"+file+"' mirroring from SRC to DST")
      if not DEBUG: 
        futil.copyfile(src_path+os.sep+file, dst_path+os.sep+file, logger=logger)
  
  logger.info("")



class job:
  name = "fsync_job"
  SRC = "__invalid__"
  DST = "__invalid__"
  BAK = "__invalid__"
  num_bak = 5
  sync_deleted = False
  LOG = logging

  def __init__(self, src_path, dst_path, bak_path, num_bak=5, sync_deleted=False, name="fsync_job"):
    global TIMESIG
    TIMESIG = datetime.now().strftime("%Y-%m-%d_%H%M%S")

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
    if not os.path.isdir(self.SRC): 
      raise ValueError("Invalid SRC directory: "+self.SRC)
    if not os.path.isdir(self.DST): 
      raise ValueError("Invalid DST directory: "+self.DST)
    if not os.path.isdir(self.BAK): 
      raise ValueError("Invalid BAK directory: "+self.BAK)
    if self.sync_deleted: 
      print("[WARNING] sync_deleted is NOT recommended if multiple machines or backup jobs use DST!\n")

  def init_logfile(self):
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
    self.LOG.info("num_bak = "+str(self.num_bak)+"")
    self.LOG.info("sync_deleted = "+str(self.sync_deleted)+"\n\n")

  def finish(self):
    self.LOG.info("\n__________________________________________________\n\n\n")
    self.LOG.handlers.clear()


  def sync_directory(self):
    self.check_single()
    self.init_logfile()
    
    sync_directory(self.SRC, self.DST, self.BAK, num_bak=self.num_bak, 
                   sync_deleted=self.sync_deleted, logger=self.LOG)
    
    self.finish()


  def sync_individual(self, include=None, exclude=None):
    self.check_single()
    self.init_logfile()

    if include is not None:
      if isinstance(include, str): include = [include]
      self.LOG.info("include = "+str(include)+"\n")
    if (exclude is not None) and (include is None):
      if isinstance(exclude, str): exclude = [exclude]
      self.LOG.info("exclude = "+str(exclude)+"\n")

    # root directory
    sync_root = True
    if (exclude is not None) and (include is None) and ("." in exclude): 
      sync_root = False
    if (include is not None) and ("." not in include): 
      sync_root = False
    if sync_root:
      self.LOG.info("_ROOT_:")
      sync_directory(self.SRC, self.DST, self.BAK, num_bak=self.num_bak, 
                     include_subdirs=False, sync_deleted=self.sync_deleted, logger=self.LOG)
    
    # subdirectories
    src_projects = [self.SRC+os.sep+obj for obj in os.listdir(self.SRC) if os.path.isdir(self.SRC+os.sep+obj)]
    bak_projects = [self.BAK+os.sep+os.path.split(obj)[-1] for obj in src_projects]

    if include is not None:
      print("[WARNING] INCLUDE option not thoroughly tested yet!")
      src_projects = [obj for obj in src_projects if os.path.split(obj)[-1] in include]
      bak_projects = [obj for obj in bak_projects if os.path.split(obj)[-1] in include]
    if (exclude is not None) and (include is None):
      print("[WARNING] EXCLUDE option not thoroughly tested yet!")
      src_projects = [obj for obj in src_projects if os.path.split(obj)[-1] not in exclude]
      bak_projects = [obj for obj in bak_projects if os.path.split(obj)[-1] not in exclude]

    for src_project,bak_project in zip(src_projects,bak_projects):
      _,project = os.path.split(src_project)
      dst_project = self.DST+os.sep+project

      self.LOG.info(project+":")
      sync_directory(src_project, dst_project, bak_project, num_bak=self.num_bak,
                     sync_deleted=self.sync_deleted, logger=self.LOG)

    self.finish()


  def sync_root(self):
    self.check_single()
    self.init_logfile()
    
    sync_directory(self.SRC, self.DST, self.BAK, num_bak=self.num_bak, 
                     include_subdirs=False, sync_deleted=self.sync_deleted, logger=self.LOG)
    
    self.finish()