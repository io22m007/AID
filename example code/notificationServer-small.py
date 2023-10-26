#
#	notificationServer.py
#
#	(c) 2020 by Andreas Kraft
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#
#	Simple base implementation of a notification server to handle notifications 
#	from a CSE.
#

from http.server import HTTPServer, BaseHTTPRequestHandler
import json, ssl

##############################################################################
#
#	HTTP Server
#

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
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
			print(json.dumps(json.loads(post_data.decode('utf-8')), indent=4))

		# Print other binary content
		else:
			print("not json:")
			print(post_data, highlight=False)

	def log_message(self, format:str, *args:int) -> None:
		if (msg := format%args).startswith(('"GET', '"POST')):	return	# ignore GET log messages
		print(msg, highlight = False)

#
#	Entry
#
print("Notification Server Small")

port = 9999	# Change this variable to specify another port.
# run http(s) server
httpd = HTTPServer(('', port), SimpleHTTPRequestHandler)

# init ssl socket
#context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)					# Create a SSL Context
#context.load_cert_chain(certfile, keyfile)				# Load the certificate and private key
#httpd.socket = context.wrap_socket(httpd.socket, server_side=True)	# wrap the original http server socket as an SSL/TLS socket

print('Notification server started.')
try:
	# run http server
	print(f'Listening for http(s) connections on port {port}.')
	httpd.serve_forever()
except KeyboardInterrupt as e:
	pass
	# The http server is stopped implicitly
except Exception:
	print()
finally:
	print('Notification server stopped.')