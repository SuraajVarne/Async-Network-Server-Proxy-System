# config.py
# Configuration settings for the Advanced Async TCP Web Server & Proxy System

# Web Server configuration (with TLS/HTTPS)
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8443
CERT_FILE = "server.crt"  # Path to TLS certificate
KEY_FILE = "server.key"   # Path to TLS private key

# Web Proxy configuration
PROXY_HOST = "0.0.0.0"
PROXY_PORT = 8888
# List of target servers (host, port) for proxy forwarding (supports basic load balancing)
TARGETS = [("www.example.com", 80), ("www.another-server.com", 80)]

# Cache configuration for proxy responses (in seconds)
CACHE_TTL = 15
