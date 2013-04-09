from puke import *
import json

def fetchgit(url, dest):
  # Require git on the system to have it
  System.check_package('git')
  # If directory exist, then update the tree
  if FileSystem.exists(dest):
    console.info('Updating')
    that = 'cd "%s"; git stash; git stash drop' % dest
    sh(that, output=True)
    that = 'cd "%s"; git pull --rebase; ' % dest
  else:
    if not FileSystem.exists(FileSystem.dirname(dest)):
      FileSystem.makedir(FileSystem.dirname(dest))
    console.info('Cloning')
    that = 'cd "%s"; git clone %s' % (FileSystem.dirname(dest), url)

  # Do the deed
  try:
    std = Std()
    sh(that, std=std, output=False)
    if std.err and (std.err.find('No stash found.') == -1):
      raise std.err
  except:
    # if puke.FileSystem.exists(dest):
    #   puke.FileSystem.remove(dest)
    console.error('Git operation failed! %s You need to manually fix or remove the directory.' % std.err)

def fetchsvn(url, dest):
  System.check_package('svn')
  # If directory exist, then update the tree
  if FileSystem.exists(dest):
    console.info('Updating')
    that = 'cd "%s"; svn up' % dest
  else:
    if not FileSystem.exists(FileSystem.dirname(dest)):
      FileSystem.makedir(FileSystem.dirname(dest))
    console.info('Cloning')
    that = 'cd "%s"; svn co %s %s' % (FileSystem.dirname(dest), url, FileSystem.basename(dest))

  # Do the deed
  try:
    std = Std()
    sh(that, std=std, output=False)
    if std.err:
     # and (std.err.find('No stash found.') == -1):
      raise std.err
  except:
    # if puke.FileSystem.exists(dest):
    #   puke.FileSystem.remove(dest)
    console.error('Svn operation failed! %s You need to manually fix or remove the directory.' % std.err)


def fetchone(url, dest, rename):
  remotefilename = url.split('/').pop()
  type = url.split('.').pop().lower()
  # Dirty trick to detect zip where the remote has no extension
  destype = rename.split('.').pop().lower()
  packpath = FileSystem.join(dest, remotefilename)
  if type == 'git':
    packpath = packpath.split('.')
    packpath.pop()
    packpath = '.'.join(packpath)
    console.info('Git repository')
    fetchgit(url, packpath)
    return packpath
  elif type == 'svn' or destype == 'svn':
    console.info('Svn repository %s %s' % (url, packpath))
    fetchsvn(url, packpath)
    return packpath
  else:
    deepcopy(FileList(url), dest + '/')
    if type == 'zip' or type == 'gz' or type == 'bz2' or destype == 'zip':
      try:
        dd = FileSystem.join(dest, remotefilename.replace('.' + type, ''))
        if FileSystem.exists(dd):
          FileSystem.remove(dd)
        FileSystem.makedir(dd)
        unpack(packpath, dd, verbose = False)
        # puke.FileSystem.remove(packpath)
      except Exception as e:
        sh('cd "%s"; 7z x "%s"' % (dd,  FileSystem.abspath(packpath)));
      FileSystem.remove(packpath)
    else:
      if remotefilename != rename:
        if not FileSystem.exists(FileSystem.dirname(FileSystem.join(dest, rename))):
          FileSystem.makedir(FileSystem.dirname(FileSystem.join(dest, rename)))
        sh('cd "%s"; mv "%s" "%s"' % (dest, remotefilename, rename))
      packpath = FileSystem.join(dest, rename)

def make(path, command):
  sh('cd "%s"; %s' % (path, command))
  # if type == 'rake':
  #   dorake(path, extra)
  # elif type == 'thor':
  #   dothor(path, extra)
  # elif type == 'make':
  #   domake(path, extra)
  # elif type == 'sh':
