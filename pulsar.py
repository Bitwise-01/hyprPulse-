# Date: 12/15/2017
# Author: Ethical-H4CK3R
# Description: Interactive Bruter

from lib.tor import tor_exists
from lib.console import Console
from lib.session import Database

class Pulsar(Console, Database):

 def run(self):
  self.create_table()
  self.cmdloop()
  self.exit()

if __name__ == '__main__':
 exit('Run: chmod +x install.sh && ./install.sh') if not tor_exists() else Pulsar().run()
