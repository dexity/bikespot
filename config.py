
# Set your keys
GOOGLE_MAPS_KEY = ""        # Browser api key
GOOGLE_DIRECTIONS_KEY = ""  # Server api key
SQLALCHEMY_DATABASE_URI = ""

try:
    from local_config import *
except ImportError:
    pass