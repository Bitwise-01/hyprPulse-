# Date: 12/02/2017
# Author: Ethical-H4CK3R
# Description: Queue

class Queue(object):
 def __init__(self, size=None):
  self.queue = []
  self.size = size

 def get(self):
  return self.queue.pop(0) if self.queue else None

 def put(self, item):
  if not item:return
  if item in self.queue:return
  if self.qsize() == self.size:self.get()
  try:self.queue.append(item.replace('\n','').replace('\r','').split('\\')[0])
  except:self.queue.append(item)

 def qsize(self):
  return len(self.queue)
