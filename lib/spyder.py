# Date: 11/27/2017
# Author: Ethical-H4CK3R
# Description: Browser

from time import time
from random import choice
from cookielib import LWPCookieJar 
from requests import get as urlopen
from mechanize import _http, Browser
from commands import getoutput as shell
from constants import ip_fetch_timeout, brwsr_max_refresh, useragents, network_manager_time

class Spyder(object):
 def __init__(self):
  super(Spyder, self).__init__()
  self._useragents = useragents
  self.last_restarted = None # the last time network manager was restarted

  with open(self._useragents, 'r') as f:
   self.useragents = [_.replace('\n','').replace('\r','') for _ in f if _]

 @property
 def br(self):
  br = Browser()
  br.set_handle_equiv(True)
  br.set_handle_referer(True)
  br.set_handle_robots(False)
  br.set_cookiejar(LWPCookieJar())
  br.addheaders=[('User-agent', self.useragent)]
  br.set_handle_refresh(_http.HTTPRefreshProcessor(), max_time=brwsr_max_refresh)
  return br

 @property
 def useragent(self):
  return choice(self.useragents)

 def restart_net_manager(self):
  shell('service network-manager restart')

 @property
 def ip_addr(self):
  try:
   ip = str(urlopen('https://api.ipify.org/?format=text', timeout=ip_fetch_timeout).text)
   self.last_restarted = None
   return ip
  except:
   if not self.last_restarted:
    self.last_restarted = time()
    self.restart_net_manager()
   else:
    if time() - self.last_restarted >= network_manager_time:
     self.last_restarted = time()
     self.restart_net_manager()
