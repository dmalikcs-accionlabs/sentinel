#!/home/openerpi/python/bin/python

# setup the virtualenv
import os, sys
os.environ.setdefault('PATH', '/bin:/usr/bin')
os.environ['PATH'] = '/home/openerpi/python/bin:' + os.environ['PATH']
os.environ['VIRTUAL_ENV'] = '/home/openerpi/python/bin'
os.environ['PYTHON_EGG_CACHE'] = '/home/openerpi/python/bin'
os.chdir('/home/openerpi/public_html/deepakmalik.in/deepakmalik')

# Add a custom Python path.
sys.path.insert(0, "/home/openerpi/public_html/deepakmalik.in/deepakmalik")

# Set the DJANGO_SETTINGS_MODULE environment variable  to the file in my
# application directory with the db settings etc.
# (filename minus the extension ".py")
os.environ['DJANGO_SETTINGS_MODULE'] = "deepakmalik.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
