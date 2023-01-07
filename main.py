import requests
import re
import random
import base64
import os
import json
import time
from re import search
from json import loads
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from colorama import Fore, init
from urllib3 import disable_warnings
import threading
from threading import Thread
import sys
import fade
from itertools import cycle
import colorama
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import colorama
import subprocess

green = Fore.GREEN
red = Fore.RED
white = Fore.WHITE

disable_warnings()


def removeaccount(i):
  accounts = open("gamepass_accounts.txt", 'r').read().splitlines()
  accounts.pop(accounts.index(i))
  accounts_write = open("gamepass_accounts.txt", "w")
  for k in accounts:
    accounts_write.write(f"{k}\n")


def authorize_login(email, password) -> None:

  def db64(data, altchars=b'+/'):
    if len(data) % 4 and '=' not in data:
      data += '=' * (4 - len(data) % 4)
    return base64.b64decode(data, altchars)

  headers = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'en-AU,en;q=0.9'
  }
  session = requests.session()
  email, password = email, password

  login = session.get('https://login.live.com/login.srf?',
                      headers=headers,
                      verify=False)

  flow_token = search(r'(?<=value=\")([^\"]*)', login.text)[0]
  uaid = session.cookies['uaid']

  email_payload = {
    'username': email,
    'uaid': uaid,
    'isOtherIdpSupported': False,
    'checkPhones': False,
    'isRemoteNGCSupported': True,
    'isCookieBannerShown': False,
    'isFidoSupported': True,
    'forceotclogin': False,
    'otclogindisallowed': True,
    'isExternalFederationDisallowed': False,
    'isRemoteConnectSupported': False,
    'federationFlags': 3,
    'flowToken': flow_token
  }
  session.post('https://login.live.com/GetCredentialType.srf',
               json=email_payload,
               verify=False,
               headers=headers)

  authorize_payload = {
    'i13': '0',
    'login': email,
    'loginfmt': email,
    'type': '11',
    'LoginOptions': '3',
    'lrt': '',
    'lrtPartition': '',
    'hisRegion': '',
    'hisScaleUnit': '',
    'passwd': password,
    'ps': '2',
    'psRNGCDefaultType': '',
    'psRNGCEntropy': '',
    'psRNGCSLK': '',
    'canary': '',
    'ctx': '',
    'hpgrequestid': '',
    'PPFT': flow_token,
    'PPSX': 'Passpor',
    'NewUser': '1',
    'FoundMSAs': '',
    'fspost': '0',
    'i21': '0',
    'CookieDisclosure': '0',
    'IsFidoSupported': '1',
    'i2': '1',
    'i17': '0',
    'i18': '',
    'i19': '1668743'
  }

  session.post('https://login.live.com/ppsecure/post.srf',
               data=authorize_payload,
               headers=headers,
               verify=False,
               allow_redirects=False)

  social = session.get(
    'https://sisu.xboxlive.com/connect/XboxLive?state=crime&ru=https://social.xbox.com/en-us/changegamertag',
    headers=headers,
    allow_redirects=True,
    verify=False)

  data = loads(db64(
    search(r'(?<=accessToken\=)(.*?)$', social.url)[0].strip()))
  user_hash = data[0]['Item2']['DisplayClaims']['xui'][0]['uhs']
  token = data[0]['Item2']['Token']

  return f"XBL3.0 x={user_hash};{token}"


def getlink(email_, passwored_):
  get_link_headers = authorize_login(email_, passwored_)

  get_link_req = requests.post(
    "https://profile.gamepass.com/v2/offers/47D97C390AAE4D2CA336D2F7C13BA074",
    headers={"authorization": get_link_headers})
  promo_link_json = json.loads(get_link_req.text)
  try:
    final_link = promo_link_json['resource']
  except:
    print(red + "Failed to fetch a promo link..." + white)

    return ''
  link_file = open("links.txt", "a")
  link_file.write(f"{final_link}\n")
  print(green + f"Successfully claimed a link --> {final_link}" + white)


account = open("gamepass_accounts.txt", 'r').read().splitlines()
for i in account:
  email = i.split("|")[0]
  password = i.split("|")[1]
  getlink(email, password)
  removeaccount(i)
