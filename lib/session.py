# Date: 12/21/2017
# Author: Ethical-H4CK3R
# Description: Sessions

import sqlite3
from constants import database_path
 
class Database(object):

 def __init__(self):
  super(Database, self).__init__()

 def create_table(self):
  database = sqlite3.connect(database_path)
  cursor = database.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS\
   Sessions(ID INTEGER PRIMARY KEY, Site TEXT, Username TEXT, Wordlist TEXT,\
   Locked_time INTEGER DEFAULT 0, Attempts INTEGER DEFAULT 0, Queue TEXT);')
  database.commit()
  database.close()

 def retrieve_ID(self, site, username, wordlist):
  ID = None
  database = sqlite3.connect(database_path)
  ID = database.cursor().execute('''SELECT ID FROM Sessions
                                    WHERE Site = ? AND
                                          Username = ? AND
                                          Wordlist = ?;''', [site, username, wordlist]).fetchone()
  ID = ID[0] if ID else ID
  database.close()
  return ID

 def retrieve_data(self, ID):
  database = sqlite3.connect(database_path)
  cursor = database.cursor()
  data = cursor.execute('SELECT Site, Username, Wordlist, Locked_time, Attempts, Queue FROM Sessions\
   WHERE ID=?;', [ID]).fetchone()
  database.close()
  return [str(_) if _ else _ for _ in data] if data else data

 def display_sessions(self):
  database = sqlite3.connect(database_path)
  for _, data in enumerate(database.cursor().execute('SELECT * FROM Sessions').fetchall()):
   print '\n[ID]: {}\nAttempts: {}\nSession: {}\n'.format(_, data[5], [str(_) for _ in data[1:4]])
  database.close()

 def delete(self, ID):
  database = sqlite3.connect(database_path)
  if self.retrieve_data(ID):
   database.cursor().execute('DELETE FROM Sessions WHERE ID=?;', [ID])
  database.commit()
  database.close()

 def delete_all(self):
  try:
   database = sqlite3.connect(database_path)
   database.cursor().execute('DELETE FROM Sessions;')
   database.commit()
   database.close()
  except:pass

 def get_database(self):
  database = sqlite3.connect(database_path)
  data = database.cursor().execute('SELECT * FROM Sessions').fetchall()
  database.close()
  return data

class Session(object):

 def __init__(self, database_path, ID, site, username, wordlist):
  self.ID = ID
  self.site = site.title()
  self.username = username
  self.wordlist = wordlist
  database_path = database_path

 def database_append(self, *args):
  database = sqlite3.connect(database_path)
  database.cursor().execute('INSERT INTO Sessions(Site, Username, Wordlist)\
   VALUES (?, ?, ?);', [args[0], args[1], args[2]])
  database.commit()
  database.close()
  return Database().retrieve_ID(args[0], args[1], args[2])

 def remove(self):
  if not self.ID:return
  database = sqlite3.connect(database_path)
  database.cursor().execute('DELETE FROM Sessions WHERE ID=?;', [self.ID])
  database.commit()
  database.close()

 def update(self, *args):
  if not self.ID:
   self.ID = self.database_append(self.site, self.username, self.wordlist)

  queue = args[0]
  locked = args[1]
  attempts = args[2]
  database = sqlite3.connect(database_path)
  database.cursor().execute('''UPDATE Sessions
                         SET Site = ?,
                             Queue = ?,
                             Attempts = ?,
                             Username = ?,
                             Wordlist = ?,
                             Locked_time = ?
                         WHERE ID = ?;''', [self.site, queue, attempts, self.username, self.wordlist, locked, self.ID])
  database.commit()
  database.close()
