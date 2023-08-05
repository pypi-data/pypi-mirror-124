from datetime import datetime
from dateutil.tz import tzutc

import os
import time

def timestamp():
    '''Get current unix timestamp
    '''
    return int(datetime.now(tzutc()).timestamp())

def terminate(shutdown=None):
    '''Mark process as to be terminated.
    '''
    global _terminate
    if shutdown is not None:
        _terminate = shutdown
    return '_terminate' in globals() and _terminate