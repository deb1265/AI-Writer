import os
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = int(os.getenv('PORT', 8000))

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            subprocess.Popen(['streamlit', 'run', 'alwrity.py', '--server.port', str(PORT)])
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Streamlit app launching...')
        else:
            self.send_error(404, 'Not Found')


if __name__ == '__main__':
    HTTPServer(('', PORT), Handler).serve_forever()
