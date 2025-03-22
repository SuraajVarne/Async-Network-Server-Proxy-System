# Advanced Async TCP Web Server & Proxy System

## Overview
This project implements an advanced TCP-based web server and proxy using Python's asyncio framework, featuring secure TLS/HTTPS, load-balanced proxying, and in-memory caching. The system ensures secure communication, optimized response times, and minimal data redundancy.

## Key Features
- **Asynchronous Web Server with TLS/HTTPS:**  
  Serves HTTP requests securely over TLS using `asyncio` for efficient non-blocking I/O.
- **Advanced Web Proxy with Load Balancing & Caching:**  
  Implements load-balanced HTTP request forwarding with in-memory caching to reduce redundant responses.
- **Detailed Logging & Error Handling:**  
  Logs request details and errors to provide actionable runtime insights.

## Files
- **advanced_async_web_server.py:** Asynchronous TLS/HTTPS web server.
- **advanced_async_web_proxy.py:** Multi-threaded web proxy with caching.
- **config.py:** Configuration settings for the server and proxy.
- **README.md:** Project documentation.
- **requirements.txt:** List of optional Python packages.

## Setup & Execution
1. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
```

2. **Run the web server**:
