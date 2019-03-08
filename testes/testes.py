#!/usr/bin/env python

import unittest, os, subprocess
from signal import SIGTERM
#1 verificar e apagar pidfile
#2 iniciar servico
#3 verificar pidfile e processo
#4 enviar sigterm para o processo e verificar pidfile
pidfile='/var/run/knock.pid'
daemon= '/usr/local/bin/knockknock-daemon'
class daemonTestCase(unittest.TestCase):
   def checkpid(self):
      try:
         pf = file(pidfile,'r')
         pid = int(pf.read().strip())
         pf.close()
      except IOError:
         pid = None

      if pid:
         os.kill(pid, SIGTERM)
         os.remove(pidfile)
      print "r"
   def init(self):
      process = subprocess.Popen(daemon ,shell=False)
      sleep(2)
      try:
         pf = file(pidfile,'r')
         pid = int(pf.read().strip())
         pf.close()
      except IOError:
         pid = None


