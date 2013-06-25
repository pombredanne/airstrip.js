# -*- coding: utf8 -*-

from puke import *
import re
import error

class GitHelper():
  def __init__(self, remote, path):
    # Require git on the system to have it
    System.check_package('git')
    clean = re.sub('[.]git$', '', remote.split('/').pop())
    self.local = FileSystem.join(path, clean)
    self.remote = remote
    self.debug = False

  def __wrap__(self, path, command):
    if FileSystem.realpath('.') == FileSystem.realpath(path):
      raise error.License(error.TERRIBLE, "Trying to manipulate current path .git (%s)!" % path)
    std = Std()
    sh('cd "%s";' % path, std = std)
    if std.err:
      raise error.License(error.TERRIBLE, "Can't change pwd! (%s)!" % path)
    sh('cd "%s"; git %s' % (path, command), std = std)
    if std.err:
      raise error.License(error.GIT_ERROR, "Something bad happened! %s!" % std.err)
      console.error(std.err)

  def __clean__(self):
    self.__wrap__(self.local, 'reset --hard HEAD; git clean -f -d; git checkout master')

  def __rebase__(self):
    self.__wrap__(self.local, 'pull --rebase')

  def __clone__(self):
    self.__wrap__(FileSystem.dirname(self.local), 'clone %s' % self.remote)

  def ensure(self):
    base = FileSystem.dirname(self.local)
    if not FileSystem.exists(base):
      FileSystem.makedir(base)
    if not FileSystem.exists(self.local):
      self.__clone__()
    else:
      self.__clean__()
      self.__rebase__()

  def checkout(self, ref):
    self.__wrap__(self.local, 'reset --hard HEAD; git clean -f -d; git checkout %s; git reset --hard %s; git clean -f -d;' % (ref, ref))

  def getPath(self):
    return self.local

