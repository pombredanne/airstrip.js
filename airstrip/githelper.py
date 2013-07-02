# -*- coding: utf8 -*-

from puke import FileSystem as fs, System as sys, Std, sh
import re
import error

class GitHelper():
  def __init__(self, remote, path):
    # Require git on the system to have it
    sys.check_package('git')
    clean = re.sub('[.]git$', '', remote.split('/').pop())

    self.local = fs.join(path, clean)
    self.remote = remote
    self.debug = False

    base = fs.dirname(self.local)
    if not fs.exists(base):
      fs.makedir(base)
    if not fs.exists(self.local):
      self.__clone__()
    else:
      self.__clean__()
      self.__rebase__()


  def __wrap__(self, path, command):
    if fs.realpath('.') == fs.realpath(path):
      raise error.License(error.TERRIBLE, "Trying to manipulate current path .git (%s)!" % path)
    std = Std()
    sh('cd "%s";' % path, std = std)
    # XXX dead broken right now
    # if std.err:
    #   raise error.License(error.TERRIBLE, "Can't change pwd! (%s)!" % path)
    sh('cd "%s"; git %s' % (path, command), std = std)
    # if std.err:
    #   raise error.License(error.GIT_ERROR, "Something bad happened! %s!" % std.err)
    #   console.error(std.err)

  def __clean__(self):
    self.__wrap__(self.local, 'reset --hard HEAD; git clean -f -d; git checkout master')

  def __rebase__(self):
    self.__wrap__(self.local, 'pull --rebase')

  def __clone__(self):
    self.__wrap__(fs.dirname(self.local), 'clone %s' % self.remote)

  def checkout(self, ref):
    self.__wrap__(self.local, 'reset --hard HEAD; git clean -f -d; git checkout %s; git reset --hard %s; git clean -f -d;' % (ref, ref))

  def path(self):
    return self.local

