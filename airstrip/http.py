import puke.Cache
import requests
import json

def get(url, cache = True, auth = False, noparse = False):
  # print " [http] simple get %s" % url
  if cache:
    id = puke.Cache.fetchHttp(url).split('/').pop()
    ret = puke.Cache.read(id)
  else:
    r = requests.get(url, auth = auth)
    ret = r.text or r.content

  if not noparse:
    ret = json.loads(ret)
  return ret

def delete(url, auth = False, noparse = False):
  r = requests.delete(url, auth = auth)
  ret = r.text or r.content

  if not noparse:
    ret = json.loads(ret)
  return ret

def post(url, data = False, headers = False, auth = False, noparse = False):
  r = requests.post(url, data = json.dumps(data), headers = headers, auth = auth)
  ret = r.text or r.content

  if not noparse:
    ret = json.loads(ret)
  return ret

def auth(uname, pwd):
  return requests.auth.HTTPBasicAuth(uname, pwd)
