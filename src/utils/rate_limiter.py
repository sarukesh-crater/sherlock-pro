
"""
Sherlock Pro - Rate Limiter
"""

import asyncio
from typing import Optional


class RateLimiter:
    def __init__(self, max_concurrent: int = 50):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.delay = 0.1

    async def acquire(self):
        await self.semaphore.acquire()
        await asyncio.sleep(self.delay)

    def release(self):
        self.semaphore.release()

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()
