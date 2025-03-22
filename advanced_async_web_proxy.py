#!/usr/bin/env python3
import asyncio
import logging
import time
import random
from config import PROXY_HOST, PROXY_PORT, TARGETS, CACHE_TTL

# Configure detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# In-memory cache (key -> (response, expiry_time))
cache = {}

def get_cache(key):
    """Retrieve cached responses if TTL has not expired."""
    entry = cache.get(key)
    if entry and entry[1] > time.time():
        return entry[0]
    elif entry:
        del cache[key]
    return None

def set_cache(key, response):
    """Set cached response with a TTL."""
    cache[key] = (response, time.time() + CACHE_TTL)

async def recvall(reader, buffer_size=8192):
    """Receive complete response from target server."""
    data = b""
    while True:
        part = await reader.read(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    return data

async def handle_proxy(reader, writer):
    try:
        # Receive client's HTTP request
        request = await reader.read(8192)
        key = hash(request)
        cached_response = get_cache(key)

        if cached_response:
            logging.info("Cache hit. Serving cached response.")
            response = cached_response
        else:
            # Select a random target server for load balancing
            target_host, target_port = random.choice(TARGETS)
            remote_reader, remote_writer = await asyncio.open_connection(target_host, target_port)
            remote_writer.write(request)
            await remote_writer.drain()

            # Retrieve and cache the response
            response = await recvall(remote_reader)
            set_cache(key, response)

            # Close remote connection
            remote_writer.close()
            await remote_writer.wait_closed()

        # Forward response back to client
        writer.write(response)
        await writer.drain()
    except Exception as e:
        logging.error("Error in handle_proxy: %s", e)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_proxy, PROXY_HOST, PROXY_PORT)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logging.info("Advanced Async Web Proxy running on %s", addrs)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
