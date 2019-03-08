import sys, os, time, grp, pwd
import signal

redirect = "/dev/null"
piddir = "/var/run/knockknock/"
pidfile =piddir+"knock.pid"

if (hasattr(os, "devnull")):
   REDIRECT_TO = os.devnull
else:
   REDIRECT_TO = "/dev/null"

def createDaemon():
   try:
      pid = os.fork()
      if pid > 0:
      # exit first parent
         sys.exit(0)
   except OSError, e:
      sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
      sys.exit(1)

# decouple from parent environment
   os.chdir("/")
   os.setsid()
   os.umask(0)

# do second fork
   try:
      pid = os.fork()
      if pid > 0:
          # exit from second parent
           sys.exit(0)
   except OSError, e:
      sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
      sys.exit(1)

# redirect standard file descriptors
   os.open(REDIRECT_TO, os.O_RDWR)	# standard input (0)
   os.dup2(0, 1)			# standard output (1)
   os.dup2(0, 2)			# standard error (2)
   write_pid()
   signal.signal(signal.SIGTERM,delpid)

# write pidfile
def write_pid():
   if not os.path.exists(piddir):
      os.makedirs(piddir)
   pid = str(os.getpid())
   file(pidfile,'w+').write("%s\n" % pid)
#change permissions on folder and pidfile.needed to delete pidfile withou root
   uid = pwd.getpwnam("root").pw_uid
   gid = grp.getgrnam("adm").gr_gid
   os.chown(pidfile, uid, gid)
   os.chown(piddir, uid, gid)
   os.chmod(pidfile,0664)
   os.chmod(piddir,0770)

def delpid(signal, frame):
   try:
      if os.path.exists(pidfile):
         os.remove(pidfile)
   except IOError:
     sys.stderr.write("Erro ao apagar o pidfile")
   os._exit(1)

def start():
# Check for a pidfile to see if the daemon already runs
   try:
      pf = file(pidfile,'r')
      pid = int(pf.read().strip())
      pf.close()
   except IOError:
      pid = None

   if pid:
      message = "pidfile %s already exist. Daemon already running?\n"
      sys.stderr.write(message % pidfile)
      sys.exit(1)

# Start the daemon
   createDaemon()

