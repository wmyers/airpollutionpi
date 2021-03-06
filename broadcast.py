import os
import logging
import logging.handlers
import json
import yaml
import requests

from datetime import datetime


# load config
with open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'), 'r') as f:
    config = yaml.load(f)

# configure logger
formatter = logging.Formatter(config['logging']['format'])
log_level = logging.getLevelName(config['logging']['level'])
if not os.path.exists(config['logging']['path']):
    os.makedirs(config['logging']['path'])

file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(config['logging']['path'], 'broadcast.log'),
    maxBytes=10485760,
    backupCount=100,
    encoding='utf-8')
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(formatter)

logging.root.setLevel(log_level)
logging.root.addHandler(file_handler)
logging.root.addHandler(console_handler)

# get logger
logger = logging.getLogger(__name__)


# get data path
path = config['data']['output']

# get url and auth
url = config['server']['url']
auth = (config['server']['user'], config['server']['password'])

# get all files (exclude .tmp files)
logger.info('Collect files in path %s' % path)
files = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.tmp')]

logger.info('Found %s file(s)' % len(files))
for fname in files:
    delete_file = False
    try:
        last_modified = os.path.getmtime(fname)
        logger.info('Process file %s [%s]' % (fname, datetime.fromtimestamp(last_modified).isoformat()))
        with open(fname, 'r') as f:
            data = f.read()

        logger.info('POST %s: %s' % (url, data))
        response = requests.post(url, data=data, auth=auth, headers={'Content-Type': 'application/octet-stream'}, timeout=2.)
        logger.info('Response: %s' % response.status_code)
        if response.ok:
            delete_file = True
    except json.decoder.JSONDecodeError:
        logger.info('File %s contains invalid json' % fname)
        delete_file = True
    except Exception as ex:
        logger.warning('Exception while trying to POST:', exc_info=True)

    if delete_file:
        logger.info('Delete file %s' % fname)
        os.remove(fname)