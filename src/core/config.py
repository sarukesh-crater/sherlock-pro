"""
Sherlock Pro - Configuration Management
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
import json
from pathlib import Path


@dataclass
class Config:
    timeout: int = 30
    threads: int = 50
    proxy: Optional[str] = None
    use_tor: bool = False
    verbose: bool = False
    no_color: bool = False
    output_format: str = "table"
    platforms_file: str = "data/platforms.json"
    max_retries: int = 3
    retry_delay: float = 1.0
    follow_redirects: bool = True
    extract_profiles: bool = True
    face_analysis: bool = False

    def __post_init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.platforms_file = self.data_dir / "platforms.json"


class PlatformConfig:
    """Manages platform detection configurations"""

    @staticmethod
    def load_platforms(file_path: Optional[str] = None) -> Dict:
        """Load platform configurations from JSON"""
        if file_path is None:
            file_path = Path(__file__).parent.parent.parent / "data" / "platforms.json"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default platforms if file not found
            return PlatformConfig.get_default_platforms()

    @staticmethod
    def get_default_platforms() -> Dict:
        """Default platform configurations"""
        return {
            "Twitter/X": {
                "url": "https://x.com/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "social",
                "icon": "🐦"
            },
            "Instagram": {
                "url": "https://www.instagram.com/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "social",
                "icon": "📸"
            },
            "GitHub": {
                "url": "https://github.com/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "development",
                "icon": "💻"
            },
            "Reddit": {
                "url": "https://www.reddit.com/user/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "social",
                "icon": "🔴"
            },
            "LinkedIn": {
                "url": "https://www.linkedin.com/in/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "professional",
                "icon": "💼"
            },
            "YouTube": {
                "url": "https://www.youtube.com/@{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "video",
                "icon": "▶️"
            },
            "TikTok": {
                "url": "https://www.tiktok.com/@{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "social",
                "icon": "🎵"
            },
            "Facebook": {
                "url": "https://www.facebook.com/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "social",
                "icon": "📘"
            },
            "Pinterest": {
                "url": "https://www.pinterest.com/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "social",
                "icon": "📌"
            },
            "Twitch": {
                "url": "https://www.twitch.tv/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "streaming",
                "icon": "🎮"
            },
            "Spotify": {
                "url": "https://open.spotify.com/user/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "music",
                "icon": "🎧"
            },
            "Medium": {
                "url": "https://medium.com/@{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "blogging",
                "icon": "✍️"
            },
            "Dev.to": {
                "url": "https://dev.to/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "development",
                "icon": "📝"
            },
            "StackOverflow": {
                "url": "https://stackoverflow.com/users/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "development",
                "icon": "❓"
            },
            "GitLab": {
                "url": "https://gitlab.com/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "development",
                "icon": "🦊"
            },
            "Bitbucket": {
                "url": "https://bitbucket.org/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "development",
                "icon": "🪣"
            },
            "Discord": {
                "url": "https://discord.com/users/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "social",
                "icon": "💬"
            },
            "Telegram": {
                "url": "https://t.me/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "messaging",
                "icon": "✈️"
            },
            "Snapchat": {
                "url": "https://www.snapchat.com/add/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "social",
                "icon": "👻"
            },
            "WhatsApp": {
                "url": "https://wa.me/{username}",
                "check_method": "status_code",
                "success_code": 200,
                "category": "messaging",
                "icon": "💚"
            }
        }
