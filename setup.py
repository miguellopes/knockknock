import sys, os, shutil
from distutils.core import setup

if sys.argv[1] != "sdist":
    shutil.copyfile("knockknock-daemon.py", "knockknock/knockknock-daemon")
    shutil.copyfile("knockknock-genprofile.py", "knockknock/knockknock-genprofile")


setup (name         = 'knockknock',
        version      = '0.8',
        description  = 'A cryptographic single-packet port-knocker.',
        author       = 'Moxie Marlinspike',
        author_email = 'moxie@thoughtcrime.org',
        url          = 'http://www.thoughtcrime.org/software/knockknock/',
        license      = 'GPL',
        install_requires=['crypto'],
        packages     = ['knockknock'],
        scripts      = ['knockknock/knockknock-daemon',
            'knockknock/knockknock-genprofile'],
        data_files   = [('/usr/share/knockknock', ['README', 'INSTALL', 'COPYING']), ('/etc/knockknock.d', ['config']), ('/etc/init.d', ['service/knockknock'])]
        )

print "Cleaning up..."

if os.path.exists("build/"):
    shutil.rmtree("build/")

try:
    os.remove("knockknock/knockknock-daemon")
    os.remove("knockknock/knockknock-genprofile")

except:
    pass

def capture(cmd):
    return os.popen(cmd).read().strip()
