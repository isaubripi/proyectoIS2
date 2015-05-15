# -.- coding: utf-8 -.-
import os, sys
from sistemask import settingsPRODUCCION
 
path = settingsPRODUCCION.PATH
if path not in sys.path:
    sys.path.append(path)
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistemask.settingsPRODUCCION")
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
