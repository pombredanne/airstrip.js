# -*- coding: utf8 -*-

from puke import FileSystem as fs, console as console, prompt as prompt
import json
import licenses

AIRSTRIP_RC_PATH = '~/.airstriprc'

API = '3'

# Template for empty RC
EMPTY_RC = json.loads("""{
  "version": "",
  "company": {
    "name": "",
    "url": "",
    "mail": ""
  },
  "git": "",
  "ln": "en-us",
  "you": {
    "name": "",
    "url": "",
    "mail": "",
    "login": ""
  },
  "license": "MIT"
}""")


class AirRC():

  def __init__(self):
    if not fs.exists(AIRSTRIP_RC_PATH):
      fs.writefile(AIRSTRIP_RC_PATH, json.dumps(EMPTY_RC, indent = 2))

    try:
      self.rc = json.loads(fs.readfile(AIRSTRIP_RC_PATH))
    except:
      raise error.AirRC(error.BROKEN, "Your airstrip rc file (%s) is horked! Please rm or fix it" % AIRSTRIP_RC_PATH)

    if not self.rc['version'] == API:
      self.__ask__()

  def __ask__(self):
    defaults = self.rc.copy()
    for i in EMPTY_RC:
      if not i in defaults:
        defaults[i] = EMPTY_RC[i]
      elif not type(EMPTY_RC[i]) == str:
        for j in EMPTY_RC[i]:
          if not j in defaults[i]:
            defaults[i][j] = EMPTY_RC[i][j]



    console.warn("""You don't seem to have documented your default informations, 
or airstrip has an upgraded version that requires new infos.""")
    console.info("""These infos are stored only in the file %s, which you can edit manually.""" % AIRSTRIP_RC_PATH)

    console.info('First, provide informations about your company (if any - used generally for the author fields and copyright owner informations.)')
    self.rc['company']['name'] = prompt('Your company name (currently: %s)' % defaults['company']['name'], defaults['company']['name'])
    self.rc['company']['mail'] = prompt('Your company mail (currently: %s)' % defaults['company']['mail'], defaults['company']['mail'])
    self.rc['company']['url'] = prompt('Your company website / twitter (currently: %s)' % defaults['company']['url'], defaults['company']['url'])

    console.info('Now, about you - this will be used for the contributors/maintainers fields.')
    self.rc['you']['name'] = prompt('Your name (currently: %s)' % defaults['you']['name'], defaults['you']['name'])
    self.rc['you']['mail'] = prompt('Your mail (currently: %s)' % defaults['you']['mail'], defaults['you']['mail'])
    self.rc['you']['url'] = prompt('Your website / twitter (currently: %s)' % defaults['you']['url'], defaults['you']['url'])
    self.rc['you']['login'] = prompt('Your github name (currently: %s)' % defaults['you']['login'], defaults['you']['login'])

    keys = licenses.Licenses().list()
    self.rc['license'] = prompt('Default license for new projects (among %s)? (currently: %s)' % (keys, defaults['license']), defaults['license'])

    self.rc['git'] = prompt('Default git owner to use for new projects? (currently: %s)' % defaults['git'], defaults['git'])
    self.rc['ln'] = prompt('Default language for projects? (currently: %s)' % defaults['ln'], defaults['ln'])

    self.set('version', API)

  def get(self, key):
    if key in self.rc:
      return self.rc[key]
    return None

  def set(self, key, value):
    if key:
      self.rc[key] = value
    fs.writefile(AIRSTRIP_RC_PATH, json.dumps(self.rc, indent = 2))
