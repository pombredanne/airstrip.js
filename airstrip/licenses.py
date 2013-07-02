# -*- coding: utf8 -*-

from puke import FileSystem as fs, FileList as filelist, sh as sh
import os
import error

AIRSTRIP_ROOT = os.path.dirname(os.path.realpath(__file__))

# System-wide yawns path
AIRSTRIP_LICENSES = fs.join(AIRSTRIP_ROOT, 'licenses')

# XXX kind of dirty hack to have it in the git local repo instead of system-wide
if fs.exists('airstrip/licenses'):
  AIRSTRIP_LICENSES = 'airstrip/licenses'

# Template for empty RC
EMPTY_LICENSE = """http://licenseurl

Licensed under the {name} license.

License text, bla."""

class Licenses():
  def __init__(self):
    self.licenses = {}
    for i in filelist(AIRSTRIP_LICENSES).get():
      d = fs.readfile(i).split('\n\n')
      licenseurl = d.pop(0)
      licensecontent = '\n\n'.join(d)
      name = fs.basename(i).split('.').pop(0).upper()
      self.licenses[name] = {"name": name, "url": licenseurl, "content": licensecontent}

  @staticmethod
  def exists(name):
    p = fs.join(AIRSTRIP_LICENSES, name)
    if fs.exists(p) and fs.isfile(p, True):
      return p
    return False

  def get(self, name):
    if not name or not name.upper() in self.licenses:
      raise error.License(error.MISSING, "Trying to read data from non existent license %s" % name)

    name = name.upper()

    return self.licenses[name]

  def edit(self, name):
    if not name:
      raise error.License(error.WRONG_ARGUMENT, "You need to pass a non-empty license name to the edit method")

    name = name.upper()

    path = fs.join(AIRSTRIP_LICENSES, name)
    if not name in self.licenses:
      self.licenses[name] = EMPTY_LICENSE.replace('{name}', name)
      fs.writefile(path, self.licenses[name])
    sh('open "%s"' % path, output = False)
    # XXX self.licenses will be lagging at this point

  def list(self):
    return self.licenses.keys()

  def remove(self, name):
    if not name or not name.upper() in self.licenses:
      raise error.License(error.MISSING, "Trying to remove non existent license %s" % name)

    name = name.upper()

    del self.licenses[name]
    p = fs.join(AIRSTRIP_LICENSES, name)
    fs.remove(p)