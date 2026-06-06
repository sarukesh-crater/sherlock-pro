
"""
Sherlock Pro - Proxy Manager
"""

from typing import Optional


class ProxyManager:
    def __init__(self, config):
        self.config = config
        self.proxy_pool = []
        self.current_index = 0

        if config.proxy:
            self.proxy_pool.append(config.proxy)

        if config.use_tor:
            self.proxy_pool.append("socks5://127.0.0.1:9050")

    def get_proxy(self) -> Optional[str]:
        if not self.proxy_pool:
            return None

        proxy = self.proxy_pool[self.current_index % len(self.proxy_pool)]
        self.current_index += 1
        return proxy

    def add_proxy(self, proxy: str):
        self.proxy_pool.append(proxy)
