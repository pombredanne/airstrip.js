#!/usr/bin/env puke
# -*- coding: utf8 -*-
from puke.Task import task
global console, FileSystem
from puke import console, FileSystem

# import airfile
import re

global yawn
import air as yawn

global airc
import airconfig as airc

global airf
import airfile as airf

global airb
import airbuild as airb


@task("Show current configuration details (airstrip use), or set a configuration flag (airstrip use key value)")
def use(key = False, value = False):
  a = airc.AirConfig()
  if key == False:
    a.list()
  else:
    if not value == False:
      if value.lower() == "true":
        value = True
      # Doesn't f**** work like it should
      elif value.lower() == "false":
        value = False
    a.override(key, value)


@task("Show project required libraries (airstrip require), or add a new library to the list of project dependencies (airstrip require somelibrary), possibly in a specific version (airstrip require somelibrary somversion)")
def require(key = False, version = False):
  a = airf.AirFile()
  if key == False:
    a.list()
  else:
    if not version:
      version = "stable"
    # Get a yawn
    if not yawn.Air.exists(key):
      console.fail('No library by that name (%s)!' % key) 
    aero = yawn.Air(key)
    # Will fail if there is no such version
    aero.get(version, 'resources')
    # Otherwise ok!
    a.require(key, version)

@task("Remove a previously required library from the list of project dependencies (airstrip remove somelibrary), possibly a specific version of it (airstrip remove somelibrary someversion)")
def remove(key, version = False):
  a = airf.AirFile()
  a.remove(key, version)

@task("Edit a library description file (airstrip edit somelibrary). Passing true as second argument edits the descriptor globally.")
def edit(name, globally = False):
  if not globally == False:
    globally = True

  a = yawn.Air(name)
  # Doesn't f**** work like it should
  a.edit(globally)

@task("Show all available libraries (airstrip show), or detailed informations about a specific library (airstrip show somelibrary)")
def show(name = False):
  if not name:
    console.info('Show the full list of available libraries')
    return
  if not yawn.Air.exists(name):
    console.fail('No library by that name (%s)!' % name) 
  a = yawn.Air(name)
  console.info('*********************')
  console.info(a.get('stable', 'fancyName'))
  console.info('*********************')
  console.info(a.get('stable', 'description'))
  console.info('*********************')
  console.info(' - Category: %s' % a.get('stable', 'category'))
  console.info(' - Tags: %s' % a.get('stable', 'tags'))
  console.info(' - Licences: %s' % a.get('stable', 'licences'))
  console.info(' - Required tools to build: %s' % a.get('stable', 'tools'))
  console.info('*********************')
  console.info('Available versions: %s' % a.versions())

@task("Search packages for a given search string")
def search():
  pass

@task("Build the list of required libraries, or a specifically required library")
def build(name = False):
  a = airf.AirFile()
  libs = a.requiredLibraries()

  config = airc.AirConfig()

  if name:
    # Check the library exists and is required
    if not yawn.Air.exists(name):
      console.fail('No library by that name (%s)!' % name) 
    if not a.isRequired(name):
      console.fail('You have not required that library (%s)!' % name) 
    y = yawn.Air(name)
    for version in libs[name]:
      category = y.get(version, 'category')
      tmp = FileSystem.join(config.get('temporary'), category, name, version)
      destination = FileSystem.join(config.get('output'), category, name, version)
      airb.buildone(tmp, category, name, version, y.get(version, 'resources'), y.get(version, 'build'),
          y.get(version, 'productions'), destination, y.get(version, 'strict'))
  else:
    for name in libs:
      y = yawn.Air(name)
      for version in libs[name]:
        category = y.get(version, 'category')
        tmp = FileSystem.join(config.get('temporary'), category, name, version)
        destination = FileSystem.join(config.get('output'), category, name, version)
        airb.buildone(tmp, category, name, version, y.get(version, 'resources'), y.get(version, 'build'),
            y.get(version, 'productions'), destination, y.get(version, 'strict'))


  # if productions:

  # else:


# @task("Get a specific info about a specific version of a library")
# def get(name, version, key):
#   a = yawn.Air(name)
#   print a.get(version, key)





# @task("Default task")
# def default():
#   print('Victory')
#   pass
  # executeTask("build")
  # executeTask("deploy")


# @task("All")
# def all():
#   executeTask("build")
#   executeTask("mint")
#   executeTask("deploy")
#   executeTask("stats")


# @task("Wash the taupe!")
# def clean():
#   PH.cleaner()

# # Get whatever has been built and exfilter some crappy stuff
# @task("Deploying")
# def deploy():
#   PH.deployer(False)


# @task("Stats report deploy")
# def stats():
#   PH.stater(Yak.build_root)


# @task("Minting")
# def mint():
#   # list = FileList(Yak.build_root, filter = "*bootstrap*.js", exclude = "*-min.js")
#   # for burne in list.get():
#   #   minify(burne, re.sub(r"(.*).js$", r"\1-min.js", burne), strict = False, ecma3 = True)
#   # raise "toto"
#   # These dont survive strict
#   PH.minter(Yak.build_root, filter = "*raphael*.js,*ember*.js,*yahoo*.js,*yepnope*.js,*modernizr*.js,*jasmine*.js", excluding=",*/jax*,*mathjax/fonts*", strict = False)
#   PH.minter(Yak.build_root, excluding = "*raphael*.js,*ember*.js,*yahoo*.js,*yepnope*.js,*modernizr*.js,*jasmine*.js,*/jax*,*mathjax/fonts*", strict = True)

# @task("Deploying the static ressources, including approved third party dependencies")
# def build(buildonly = False):
#   # Crossdomain
#   sed = Sed()
#   sed.add("<\!--.*-->\s*", "")
#   combine("src/crossdomain.xml", Yak.build_root + "/crossdomain.xml", replace = sed)

#   # Robots
#   sed = Sed()
#   # XXX partially fucked-up
#   sed.add("(?:^|\n+)(?:#[^\n]*\n*)+", "")
#   combine("src/robots.txt", Yak.build_root + "/robots.txt", replace = sed)

#   # Deepcopy other stuff
#   sed = Sed()
#   PH.replacer(sed)
#   list = FileList("src/", exclude="*robots.txt,*crossdomain.xml,*index.html")
#   deepcopy(list, Yak.build_root, replace=sed)


#   # Process the remote leaves
#   description = {}

#   # Yak.collection.items()
#   colls = PH.getyanks()
#   # print Yak.collection
#   # for name in Yak.collection:
#   #   print name
#   for name in colls:
#     packinfo = colls[name]
#     # Temporary and build output directories definitions
#     tmpdir = FileSystem.join(Yak.tmp_root, "lib", packinfo["Destination"], name)
#     builddir = FileSystem.join(Yak.build_root, "lib", packinfo["Destination"], name)

#     desclist = []
#     marker = 'lib/%s/' % packinfo["Destination"]
#     for(localname, url) in packinfo["Source"].items():
#       # Do the fetch of 
#       PH.fetchone(url, tmpdir, localname)
#       # Copy files that "exists" to build directory
#       f = FileSystem.join(tmpdir, localname)
#       if FileSystem.exists(f):
#         d = FileSystem.join(builddir, localname)
#         # if not FileSystem.exists(FileSystem.dirname(d)):
#         #   FileSystem.makedir(FileSystem.dirname(d));
#         FileSystem.copyfile(f, d)
#         # Augment desclist with provided localname
#         desclist += [FileSystem.join(marker, name, localname)]

#     if "Build" in packinfo:
#       buildinfo = packinfo["Build"]
#       production = buildinfo["production"]
#       tmpdir = FileSystem.join(tmpdir, buildinfo["dir"])
#       extra = ''
#       if 'args' in buildinfo:
#         extra = buildinfo["args"]
#       if not buildonly or buildonly == name:
#         PH.make(tmpdir, buildinfo["type"], extra)

#       # Copy production to build dir
#       for(local, builded) in production.items():
#         f = FileSystem.join(tmpdir, builded)
#         d = FileSystem.join(builddir, local)
#         desclist += [FileSystem.join(marker, name, local)]
#         if FileSystem.isfile(f):
#           FileSystem.copyfile(f, d)
#         elif FileSystem.isdir(f):
#           deepcopy(FileList(f), d)

#       # ["coin%s" % key for key in ['item1', 'item2']]


#       # map((lambda item: "%s%s" % (name, item)), ['item1', 'item2'])
#       # # Augment description list with build result
#       # bitch = production.keys();

#       # for x in bitch:
#       #   bitch[x] = FileSystem.join(name, bitch[x]);

#       # print bitch
#       # raise "toto"

#       # desclist = desclist + production.keys()

#     description[name] = desclist
#     # description[name] = "%s%s" % (name, marker, ('",\n"%s' % marker).join(desclist)))

#     # miam += """
#     #   %s:
#     #     ["%s%s"]
#     # """ % (name, marker, ('", "%s' % marker).join(desclist))
#   # FileSystem.writefile(FileSystem.join(Yak.build_root, "airstrip.yaml"), yaml.dump(yaml.load('\n'.join(description))))


#     # print json.dumps(description)
#     # raise "toto"

#   shortversion = Yak.package['version'].split('-').pop(0).split('.')
#   shortversion = shortversion[0] + "." + shortversion[1]
#   PH.describe(shortversion, "airstrip", description)
#   # Write description file
#   # FileSystem.writefile(FileSystem.join(Yak.build_root, "airstrip.json"), '{%s}' % ',\n'.join(description))

#   # Build-up the description file
#   file = "src/index.html"
#   sed.add("{PUKE-LIST}", json.dumps(description, indent=4))
#   deepcopy(file, Yak.build_root, replace=sed)


