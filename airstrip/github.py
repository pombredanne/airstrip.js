from puke import *
import json
import yaml
import os
import base64
import sys, logging, os, traceback
import airrc
import keyring
import http
from osxkeyring import *

GITHUB_ROOT = "https://api.github.com"
GITGIT_ROOT = "https://github.com"
GITRAW_ROOT = "https://raw.github.com"


class Token():
  @staticmethod
  def get(auth):
    r = http.get("%s/authorizations" % GITHUB_ROOT, cache = False, auth = auth)
    for i in r:
      if i["note"] == "airstrip2":
        return i["token"]
    return False

  @staticmethod
  def remove(auth):
    r = http.get("%s/authorizations" % GITHUB_ROOT, cache = False, auth = auth)
    for i in r:
      if i["note"] == "airstrip2":
        http.delete("%s/authorizations/%s" % (GITHUB_ROOT, i["id"]), auth = auth)

  @staticmethod
  def create(auth):
    payload = {"scopes": ["public_repo", "repo"], "note": "airstrip2"}
    headers = {'content-type': 'application/json'}
    r = http.post("%s/authorizations" % GITHUB_ROOT, data = payload, headers = headers, auth = auth)
    return r["token"]


class Requestor():

  def __init__(self, uname, pwd):
    auth = http.auth(uname, pwd)
    token = Token.get(auth)
    if not token:
      token = Token.create(auth)
    self.token = token

  def query(self, fragment, nocache = False):
    if '?' in fragment:
      u = "%s/%s&access_token=%s" % (GITHUB_ROOT, fragment, self.token)
    else:
      u = "%s/%s?access_token=%s" % (GITHUB_ROOT, fragment, self.token)
    return http.get(u, cache = not nocache)

  def get(self, url, nocache = False):
    return http.get(url, cache = not nocache)





class GitHubInit():

  def __init__(self):
    # consoleCfg = logging.StreamHandler()
    # consoleCfg.setFormatter(logging.Formatter( ' %(message)s' , '%H:%M:%S'))
    # logging.getLogger().addHandler(consoleCfg)
    # logging.getLogger().setLevel(logging.DEBUG)

    rc = airrc.AirRC()

    if not rc.get('you')['login']:
      console.error('You must provide your github login to be able to use most of the API')

    uname = rc.get('you')['login'];

    if System.OS == 'Darwin':
      keyring.set_keyring(OSXPatchedKeyring())

    pwd = keyring.get_password('github.com', uname)
    if not pwd:
      console.fail('Unauthorized to access passwords, or no password found for that user in the internet keyring')

    # API requestor
    self.requestor = Requestor(uname, pwd)


  def search(self, keyword):
    return self.requestor.query("legacy/repos/search/%s?sort=stars&order=desc" % (keyword), nocache = True)

  def retrieve(self, owner, repo, dest, name):
    print " [github-connector] working on %s/%s" % (owner, repo)

    # Get refs for a starter
    refs = self.requestor.query("repos/%s/%s/git/refs" % (owner, repo), nocache = True)

    print " [github-connector] found %s refs" % len(refs)

    tags = {}
    # Get and init every tag, plus master
    for i in refs:
      tag = i["ref"].split('/').pop()
      if i["ref"].startswith("refs/tags/") or i["ref"].startswith("refs/heads/master"):
        tags[tag] = {"sha": i["object"]["sha"]}
        tags[tag]["tree"] = {}
        tags[tag]["package.json"] = {
          "name": repo,
          "author": owner,
          "version": tag
        }

    print " [github-connector] found %s tags" % len(tags)

    for tag in tags:
      sha = tags[tag]["sha"]
      print " [github-connector] analyzing tag %s (sha %s)" % (tag, sha)

      if tag == "master":
        tree = self.requestor.query("repos/%s/%s/git/trees/%s" % (owner, repo, sha), nocache = True)
      else:
        tree = self.requestor.query("repos/%s/%s/git/trees/%s" % (owner, repo, sha))

      date = self.requestor.query("repos/%s/%s/git/commits/%s" % (owner, repo, sha))
      if unicode(date['message']) == unicode("Not Found"):
        date = self.requestor.query("repos/%s/%s/git/tags/%s" % (owner, repo, sha))

      try:
        tags[tag]["date"] = {
          "authored": date["author"]["date"],
          "commited": date["committer"]["date"]
        }
      except:
        try:
          tags[tag]["date"] = {
            "authored": date["tagger"]["date"],
            "commited": date["tagger"]["date"]
          }
        except:
          tags[tag]["date"] = {
            "authored": None,
            "commited": None
          }
          console.error('Failed fetching a commit!!!')

      for item in tree["tree"]:
        if item["path"].lower() in ['package.json', 'component.json', '.travis.yml']:
          print " [github-connector] actually reading file %s" % item["path"]
          # XXX avoid API call
          item["url"] = "%s/%s/%s/%s/%s" % (GITRAW_ROOT, owner, repo, tag, item["path"].lower())

          if tag == "master":
            d = self.requestor.get(item["url"], nocache = True)
          else:
            d = self.requestor.get(item["url"])
          try:
            tags[tag][item["path"].lower()] = json.loads(d)
          except:
            try:
              tags[tag][item["path"].lower()] = yaml.load(d)
            except:
              pass
        elif "url" in item:
          tags[tag]["tree"][item["path"]] = item["url"]

    previous = {}
    p = FileSystem.join(dest, '%s.json' % name)
    if FileSystem.exists(p):
      previous = json.loads(FileSystem.readfile(p))

    previous["versions"] = tags
    previous["git"] = "%s/%s/%s" % (GITGIT_ROOT, owner, repo)

    FileSystem.writefile(p, json.dumps(previous, indent=4))



# g = GitHubInit()
# # g.retrieve("documentcloud", "backbone", "airstrip/airs", "backbone")
# # g.retrieve("twitter", "bootstrap", "airstrip/airs", "bootstrap")
# g.retrieve("emberjs", "ember.js", "airstrip/airs", "ember")
# g.retrieve("h5bp", "html5-boilerplate", "airstrip/airs", "h5bp")
# g.retrieve("wycats", "handlebars.js", "airstrip/airs", "handlebars")
# # g.retrieve("jquery", "jquery", "airstrip/airs", "jquery")
# g.retrieve("necolas", "normalize.css", "airstrip/airs", "normalize")
# # g.retrieve("madrobby", "zepto", "airstrip/airs", "zepto")







  # @staticmethod
  # def getblob(url, tmp):
  #   deepcopy(FileList(url), tmp)
  #   content = json.loads(FileSystem.readfile(FileSystem.join(tmp, url.split('/').pop())))
  #   return base64.b64decode(content["content"])

  # @staticmethod
  # def getraw(url, tmp):
  #   deepcopy(FileList(url), tmp)
  #   return FileSystem.readfile(FileSystem.join(tmp, url.split('/').pop()))


# /repos/:owner/:repo/git/trees/:sha

# 4a95dae0378f6e3058f70c51bff03318fb5fc63a






  # config = airc.AirConfig()
  # config.get('temporary')