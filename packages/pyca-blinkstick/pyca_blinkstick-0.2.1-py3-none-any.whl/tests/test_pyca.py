
from pyca_blinkstick.controller import process_pyca_status
import responses
import usb.core

from blinkstick import blinkstick

bstick = blinkstick.find_first()

@responses.activate
def test_recording_running():
    json_out = {
			"meta": {
				"services": {
					"agentstate": "idle",
					"capture": "busy",
					"ingest": "idle",
					"schedule": "idle"
				}
			}
		}

    responses.add(responses.GET, 'http://localhost:80/api/services',
    				json=json_out, status=200)

    # Call the service, which will send a request to the server.
    response = process_pyca_status()

    # Since pyca is recording, the blinkstick should be red.
    assert bstick.get_color() == [255, 0, 0]

@responses.activate
def test_recording_idle():
    json_out = {
			"meta": {
				"services": {
					"agentstate": "idle",
					"capture": "idle",
					"ingest": "idle",
					"schedule": "idle"
				}
			}
		}

    responses.add(responses.GET, 'http://localhost:80/api/services',
    				json=json_out, status=200)

    # Call the service, which will send a request to the server.
    response = process_pyca_status()

    # Since pyca is recording, the blinkstick should be red.
    assert bstick.get_color() == [0, 255, 0]

@responses.activate
def test_recording_error():
    json_out = {
			"meta": {
				"services": {
					"agentstate": "idle",
					"capture": "stopped",
					"ingest": "idle",
					"schedule": "idle"
				}
			}
		}

    responses.add(responses.GET, 'http://localhost:80/api/services',
    				json=json_out, status=400)

    # Call the service, which will send a request to the server.
    response = process_pyca_status()

    # Since pyca is recording, the blinkstick should be red.
    assert bstick.get_color() == [255, 94, 19]