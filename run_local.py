#!/usr/bin/env python3
"""
Simple local web server for testing Eternal web app.
Run this to test the web app locally before deploying to GitHub Pages.
"""

import http.server
import socketserver
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve from root directory"""
    
    def end_headers(self):
        # Add CORS headers for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Change to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    Handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("=" * 60)
            print("🧠 Eternal AI News Aggregator - Local Server")
            print("=" * 60)
            print(f"\n✅ Server running at: http://localhost:{PORT}/")
            print(f"✅ Web app: http://localhost:{PORT}/webapp/")
            print(f"✅ Or visit: http://localhost:{PORT}/ (auto-redirects)")
            print("\n📝 Note: You need to run the collector first to generate data:")
            print("   python collector/generate_news.py")
            print("\n⏹️  Press Ctrl+C to stop the server\n")
            print("=" * 60)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        sys.exit(0)
    except OSError as e:
        if e.errno == 98 or e.errno == 10048:  # Address already in use
            print(f"\n❌ Error: Port {PORT} is already in use.")
            print(f"   Try closing other applications or use a different port.")
            sys.exit(1)
        else:
            raise

if __name__ == "__main__":
    main()
