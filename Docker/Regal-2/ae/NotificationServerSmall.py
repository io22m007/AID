#
#	notificationServer.py
#
#	(c) 2020 by Andreas Kraft
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#
#	Simple base implementation of a notification server to handle notifications 
#	from a CSE.
#
#
#   Modified by Mario Kolos, Florian Jeschek and Bernhard Monschiebl 2023-2024
#

from http.server import HTTPServer, BaseHTTPRequestHandler
import json, ssl
import threading
import queue

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
	def __init__(self, *args, data_queue:queue.Queue, **kwargs):
		self.data_queue = data_queue
		super().__init__(*args, **kwargs)

	def do_POST(self) -> None:
		"""	Handle notification.
		"""

		# Get headers and content data
		length = int(self.headers['Content-Length'])
		contentType = self.headers['Content-Type']
		requestID = self.headers['X-M2M-RI']
		post_data = self.rfile.read(length)

		# Print the content data
		print('Received Notification (http)')
		print(self.headers)
		# Construct return header
		# Always acknowledge the verification requests
		self.send_response(200)
		self.send_header('X-M2M-RSC', '2000')
		self.send_header('X-M2M-RI', requestID)
		self.end_headers()

		# HTTP Response
		self.wfile.write(b'') 

		# Print JSON
		if contentType in [ 'application/json', 'application/vnd.onem2m-res+json' ]:
			#Convert the post data into a json dict with utf8 decoding
			notification = json.loads(post_data.decode('utf-8'))
			if "m2m:sgn" in notification and "nev" in notification["m2m:sgn"] and "rep" in notification["m2m:sgn"]["nev"]:
				#Put notification into the queue
				self.data_queue.put(notification)
			print(json.dumps(json.loads(post_data.decode('utf-8')), indent=4))

class NotificationServer(threading.Thread):
	def __init__(self, data_queue:queue.Queue, port:int, certfile:str, keyfile:str):
		super().__init__()
		self.data_queue = data_queue
		self.port = port
		self.certfile = certfile
		self.keyfile = keyfile

	def run(self):
		# run http(s) server
		httpd = HTTPServer(('', self.port), lambda *args, **kwargs: SimpleHTTPRequestHandler(data_queue=self.data_queue, *args, **kwargs))

		# init ssl socket
		# Create a SSL Context
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)			
		# Load the certificate and private key		
		context.load_cert_chain(self.certfile, self.keyfile)		
		# wrap the original http server socket as an SSL/TLS socket		
		httpd.socket = context.wrap_socket(httpd.socket, server_side=True)	
		print('Notification server started.')
		try:
			# run http server
			print(f'Listening for http(s) connections on port {self.port}.')
			httpd.serve_forever()
		except KeyboardInterrupt:
			pass
			# The http server is stopped implicitly
		except Exception:
			print()
		finally:
			print('Notification server stopped.')
