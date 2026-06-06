"""
Sherlock Pro - Core Investigation Engine
"""

import asyncio
import aiohttp
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from .config import Config
from scanners.platform_scanner import PlatformScanner
from scanners.email_scanner import EmailScanner
from scanners.phone_scanner import PhoneScanner
from utils.rate_limiter import RateLimiter
from utils.proxy_manager import ProxyManager


@dataclass
class InvestigationResult:
    username: str
    platform: str
    url: str
    exists: bool
    metadata: Dict
    response_time: float
    status_code: int
    screenshot: Optional[str] = None
    profile_data: Optional[Dict] = None


class SherlockEngine:
    def __init__(self, config: Config):
        self.config = config
        self.scanner = PlatformScanner(config)
        self.email_scanner = EmailScanner(config)
        self.phone_scanner = PhoneScanner(config)
        self.rate_limiter = RateLimiter(config.threads)
        self.proxy_manager = ProxyManager(config) if config.proxy or config.use_tor else None
        self.session: Optional[aiohttp.ClientSession] = None

    async def _init_session(self):
        connector = aiohttp.TCPConnector(
            limit=self.config.threads,
            limit_per_host=10,
            enable_cleanup_closed=True,
            force_close=True,
        )

        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )

    async def investigate(
        self, 
        username: str, 
        platforms: Optional[List[str]] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Main investigation method
        """
        await self._init_session()

        start_time = time.time()
        results = {
            "username": username,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_platforms": 0,
            "found_accounts": 0,
            "investigation_time": 0,
            "accounts": [],
            "metadata": {}
        }

        try:
            # Load platform configurations
            platform_configs = self.scanner.load_platforms(platforms)
            results["total_platforms"] = len(platform_configs)

            # Create tasks for all platforms
            tasks = []
            for platform_name, platform_config in platform_configs.items():
                task = self._check_platform(username, platform_name, platform_config)
                tasks.append(task)

            # Execute with progress tracking
            completed = 0
            for coro in asyncio.as_completed(tasks):
                result = await coro
                completed += 1

                if result.exists:
                    results["found_accounts"] += 1
                    results["accounts"].append({
                        "platform": result.platform,
                        "url": result.url,
                        "metadata": result.metadata,
                        "response_time": result.response_time,
                        "profile_data": result.profile_data
                    })

                if progress_callback:
                    progress_callback(completed, len(tasks), result.platform, result.exists)

            # Additional scans
            email_results = await self.email_scanner.scan(username, self.session)
            if email_results:
                results["email_analysis"] = email_results

            # Calculate timing
            results["investigation_time"] = round(time.time() - start_time, 2)

        finally:
            if self.session:
                await self.session.close()

        return results

    async def _check_platform(
        self, 
        username: str, 
        platform_name: str, 
        config: Dict
    ) -> InvestigationResult:
        """
        Check if username exists on a specific platform
        """
        start_time = time.time()

        url = config["url"].format(username=username)
        check_method = config.get("check_method", "status_code")

        try:
            await self.rate_limiter.acquire()

            proxy = None
            if self.proxy_manager:
                proxy = self.proxy_manager.get_proxy()

            async with self.session.get(
                url, 
                proxy=proxy,
                allow_redirects=config.get("follow_redirects", True)
            ) as response:

                response_time = time.time() - start_time
                exists = False
                metadata = {}
                profile_data = None

                if check_method == "status_code":
                    exists = response.status == config.get("success_code", 200)

                    # Try to extract profile data if exists
                    if exists and config.get("extract_profile", False):
                        try:
                            html = await response.text()
                            profile_data = self.scanner.extract_profile_data(
                                html, platform_name, config
                            )
                        except:
                            pass

                elif check_method == "response_text":
                    text = await response.text()
                    error_text = config.get("error_text", "")
                    exists = error_text not in text

                elif check_method == "response_url":
                    final_url = str(response.url)
                    exists = config.get("success_url_pattern") in final_url

                return InvestigationResult(
                    username=username,
                    platform=platform_name,
                    url=url,
                    exists=exists,
                    metadata=metadata,
                    response_time=response_time,
                    status_code=response.status,
                    profile_data=profile_data
                )

        except asyncio.TimeoutError:
            return InvestigationResult(
                username=username,
                platform=platform_name,
                url=url,
                exists=False,
                metadata={"error": "timeout"},
                response_time=time.time() - start_time,
                status_code=0
            )
        except Exception as e:
            return InvestigationResult(
                username=username,
                platform=platform_name,
                url=url,
                exists=False,
                metadata={"error": str(e)},
                response_time=time.time() - start_time,
                status_code=0
            )
