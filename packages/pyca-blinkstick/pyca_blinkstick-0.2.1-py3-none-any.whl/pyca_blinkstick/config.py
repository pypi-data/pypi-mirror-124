import configobj
import os
import sys
import socket
import logging
import logging.handlers
from validate import Validator

logger = logging.getLogger(__name__)

__CFG = '''
[pyca]
hostname = string(default='http://localhost')
port = integer(default=80)
user = string(default='admin')
pass = string(default='opencast')
update_frequency = integer(default=10)

[logging]
syslog           = boolean(default=False)
stderr           = boolean(default=True)
file             = string(default='')
level            = option('debug', 'info', 'warning', 'error', default='debug')
format           = string(default='[%(name)s:%(lineno)s:%(funcName)s()] [%(levelname)s] %(message)s')
'''

cfgspec = __CFG.split('\n')
__config = None

def configuration_file(cfgfile):
    '''Find the best match for the configuration file.
    '''
    if cfgfile is not None:
        return cfgfile
    # If no file is explicitely specified, probe for the configuration file
    # location.
    cfg = 'config/config.ini'
    if not os.path.isfile(cfg):
        return '/etc/pyca/pyca_blinkstick.conf'
    return cfg

def update_configuration(cfgfile=None):
    '''Update configuration from file.

    :param cfgfile: Configuration file to load.
    '''
    configobj.DEFAULT_INTERPOLATION = 'template'
    cfgfile = configuration_file(cfgfile)
    cfg = configobj.ConfigObj(cfgfile, configspec=cfgspec, encoding='utf-8')
    validator = Validator()
    val = cfg.validate(validator)
    if val is not True:
        raise ValueError('Invalid configuration: %s' % val)

    globals()['__config'] = cfg
    logger_init()
    logger.info('Configuration loaded from %s', cfgfile)
    return cfg

def config(*args):
    '''Get a specific configuration value or the whole configuration, loading
    the configuration file if it was not before.

    :param key: optional configuration key to return
    :type key: string
    :return: Part of the configuration object containing the configuration
             or configuration value.
             If a part of the configuration object (e.g. configobj.Section) is
             returned, it can be treated like a dictionary.
             Returning None, if the configuration value is not found.
    '''
    cfg = __config or update_configuration()
    for key in args:
        if cfg is None:
            return
        cfg = cfg.get(key)
    return cfg

def logger_init():
    '''Initialize logger based on configuration
    '''
    handlers = []
    logconf = config('logging')
    if logconf['syslog']:
        handlers.append(logging.handlers.SysLogHandler(address='/dev/log'))
    if logconf['stderr']:
        handlers.append(logging.StreamHandler(sys.stderr))
    if logconf['file']:
        handlers.append(logging.handlers.WatchedFileHandler(logconf['file']))
    for handler in handlers:
        handler.setFormatter(logging.Formatter(logconf['format']))
        logging.root.addHandler(handler)

    logging.root.setLevel(logconf['level'].upper())
    logger.info('Log level set to %s', logconf['level'])
