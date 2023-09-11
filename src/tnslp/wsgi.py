
import sys
import logging
from tnslp.app import app as application
 
sys.path.insert(0, '/var/www/The-No-Shoelace-Place')
sys.path.insert(0, '/var/www/The-No-Shoelace-Place/venv/lib/python3.10/site-packages/')
 
# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

if __name__ == '__main__':
   sys.path.insert(0, '/Users/brockbritton15/Documents/GitHub/The-No-Shoelace-Place/src/tnslp')
   application.run()