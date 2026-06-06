"""
Sherlock Pro - Platform Scanner Module
"""

import json
import re
from typing import Dict, List, Optional
from pathlib import Path
from bs4 import BeautifulSoup

from core.config import PlatformConfig


class PlatformScanner:
    def __init__(self, config):
        self.config = config
        self.platforms = {}

    def load_platforms(self, filter_platforms: Optional[List[str]] = None) -> Dict:
        """Load and optionally filter platforms"""
        all_platforms = PlatformConfig.load_platforms(self.config.platforms_file)

        if filter_platforms:
            return {
                name: config 
                for name, config in all_platforms.items() 
                if name in filter_platforms
            }

        return all_platforms

    def extract_profile_data(self, html: str, platform: str, config: Dict) -> Optional[Dict]:
        """Extract profile information from HTML"""
        try:
            soup = BeautifulSoup(html, "html.parser")
            data = {"platform": platform}

            # Extract title
            title_tag = soup.find("title")
            if title_tag:
                data["title"] = title_tag.get_text(strip=True)

            # Extract meta description
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                data["description"] = meta_desc.get("content", "")

            # Extract OG image (profile picture)
            og_image = soup.find("meta", property="og:image")
            if og_image:
                data["profile_image"] = og_image.get("content", "")

            # Platform-specific extractions
            extractors = {
                "GitHub": self._extract_github,
                "Twitter/X": self._extract_twitter,
                "Instagram": self._extract_instagram,
                "LinkedIn": self._extract_linkedin,
                "Reddit": self._extract_reddit,
            }

            if platform in extractors:
                platform_data = extractors[platform](soup)
                data.update(platform_data)

            return data

        except Exception:
            return None

    def _extract_github(self, soup: BeautifulSoup) -> Dict:
        data = {}
        # Extract name
        name_tag = soup.find("span", class_="p-name")
        if name_tag:
            data["name"] = name_tag.get_text(strip=True)

        # Extract bio
        bio_tag = soup.find("div", class_="p-note")
        if bio_tag:
            data["bio"] = bio_tag.get_text(strip=True)

        # Extract stats
        stats = soup.find_all("span", class_="text-bold")
        if len(stats) >= 3:
            data["repositories"] = stats[0].get_text(strip=True)
            data["followers"] = stats[1].get_text(strip=True)
            data["following"] = stats[2].get_text(strip=True)

        return data

    def _extract_twitter(self, soup: BeautifulSoup) -> Dict:
        data = {}
        # Extract display name
        name_tag = soup.find("div", attrs={"data-testid": "UserName"})
        if name_tag:
            data["display_name"] = name_tag.get_text(strip=True)

        # Extract bio
        bio_tag = soup.find("div", attrs={"data-testid": "UserDescription"})
        if bio_tag:
            data["bio"] = bio_tag.get_text(strip=True)

        return data

    def _extract_instagram(self, soup: BeautifulSoup) -> Dict:
        data = {}
        # Look for JSON data in script tags
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                json_data = json.loads(script.string)
                if "author" in json_data:
                    data["name"] = json_data["author"].get("name", "")
                if "description" in json_data:
                    data["bio"] = json_data["description"]
            except:
                pass

        return data

    def _extract_linkedin(self, soup: BeautifulSoup) -> Dict:
        data = {}
        # Extract name from title
        title = soup.find("title")
        if title:
            name = title.get_text().replace(" | LinkedIn", "").strip()
            data["name"] = name

        return data

    def _extract_reddit(self, soup: BeautifulSoup) -> Dict:
        data = {}
        # Extract karma
        karma_tags = soup.find_all("span", class_=re.compile("karma"))
        if karma_tags:
            data["karma"] = karma_tags[0].get_text(strip=True)

        return data

    def get_platform_categories(self) -> Dict[str, List[str]]:
        """Group platforms by category"""
        platforms = self.load_platforms()
        categories = {}

        for name, config in platforms.items():
            category = config.get("category", "other")
            if category not in categories:
                categories[category] = []
            categories[category].append(name)

        return categories
