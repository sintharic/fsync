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



import os, sys, shutil
import logging, traceback



# ----- Utility Functions ----- #

def find(string, container):
  """ Find an string in an container of strings

  Parameters
  string : str
  container : list of str
    the container in which to search for <string>
  
  Returns
  -------
  f : int
    the index of the first occurrence of <string> in <container>.

  """

  for f, obj in enumerate(container):
    if obj == string: return(f)
  return(-1)


def mkdirtree(paths):
  """ Make a whole tree of directories

  Parameters
  ----------
  paths: str or list of str
    directories to be created 

  """

  if isinstance(paths, str): paths = [paths]
  for path in paths: os.makedirs(path, exist_ok=True)


def copyfile(sourcename, destname, logger=logging):
  """ Copy a file

  Any exceptions are redirected to the logging module.
  Inconsequential metadata mismatch errors are not raised.

  Parameters
  ----------
  sourcename: str
    file to be copied
  destname: str
    exact file name or folder, to which <sourcename> is copied
  logger: logging.Logger
    Logger, to which potential errors and warnings are redirected 

  """

  try: shutil.copy2(sourcename,destname)
  except OSError: 
    if os.path.isfile(destname): 
      print(" [WARNING] file metadata could not be copied")
    else:
      logger.debug(traceback.format_exc()+"\n")
      raise
  except BaseException:
    logger.debug(traceback.format_exc()+"\n")
    raise


def movefile(sourcename, destname, logger=logging):
  """ Move a file

  Any exceptions are redirected to the logging module.

  Parameters
  ----------
  sourcename: str
    file to be moved
  destname: str
    exact file name or folder, to which <sourcename> is moved
  logger: logging.Logger
    Logger, to which potential errors and warnings are redirected

  """

  try: shutil.move(sourcename, destname)
  except: 
    logger.debug(traceback.format_exc()+"\n")
    raise


def copytree(sourcename, destname, logger=logging):
  """ Recursively copy a whole directory tree

  Any exceptions are redirected to the logging module.
  Inconsequential metadata mismatch errors are not raised.

  Parameters
  ----------
  sourcename: str
    folder to be copied
  destname: str
    folder, to which <sourcename> is copied
  logger: logging.Logger
    Logger, to which potential errors and warnings are redirected

  """

  try: shutil.copytree(sourcename, destname)
  except OSError: 
    msg = """
------------------- WARNING -------------------
  OSError occured in shutil.copytree(src,dst).
  This may just be due to irrelevant metadata
  mismatch. Check logfile for full traceback.
------------------- WARNING -------------------
"""
    print(msg)
    logger.debug(traceback.format_exc()+"\n")
  except BaseException:
    logger.debug(traceback.format_exc()+"\n")
    raise


def removetree(foldername, logger=logging):
  """ Recursively remove a whole directory tree

  Any exceptions are redirected to the logging module.

  Parameters
  ----------
  foldername: str
    folder to be removed
  logger: logging.Logger
    Logger, to which potential errors and warnings are redirected
  
  """

  try: shutil.rmtree(foldername)
  except: 
    logger.debug(traceback.format_exc()+"\n")
    raise


def relDirsFiles(fullpath):
  """ List the whole directory tree and all files contained in a directory

  The file list contains files in the parent and all subdirectories.
  The directorytree can be passed to mkdirtree().

  Parameters
  ----------
  fullpath : str
    path to the folder whose contents are listed

  Returns
  -------
  folderlist : list of str
    the whole directory tree contained in <fullpath>, relative to <fullpath>
  filelist : list of str
    relative paths to all files contained in the directroy tree

  """

  if fullpath[-1] != os.sep: fullpath += os.sep

  # base path
  folderlist = []; filelist = []
  lsdir = sorted(os.listdir(fullpath))
  for obj in lsdir:
    if os.path.isdir(fullpath+obj): folderlist.append(obj)
    else: filelist.append(obj)

  # recursive through sub-directories
  found = True
  newfolders = folderlist.copy()
  while found:
    toadd = []
    for folder in newfolders:
      folder = folder + os.sep
      lsdir = sorted(os.listdir(fullpath+folder))
      for obj in lsdir:
        if os.path.isdir(fullpath+folder+obj): 
          toadd.append(folder+obj)
        else: filelist.append(folder+obj)
    if len(toadd):
      folderlist = folderlist + toadd
      newfolders = toadd.copy()
    else: found = False

  return(folderlist, filelist)


def recDirsFiles(fullpath):
  """ List the whole directory tree and all files contained in a directory

  Cleaner version of relDirsFiles(), where the order of elements in the returned 
  lists may be different.

  """

  if fullpath[-1] != os.sep: fullpath += os.sep

  # base path
  folderlist = []; filelist = []
  lsdir = sorted(os.listdir(fullpath))
  for obj in lsdir:
    if os.path.isdir(fullpath+obj): 
      morefolders, morefiles = recDirsFiles(obj)
      folderlist.append(obj)
      folderlist += [obj + os.sep + folder for folder in morefolders]
      filelist += [obj + os.sep + file for file in morefiles]
    else: filelist.append(obj)

  return(folderlist, filelist)

