import os
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Default to Vercel's provided port if available
PORT = int(os.getenv("PORT", 3000))

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            cmd = [
                "streamlit",
                "run",
                "alwrity.py",
                "--server.port",
                str(PORT),
                "--server.address",
                "0.0.0.0",
            ]
            subprocess.Popen(cmd)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Streamlit app launching...')
        else:
            self.send_error(404, 'Not Found')


if __name__ == '__main__':
    HTTPServer(('', PORT), Handler).serve_forever()
