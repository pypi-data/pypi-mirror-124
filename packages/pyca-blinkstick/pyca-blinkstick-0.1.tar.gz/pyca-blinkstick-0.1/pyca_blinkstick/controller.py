from pyca_blinkstick.utils import timestamp, terminate
from pyca_blinkstick.config import config

from blinkstick import blinkstick
import sdnotify
import requests
import time
import usb.core
import logging
import json

logger = logging.getLogger(__name__)
notify = sdnotify.SystemdNotifier()
bstick = blinkstick.find_first()

def process_pyca_status():
	'''Send GET request to services endpoint and process the response to controll the blinkstick
	'''
	host = config('pyca','hostname')
	port = config('pyca', 'port')
	auth = requests.auth.HTTPBasicAuth(config('pyca', 'user'), config('pyca', 'pass'))
	headers = {'content-type': 'application/vnd.api+json'}
	r = requests.get(host + ':' + str(port) + '/api/services', auth=auth, headers=headers)
	if r.status_code != 200:
		#Set to Orange when there is an unexpected status
		bstick.set_color(red=255, green=94, blue=19)
		return
	recording = r.json()["meta"]["services"]["capture"]
	logger.debug("Recording is set to : " + recording)
	if recording == 'busy':
		bstick.set_color(red=255)
	elif recording == 'idle':
		bstick.set_color(green=255)
	else:
		#Set to Orange when there is an unexpected status
		bstick.set_color(red=255, green=94, blue=19)


def control_loop():
	notify.notify('READY=1')
	notify.notify('STATUS=Running')
	while not terminate():
		next_update = timestamp() + config('pyca','update_frequency')
		while not terminate() and timestamp() < next_update:
			time.sleep(0.1)

		if not terminate():
			process_pyca_status()

def run():
	'''Poll the pyca rest api /services endpoint to retrieve the capture state
	'''
	control_loop()
