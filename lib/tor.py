# Date: 12/05/2017
# Author: Ethical-H4CK3R
# Description: Tor Controls

from time import sleep
from commands import getoutput as shell

def tor_stop():
 shell('service tor stop')

def tor_restart():
 shell('service tor restart')
 sleep(1.5)

def tor_is_active():
 return not 'dead' in shell('service tor status')

def tor_exists():
 return shell('which tor')
 
