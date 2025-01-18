import sys

# Add your project directory to the sys.path for pythonanywhere.com
project_home = '/home/songlet/chinese-name-generator'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the application
from app import application
