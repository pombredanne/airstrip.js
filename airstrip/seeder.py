from puke import *
import json
import os
import datetime

AIRSTRIP_ROOT = os.path.dirname(os.path.realpath(__file__))

class Seeder():
  def __init__(self):
    pass

  def project(self):
    defaultname = FileSystem.basename(FileSystem.realpath('.'))
    defaultusername = Env.get("PUKE_LOGIN", System.LOGIN)
    os = Env.get("PUKE_OS", System.OS).lower()

    # Licenses
    lic = FileList(FileSystem.join(AIRSTRIP_ROOT, 'boilerplates'), filter="*license-plate*")
    licenses = {}
    keys = []
    for i in lic.get():
      licensekey = i.split('.').pop().upper()
      u = FileSystem.readfile(i).split('\n\n')
      licenseurl = u.pop(0)
      licensecontent = ('\n\n').join(u)
      licenses[licensekey] = {"url": licenseurl, "content": licensecontent}
      keys.append(licensekey)

    # Existing git repo
    std = Std()
    gitdata = sh('git remote -v', std = std)
    if not std.err:
      gitdata = gitdata.split('\n')
      gitdata.pop()
      gitdata = gitdata.pop().split(' ')
      gitdata.pop()
      gitdata = gitdata.pop().split('\t')
      gitdata = gitdata.pop().split('/')
      gitdata = {'repo': gitdata.pop().rstrip('.git'), 'owner': gitdata.pop().split(':').pop()}
    else:
      gitdata = False

    prompt("""This will create a new project in the current working directory.
You can leave any of the following informations blank, or later edit the generated files to fit your mileage.
Hit enter to confirm.""")


    # User-provided informations
    name = prompt("Pick a fancy project name (default %s)" % defaultname, defaultname).strip()
    description = prompt("Short description for your project").strip()
    keywords = prompt("Keywords for your project (coma separated)").strip()


    if gitdata:
      prompt("Automatically detected github location %s. If this is not correct, break now and change that!" % gitdata)
    else:
      gitdata = prompt("Github owner/repositoryname (eg: toto/superproject):").strip()
      if gitdata:
        gitdata = gitdata.split('/')
        gitdata = {'repo': gitdata.pop(), 'owner': gitdata.pop()}
      else:
        gitdata = False

    ln = prompt("Project favorite language (default: en-us)", "en-us").strip()
    license = prompt("License for your project (choose from: %s, default: MIT)" % keys, 'MIT').strip()
    license = license.upper()
    homepage = prompt("Homepage for your project").strip()

    company = prompt("Your company name (or your name) as a copyright holder").strip()
    yourname = prompt("Your developer name (default %s)" % defaultusername, defaultusername).strip()
    yourmail = prompt("Your email").strip()
    yourwebsite = prompt("Your website / twitter / whatever").strip()

    s = Sed()
    s.add('{{miniboot.name}}', name)
    s.add('{{miniboot.ln}}', ln)
    s.add('{{miniboot.description}}', description)
    s.add('{{miniboot.keywords}}', json.dumps(keywords.split(',')))
    s.add('{{miniboot.companyname}}', company)
    now = datetime.datetime.now()
    s.add('{{miniboot.year}}', str(now.year))

    s.add('{{miniboot.you.name}}', yourname)
    s.add('{{miniboot.you.mail}}', yourmail)
    s.add('{{miniboot.you.web}}', yourwebsite)

    s.add('{{miniboot.path}}', FileSystem.realpath('.'))

    # print name
    # print ln
    # print description
    # print str(keywords.split(','))
    # print company
    # print now.year
    # print yourname
    # print yourmail
    # print yourwebsite

    track = ''
    rep = ''
    if gitdata:
      track = 'https://github.com/%s/%s/issues' % (gitdata["owner"], gitdata["repo"])
      rep = 'https://github.com/%s/%s.git' % (gitdata["owner"], gitdata["repo"])

    s.add('{{miniboot.tracker}}', track)
    s.add('{{miniboot.repository}}', rep)

    s.add('{{miniboot.homepage}}', homepage)

    lurl = ''
    lname = ''
    if not license in keys:
      console.warn('Ignoring unknown license %s' % license)
    else:
      lurl = licenses[license]["url"]
      lname = license

    s.add('{{miniboot.license.name}}', lname)
    s.add('{{miniboot.license.url}}', lurl)


    for item in ['.gitignore', '.pukeignore', '.jshintrc', 'README.md', 'LICENSE.md', 'package.json',
        'project.sublime-project', 'pukefile.py', 'helpers.py']:
      combine(FileSystem.join(AIRSTRIP_ROOT, 'boilerplates', item), item, replace=s)


    if license in keys:
      d = FileSystem.readfile('LICENSE.md')
      FileSystem.writefile('LICENSE.md', '%s\n\n%s' % (d, licenses[license]["content"]))

    FileSystem.writefile('package-%s-%s.json' % (Env.get("PUKE_LOGIN", System.LOGIN), Env.get("PUKE_OS", System.OS).lower()), '{}')
    deepcopy(FileList(FileSystem.join(AIRSTRIP_ROOT, 'boilerplates', 'src')), './src', replace = s)
    # combine(FileSystem.join(AIRSTRIP_ROOT, 'boilerplates', 'src', 'index.html'), './src/index.html', replace = s)
    # FileSystem.makedir('src')

  # puke.sh("touch pukefile.py")
  # puke.sh("touch %s.sublime-project")

