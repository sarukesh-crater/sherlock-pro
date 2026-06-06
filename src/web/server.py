
"""
Sherlock Pro - Web UI Server
Lightweight server for local web interface
"""

import asyncio
import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser


class SherlockHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.web_dir = Path(__file__).parent.parent / "web"
        super().__init__(*args, directory=str(self.web_dir), **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def log_message(self, format, *args):
        pass


async def start_server(port=8080):
    """Start the web UI server"""
    from ui.banner import Banner
    banner = Banner()
    banner.print_status("Starting Web UI Server...", "info")

    server = HTTPServer(("localhost", port), SherlockHandler)

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    url = f"http://localhost:{port}"
    banner.print_status(f"Web UI running at {url}", "success")

    # Open browser
    webbrowser.open(url)

    print("\nPress Ctrl+C to stop the server")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
        banner.print_status("Server stopped", "info")
