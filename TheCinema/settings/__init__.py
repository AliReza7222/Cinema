from .base import *

if not DEBUG:
    from .production import *
