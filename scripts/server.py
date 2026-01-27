#!/usr/bin/env python3
"""
Start local development server for murder mystery game
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Get project root (parent of scripts directory)
script_dir = Path(__file__).parent
project_root = script_dir.parent

# Change to project root
os.chdir(project_root)

PORT = 8005

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 60)
        print("🔍 Murder Mystery Game - Local Server")
        print("=" * 60)
        print(f"📡 Server running at: http://localhost:{PORT}/")
        print(f"📁 Serving from: {project_root}")
        print("=" * 60)
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        httpd.serve_forever()
except OSError as e:
    if "Address already in use" in str(e):
        print(f"❌ Error: Port {PORT} is already in use")
        print(f"   Try a different port or stop the process using port {PORT}")
        sys.exit(1)
    else:
        raise
except KeyboardInterrupt:
    print("\n\n🛑 Server stopped")
    sys.exit(0)
