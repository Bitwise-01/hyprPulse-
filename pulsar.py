# Date: 12/15/2017
# Author: Ethical-H4CK3R
# Description: Interactive Bruter

from sys import exit
from lib.tor import tor_exists
from lib.console import Console
from lib.session import Database

class Pulsar(Console, Database):

 def console(self):
  self.create_table()
  self.cmdloop()
  self.exit()

if __name__ == '__main__':
 if not tor_exists():
  exit('Tor is not installed. Run: sudo python install.py')
 else:
  Pulsar().console()
