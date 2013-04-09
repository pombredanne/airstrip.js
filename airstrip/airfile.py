from puke import *
import json

# This file is meant to manipulate the current project "airfile", containing lists of
# what the user has requested

PROJECT_AIRFILE_PATH = './airfile.json'

class AirFile():
  def __init__(self):
    self.project = json.loads('{}')
    if FileSystem.exists(PROJECT_AIRFILE_PATH):
      try:
        self.project = json.loads(FileSystem.readfile(PROJECT_AIRFILE_PATH))
      except:
        console.error('Your project airfile is horked and has been ignored!')
    # XXX should also check that the requested dependencies exist?

  def require(self, name, version):
    if name in self.project:
      if version in self.project[name]:
        console.error('Library %s in version %s is already required' % (name, version))
        return
      else:
        self.project[name].append(version)
    else:
      self.project[name] = [version]

    FileSystem.writefile(PROJECT_AIRFILE_PATH, json.dumps(self.project, indent=4))

  def remove(self, name, version = False):
    if not name in self.project:
      console.error('That library was not requested in the first place')
      return

    if version and (not version in self.project[name]):
      console.error('That version of the library was not requested in the first place')
      return

    if version:
      self.project[name].remove(version)
      console.info('Library %s version %s has been removed from dependencies' % (name, version))

    if (not version) or (not len(self.project[name])):
      self.project.pop(name, None)
      console.info('Library %s is no longer a dependency of your project' % name)

    FileSystem.writefile(PROJECT_AIRFILE_PATH, json.dumps(self.project, indent=4))

  def list(self):
    for i in self.project:
      print "%s: " % i
      for j in self.project[i]:
        print "    - version: %s" % j

  def isRequired(self, name):
    return name in self.project

  def requiredLibraries(self):
    return self.project
