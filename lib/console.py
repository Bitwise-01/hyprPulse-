# Date: 12/15/2017
# Author: Ethical-H4CK3R
# Description: Interactive Console

from cmd2 import Cmd
from time import sleep
from queue import Queue
from tor import tor_stop
from os.path import exists
from getpass import getuser
from subprocess import call
from session import Session
from bruter import Bruteforce
from regulator import Regulate
from constants import sites, database_path, colors

class Console(Cmd, object):

 def __init__(self):
  super(Console, self).__init__()
  self.session_history = [] # prevent duplicates of sessions

  self.debug = True
  self.ruler = '-'
  self.default_to_shell = True
  self.doc_header = '\n{0}Possible Commands {2}({2}type {1}help <{2}command{1}>{2})'.\
  format(colors['blue'], colors['yellow'], colors['white'])
  self.intro = '\n\ttype {}help{} for help\n'.\
  format(colors['yellow'], colors['white'])

  call('clear')
  self._sessions = Queue() # holds attack sessions
  self.prompt = '{}{}{}>{} '.\
  format(colors['red'], getuser(), colors['blue'], colors['white'])

 def _help_menu(self):
  """"Show a list of commands which help can be displayed for.
  """
  ignore = ['shell', '_relative_load', 'cmdenvironment', 'help', 'history', 'load',
            'edit', 'py', 'pyscript', 'set', 'show', 'save', 'shortcuts', 'run']

  # get a list of all method names
  names = self.get_names()

  # remove any command names which are explicitly excluded from the help menu
  for name in self.exclude_from_help:
   names.remove(name)

  cmds_doc = []
  help_dict = {}
  for name in names:
   if name[:5] == 'help_':
    help_dict[name[5:]] = 1

  names.sort()
  prevname = ''

  for name in names:
   if name[:3] == 'do_':
    if name == prevname:
     continue

    prevname = name
    command = name[3:]

    if command in ignore:
     continue

    if command in help_dict:
     cmds_doc.append(command)
     del help_dict[command]
    elif getattr(self, name).__doc__:
     cmds_doc.append(command)
    else:pass

  self.print_topics(self.doc_header, cmds_doc, 15, 80)

 def print_topics(self, header, cmds, cmdlen, maxcol):
  if cmds:
   self.stdout.write("%s\n"%str(header))
   if self.ruler:
    self.stdout.write("+%s+\n"%str(self.ruler * (len(header)-8)))
   self.columnize(cmds, maxcol-1)
   self.stdout.write("\n")

 def do_supported(self, args):
  '''\n\tDescription: Check if one site or more are supported or display supported sites
    \tUsage: supported <site>\n\tUsage: supported\n'''

  if not args:
   for _, site in enumerate(sites):
    if not _:print
    print '\t{}'.format(site.title())
   else:print
  else:
   for site in args.split():
    site = site.lower()
    output = '\n\t{}: Supported'.format(site.title()) if site in sites\
    else '\n\t{}: Not Supported'.format(site.title())
    print output
   else:print

 def exit(self):
  for session in self._sessions.queue:session.stop()
  tor_stop()
  print

 def check_args(self, args, num):
  args = args.split()
  if len(args) != num:
   print '\n\t[-] Error: This Function takes {} arguments ({} given)\n'.\
   format(num, len(args))
   return

  index = args[0]
  new_data = args[1]

  if not index.isdigit():
   print '\n\tError: `{}` is not a number\n'.format(index)
   return

  index = int(index)
  if any([index >= len(self._sessions.queue), index < 0]):
   print '\n\tError: `{}` is not in the queue\n'.format(index)
   return
  return index, new_data

 def do_change_username(self, args):
  '''\n\tDescription: Change the username of a session that's within the queue
    \tUsage: change_username <id> <new_username>\n'''
  args = self.check_args(args, 2)
  if not args:return
  obj = self._sessions.queue[args[0]].obj
  del self.session_history[self.session_history.index('{} {} {}'.\
  format(obj.site['name'].lower(), obj.username, obj.wordlist))]
  obj.username = args[1].title()
  self.session_history.append('{} {} {}'.\
  format(obj.site['name'].lower(), obj.username, obj.wordlist))
  obj.session.username = obj.username

 def do_change_wordlist(self, args):
  '''\n\tDescription: Change the wordlist of a session that's within the queue & restart it
    \tUsage: change_wordlist <id> <new_wordlist>\n'''
  args = self.check_args(args, 2)
  if not args:return
  if not exists(args[1]):
   print '\n\tError: `{}` doesn\'t exists\n'
   return

  obj = self._sessions.queue[args[0]].obj
  restart = False if not obj.is_alive else True
  del self.session_history[self.session_history.index('{} {} {}'.\
  format(obj.site['name'].lower(), obj.username, obj.wordlist))]
  obj.wordlist = args[1]

  self.session_history.append('{} {} {}'.\
  format(obj.site['name'].lower(), obj.username, obj.wordlist))
  self._sessions.queue[args[0]].reset()
  obj.session.wordlist = obj.wordlist
  if restart:self.do_start(str(args[0]))

 def do_change_site(self, args):
  '''\n\tDescription: Change the site of a session that's within the queue
    \tUsage: change_site <id> <new_site>\n'''
  args = self.check_args(args, 2)
  if not args:return

  if not args[1].lower() in sites:
   print '\n\t[-] Error: `{}` is not supported. Only {} are supported\n'.\
   format(args[1].lower(), ', '.join([_.title() for _ in sites]))
   return

  obj = self._sessions.queue[args[0]].obj
  del self.session_history[self.session_history.index('{} {} {}'.\
  format(obj.site['name'].lower(), obj.username, obj.wordlist))]
  obj.site = sites[args[1].lower()]
  
  obj.session.site = obj.site
  self.session_history.append('{} {} {}'.\
  format(obj.site['name'].lower(), obj.username, obj.wordlist))

 def do_database(self, args):
  '''\n\tDescription: Display all saved sessions within the database
    \tUsage: database\n'''
  self.display_sessions()

 def do_monitor(self, index):
  '''\n\tDescription: Monitor a session
    \tUsage: monitor <id>\n'''
  if not index.isdigit():return
  index = int(index)

  if any([index >= len(self._sessions.queue), index < 0]):return
  session = self._sessions.queue[index]
  while session.obj.is_alive:
   try:
    call('clear')
    print session.info
    sleep(0.45 if session.obj.locked else 2) # for a smooth countdown display
   except KeyboardInterrupt:break

 def do_start(self, args):
  '''\n\tDescription: Start one session or more within the queue
    \tUsage: start <id>\n'''

  for index in args:
   if not index.isdigit():continue
   index = int(index)

   if any([index >= len(self._sessions.queue), index < 0]):continue
   print '\n\tStarting: {} ...\n'.format(index)
   self._sessions.queue[index].start()
   sleep(0.5)

 def do_restart(self, args):
  '''\n\tDescription: Restart one session or more within the queue
    \tUsage: restart <id>\n'''

  for index in args:
   if not index.isdigit():continue
   index = int(index)

   if any([index >= len(self._sessions.queue), index < 0]):continue
   self._sessions.queue[index].reset()
   self.do_start(str(index))

 def do_stop(self, args):
  '''\n\tDescription: Stop one session or more within the queue
    \tUsage: stop <id>\n'''

  for index in args:
   if not index.isdigit():continue
   index = int(index)

   if any([index >= len(self._sessions.queue), index < 0]):continue
   print '\n\tStopping: {} ...\n'.format(index)
   self._sessions.queue[index].stop()
   sleep(0.5)

 def do_delete(self, args):
  '''\n\tDescription: Remove one session or more from the queue
    \tUsage: remove <id>\n '''

  for index in args:
   if not index.isdigit():continue
   index = int(index)

   if any([index >= len(self._sessions.queue), index < 0]):continue
   obj = self._sessions.queue[index].obj

   del self.session_history[self.session_history.index('{} {} {}'.\
   format(obj.site['name'].lower(), obj.username, obj.wordlist))]
   self._sessions.queue[index].stop()
   self._sessions.queue.pop(index)

 def do_remove(self, args):
  '''\n\tDescription: Remove one session or more from the database
    \tUsage: remove <id>\n '''

  for index in args:
   if not index.isdigit():continue
   index = int(index)

   if any([index >= len(self._sessions.queue), index < 0]):continue
   obj = self._sessions.queue[index].obj

   del self.session_history[self.session_history.index('{} {} {}'.\
   format(obj.site['name'].lower(), obj.username, obj.wordlist))]
   session = self._sessions.queue.pop(index)
   session.remove()
   sleep(0.1)

 def do_reset(self, args):
  '''\n\tDescription: Reset database, by deleting all saved sessions
    \tUsage: reset\n'''
  try:
   if raw_input('\n\tAre you sure you want remove EVERY session? [Y/n] ').lower() == 'y':
    self.delete_all()
    for session in self._sessions.queue:
     self._sessions.get()
     session.remove()
   print
  except:return

 def do_quit(self, args):
  '''\n\tDescription: Terminate the program
    \tUsage: quit\n'''
  self._should_quit = True
  return self._STOP_AND_EXIT

 def do_queue(self, args):
  '''\n\tDescription: Display the sessions within the queue
    \tUsage: queue\n'''
  for _, session in enumerate(self._sessions.queue):
   ID = '\n{0}[{1}ID{0}]{1}: {2}'.format(colors['yellow'], colors['white'], _)
   acv = '\nActive: {}{}{}'.format(colors['red'] if not session.obj.is_alive\
   else colors['blue'], session.obj.is_alive, colors['white'])

   locked = '\nLocked: {}{}{}'.format(colors['red'] if session.obj.locked\
   else colors['blue'], True if session.obj.locked else False, colors['white'])

   attempts = '\nAttempts: {}{}{}'.format(colors['yellow'],
   session.obj.attempts, colors['white'])

   msg = session.obj.msg if session.obj.msg else ''

   print '{}{}{}{}{}\nSession: {}\n'.\
   format(ID, acv, locked, attempts, msg, [_ for _ in session.simple_info])

 def do_create(self, args):
  '''\n\tDescription: Create a new session & append it into the queue
    \tUsage: create <site> <username> <wordlist>\n'''
  if not args:return
  args = args.split()

  if len(args) != 3:
   print '\n\t[-] Error: This Function takes 3 arguments ({} given)\n'.format(len(args))
   return

  site = args[0].lower()
  username = args[1].title()
  wordlist = args[2]

  if not site in sites:
   print '\n\t[-] Error: `{}` is not supported. Only {} are supported\n'.\
   format(site, ', '.join([_.title() for _ in sites]))
   return

  if not exists(wordlist):
   print '\n\t[-] Error: Unable to locate `{}`\n'.format(wordlist)
   return

  bruter = Bruteforce(site, username, wordlist)
  ID = self.retrieve_ID(site.title(), username, wordlist)
  if '{} {} {}'.format(site, username, wordlist) in self.session_history:return
  else:self.session_history.append('{} {} {}'.format(site, username, wordlist))

  if ID:
   try:
    if raw_input('\n\tDo you want to use saved data? [Y/n] ').lower() == 'y':
     data = self.retrieve_data(ID)
     if data[-1]:
      bruter.passlist.queue = eval(data[-1])
     if data[-2]:
      bruter.retrieve = True
      bruter.attempts = eval(data[-2])
     if data[-3]:
      bruter.locked = eval(data[-3])
    else:
     self.delete(ID)
     ID = 0
   except:return

  bruter.session = Session(database_path, ID, site, username, wordlist)
  self._sessions.put(Regulate(bruter))
  if ID:print

 def do_recreate(self, args):
  '''\n\tDescription: Recreate one session or more from the database
    \tUsage: recreate <id>\n'''

  database = {}
  for num, session in enumerate(self.get_database()):
   database[num] = session

  for index in args:
   if not index.isdigit():continue
   if not int(index) in database:continue

   session = database[int(index)]
   ID = int(session[0])

   site = str(session[1]).lower()
   username = str(session[2])
   wordlist = str(session[3])

   locked = session[4]
   attempts = session[5]
   passlist = eval(session[6]) if session[6] else []

   if '{} {} {}'.format(site, username, wordlist) in self.session_history:return
   else:self.session_history.append('{} {} {}'.format(site, username, wordlist))
   bruter = Bruteforce(site, username, wordlist)
   bruter.retrieve = True

   bruter.username = username
   bruter.wordlist = wordlist

   bruter.locked = locked
   bruter.attempts = attempts
   bruter.passlist.queue = passlist

   bruter.session = Session(database_path, ID, site, username, wordlist)
   self._sessions.put(Regulate(bruter))

   print '\n\tRecreating {} ...\n'.format(index)
   sleep(1)
