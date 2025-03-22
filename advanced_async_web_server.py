#!/usr/bin/env python3
import asyncio
import ssl
import logging
from config import SERVER_HOST, SERVER_PORT, CERT_FILE, KEY_FILE

# Configure detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def handle_client(reader, writer):
    try:
        # Receive incoming request
        request = await reader.read(8192)
        request_str = request.decode('utf-8', errors='ignore')
        logging.info("Server received: %s", request_str.splitlines()[0])

        # Create a basic HTTPS response
        body = "<html><body><h1>Secure Async Web Server</h1><p>Welcome to the HTTPS-enabled server!</p></body></html>"
        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Connection: close\r\n\r\n"
            f"{body}"
        )
        writer.write(response.encode('utf-8'))
        await writer.drain()
    except Exception as e:
        logging.error("Error in handle_client: %s", e)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    # Set up TLS/HTTPS
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    # Start the asynchronous HTTPS server
    server = await asyncio.start_server(handle_client, SERVER_HOST, SERVER_PORT, ssl=ssl_context)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logging.info("Secure Async Web Server running on %s", addrs)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
