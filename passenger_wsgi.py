import os
import sys

# Add project directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# If your Django project is inside a subfolder, adjust this path
project_home = os.path.dirname(__file__)
if project_home not in sys.path:
    sys.path.append(project_home)

# Set the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectapp.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
