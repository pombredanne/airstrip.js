from puke import *

class GitHelper():
  def __init__(self, remote, path):
    # Require git on the system to have it
    System.check_package('git')
    self.local = FileSystem.join(path, remote.split('/').pop().rstrip('.git'))
    self.remote = remote
    self.debug = False

  def __wrap__(self, path, command):
    std = Std()
    sh('cd "%s"; git %s' % (path, command), std = std, output = self.debug)
    if std.err and self.debug:
      console.error(std.err)


  def __clean__(self):
    self.__wrap__(self.local, 'reset --hard HEAD; git clean -f -d; git checkout master') # checkout .; git checkout master

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
    self.__wrap__(self.local, 'reset --hard HEAD; git clean -f -d; git checkout %s' % ref)

  def getPath(self):
    return self.local

