import http.server
import socketserver
import subprocess
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(os.path.dirname(ROOT_DIR), "site")

PORT = 1663
Handler = http.server.SimpleHTTPRequestHandler

subprocess.run([sys.executable, os.path.join(ROOT_DIR, "generate_site_assets.py")])

os.chdir(BASE_DIR)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server started on: http://localhost:{PORT}")
    httpd.serve_forever()