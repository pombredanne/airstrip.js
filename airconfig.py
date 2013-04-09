from puke import *
import json

# That file is meant to manipulate the airstrip configuration in the scope of the current project
# That project configuration by-default use the airstrip global configuration
# Possibly overriden by specific elements in the airconfig file in cwd.

# Should point to the globally installed airstrip configuration file
AIRSTRIP_CONFIG_PATH = 'global.json'
# The project in the current directory airconfig file, if any
PROJECT_CONFIG_PATH = './airconfig.json'


class AirConfig():
  def __init__(self):
    self.general = json.loads(FileSystem.readfile(AIRSTRIP_CONFIG_PATH))
    self.project = json.loads('{}')
    if FileSystem.exists(PROJECT_CONFIG_PATH):
      try:
        self.project = json.loads(FileSystem.readfile(PROJECT_CONFIG_PATH))
      except:
        console.error('Your project file configuration is horked and has been ignored!')

  def list(self):
    for i in self.general:
      value = self.general[i]['default']
      if i in self.project:
        value = "%s (default: %s)" % (self.project[i], self.general[i]['default'])
      print "%s: %s [%s]" % (i, value, self.general[i]['info'])


  def get(self, key):
    if not key in self.general:
      console.error('No such configuration flag (%s)' % key);
      return
    if key in self.project:
      return self.project[key]
    return self.general[key]["default"]

  def override(self, key, value):
    if not key in self.general:
      console.error('You are tryin to set a configuration switch that does not exist (%s)' % key);
      return
    if key in self.project:
      # Same value, ignore
      if value == self.project[key]:
        console.error('Ignoring unchanged property %s (value is already %s)' % (key, value))
        return
      # Default value, remove from self.project settings
      if self.general[key]["default"] == value:
        self.project.pop(key, None)
      # Otherwise change self.project key override
      else:
        self.project[key] = value
    elif self.general[key]["default"] == value:
      console.error('Ignoring unchanged property %s (default is already %s)' % (key, value))
      return
    else:
      self.project[key] = value

    console.info('Configuration switch "%s" has been set to "%s"' % (key, value))
    FileSystem.writefile(PROJECT_CONFIG_PATH, json.dumps(self.project, indent=4))
