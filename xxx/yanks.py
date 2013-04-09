from puke import *

global yanks

def load():
  # XXX this should be "localinstallairs"
  projectairspath = 'airs'
  globalairspath = 'airs'
  l = FileList(globalairspath, filter = '*.yaml', exclude = '*xxx*');
  yanks = {}
  for i in l.get():
    a = Load(i)
    yanks = Utils.deepmerge(yanks, a.content['yanks'])

  l = FileList(projectairspath, filter = '*.yaml', exclude = '*xxx*');
  for i in l.get():
    a = Load(i)
    yanks = Utils.deepmerge(yanks, a.content['yanks'])

  # return yanks

def nothing(name):
  raise('No air defined by name %s' % name)


def get(name):
  if name in yanks:
    return yanks[name]
  nothing(name)

def show(name):
  print get(name)

def search(needle):
  yanks