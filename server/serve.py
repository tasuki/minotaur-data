from .predictor import predict

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

class S(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def _set_headers(self, content_length):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', content_length)
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)
        game = url.query.replace("game=", "")

        encoded = json.dumps(predict(game))
        content = (encoded + "\n").encode('utf-8')

        self._set_headers(len(content))
        self.wfile.write(content)


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()
