from puke import *
import json
import os

AIRSTRIP_ROOT = os.path.dirname(os.path.realpath(__file__))

# System-wide yawns path
AIRSTRIP_YAWN_PATH = os.path.join(AIRSTRIP_ROOT, 'airs')

# Project user-defined yawns path
PROJECT_YAWN_PATH = './airs'

EMPTY_GLOBAL = """
      "description": "",
      "tags": [],
      "licences": [],
      "category": "library",
      "home": "http://",
      "tools": [],
      "depends": {},
      "versions": {
        "stable": {
          "package": "", 
          "resources": {
          },
          "build": [],
          "productions": {
          }
        }
      }
}"""


EMPTY_LOCAL_VERSION = """{
  "versions": {
    "version.name": {
      "package": "", 
      "resources": {
      },
      "build": [],
      "productions": {
      }
    }
  }
}"""

class Air():
  def __init__(self, name):
    self.name = name
    self.hasGlobal = False
    self.yawn = json.loads("""{
      "fancyName": "%s",
      %s""" % (name, EMPTY_GLOBAL))

    systemPath = FileSystem.join(AIRSTRIP_YAWN_PATH, '%s.json' % name)
    if FileSystem.exists(systemPath):
      try:
        self.yawn = json.loads(FileSystem.readfile(systemPath))
        self.hasGlobal = True
      except:
        console.error('The system yawn descriptor for %s is borked!' % name)

    self.hasLocal = False
    self.local = json.loads('{}')
    localPath = FileSystem.join(PROJECT_YAWN_PATH, '%s.json' % name)
    if FileSystem.exists(localPath):
      try:
        self.local = json.loads(FileSystem.readfile(localPath))
        self.hasLocal = True
      except:
        console.error('The yawn descriptor for %s in your project is borked!' % name)


  @staticmethod
  def exists(name):
    systemPath = FileSystem.join(AIRSTRIP_YAWN_PATH, '%s.json' % name)
    localPath = FileSystem.join(PROJECT_YAWN_PATH, '%s.json' % name)
    if not FileSystem.exists(localPath) and not FileSystem.exists(systemPath):
      return False
    return True



  def edit(self, globally = False):
    # Global edition, just go
    if globally:
      p = FileSystem.join(AIRSTRIP_YAWN_PATH, '%s.json' % self.name)
      c = self.yawn
    else:
      p = FileSystem.join(PROJECT_YAWN_PATH, '%s.json' % self.name)
      # No local data yet
      if not self.hasLocal:
        # if no global data either, populate with yawn
        if not self.hasGlobal:
          self.local = json.loads("""{
            "fancyName": "%s",
            %s""" % (self.name, EMPTY_GLOBAL))
        # if has global data, should start empty instead, as a version specialization
        else:
          self.local = json.loads(EMPTY_LOCAL_VERSION)
      c = self.local

    if not FileSystem.exists(p):
      FileSystem.writefile(p, json.dumps(c, indent=4))
    sh('open "%s"' % p)
    self.__init__(self.name)

  def get(self, version, key):
    if key == "name":
      return self.name
    keys = ['fancyName', 'description', 'tags', 'licences', 'category', 'tools', 'depends', 'package', 'resources', 'build', 'productions']
    #, 'versions']
    if not key in keys:
      console.error('There is no such thing as %s' % key)

    if self.hasGlobal and (version in self.yawn["versions"]):
      ref = self.yawn['versions'][version]
      parent = self.yawn
    elif self.hasLocal and (version in self.local["versions"]):
      ref = self.local['versions'][version]
      parent = self.local
    else:
      console.fail('The requested version (%s) does not exist' % version)

    if key in ref:
      return ref[key]
    if not key in parent:
      if "branch" in ref:
        return self.get(ref["branch"], key)
      else:
        console.error('No such key (%s)' % key)
        return False
    return parent[key]

  def versions(self):
    l1 = list()
    if self.hasGlobal:
      l1 = list(self.yawn["versions"])
    if self.hasLocal:
      l2 = list(self.local["versions"])
      for v in l2:
        l1.append(v)
    return l1

    # if self.hasGlobal:
    #   if key in self.yawn:
    #     ref = self.yawn[key]

    # if self.hasGlobal:
    #   ref = 
    #   return self.yawn[key]
    # if self.hasLocal:
    #   return self.local[key]
    # idx = keys.index(key)
    # types = ['', '', [], [], '', [], {}, '', {}, [], {}]
    # return types[idx]


  # yanks:
#   PackageFancyName:
#     Description: "long description"
#     Tags: "tags"
#   # License(s)
#     License: "Apache"
#   # Type (might impact destination)
#     Type: "tooling"
#   # Required tools to build
#     Tools: ['rake', 'sh']
#   # Dependency list
#     Depends:
#       FancyName: "min-version"
#       OtherFancyName:
#         min: "version"
#         max: "version"
#         recommended: "version"
#   # Per-version descriptors
#     Versions:
#       whatever:
#         Package: "package.json url"
#         # Can override default
#         Tools: 
#         Depends: 
#         License:
#         Type:

#         Resources:
#           localname: "remote_url"
#           otherlocalname: "remote_url"

#         Build:
#           command: ''

#         Productions:
#           destinationName: "buildedname"

