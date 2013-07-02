import puke.Cache
import requests
import json
import error
from xml.dom import minidom

okcodes = [200, 302]

def __parse__(content):
  try:
    content = json.loads(content)
  except:
    try:
      content = minidom.parseString(content)
    except:
      pass

  return content

def get(url, cache = True, auth = False, noparse = False):
  # print " [http] simple get %s" % url
  if cache:
    id = puke.Cache.fetchHttp(url).split('/').pop()
    ret = puke.Cache.read(id)
  else:
    r = requests.get(url, auth = auth)
    ret = r.text or r.content

    if not r.status_code in okcodes:
      raise error.Http(error.UNSPECIFIED, "Error! %s" % r.status_code)

  return __parse__(ret)

def delete(url, auth = False, noparse = False):
  r = requests.delete(url, auth = auth)
  ret = r.text or r.content

  if not r.status_code in okcodes:
    raise error.Http(error.UNSPECIFIED, "Error! %s" % r.status_code)

  return __parse__(ret)

def post(url, data = False, headers = False, auth = False, noparse = False):
  r = requests.post(url, data = json.dumps(data), headers = headers, auth = auth)
  ret = r.text or r.content

  if not r.status_code in okcodes:
    raise error.Http(error.UNSPECIFIED, "Error! %s" % r.status_code)

  return __parse__(ret)

def auth(uname, pwd):
  return requests.auth.HTTPBasicAuth(uname, pwd)
