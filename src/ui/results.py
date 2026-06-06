
"""
Sherlock Pro - Results Display & Formatting
"""

import json
import csv
from typing import Dict, List
from datetime import datetime


class ResultsDisplay:
    def __init__(self, no_color: bool = False):
        self.no_color = no_color
        self.colors = {
            "green": "\033[92m",
            "red": "\033[91m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "cyan": "\033[96m",
            "magenta": "\033[95m",
            "bold": "\033[1m",
            "reset": "\033[0m"
        }

    def _color(self, text: str, color: str) -> str:
        if self.no_color:
            return text
        return f"{self.colors.get(color, '')}{text}{self.colors['reset']}"

    def show(self, results: Dict, format: str = "table"):
        if format == "json":
            print(json.dumps(results, indent=2, default=str))
        elif format == "csv":
            self._show_csv(results)
        elif format == "html":
            self._show_html(results)
        else:
            self._show_table(results)

    def _show_table(self, results: Dict):
        print(f"\n{self._color('═' * 70, 'blue')}")
        print(f"{self._color('📊 INVESTIGATION RESULTS', 'bold')}")
        print(f"{self._color('═' * 70, 'blue')}\n")

        # Summary
        print(f"  {self._color('Target Username:', 'cyan')} {self._color(results['username'], 'yellow')}")
        print(f"  {self._color('Timestamp:', 'cyan')} {results['timestamp']}")
        print(f"  {self._color('Platforms Scanned:', 'cyan')} {results['total_platforms']}")
        print(f"  {self._color('Accounts Found:', 'cyan')} {self._color(str(results['found_accounts']), 'green')}")
        print(f"  {self._color('Investigation Time:', 'cyan')} {results['investigation_time']}s")
        print()

        if results["found_accounts"] == 0:
            print(f"  {self._color('⚠️  No accounts found for this username.', 'yellow')}")
            print(f"  {self._color('   Try variations or check if the username is correct.', 'yellow')}")
            return

        # Accounts table
        print(f"  {self._color('┌' + '─' * 66 + '┐', 'blue')}")
        print(f"  {self._color('│', 'blue')} {self._color('PLATFORM', 'bold'):<20} {self._color('│', 'blue')} {self._color('URL', 'bold'):<43} {self._color('│', 'blue')}")
        print(f"  {self._color('├' + '─' * 66 + '┤', 'blue')}")

        for account in results["accounts"]:
            platform = account["platform"][:18]
            url = account["url"][:40]
            print(f"  {self._color('│', 'blue')} {self._color(platform, 'green'):<20} {self._color('│', 'blue')} {url:<43} {self._color('│', 'blue')}")

        print(f"  {self._color('└' + '─' * 66 + '┘', 'blue')}")

        # Profile data if available
        for account in results["accounts"]:
            if account.get("profile_data"):
                print(f"\n  {self._color('📋 Profile Data from', 'cyan')} {self._color(account['platform'], 'green')}:")
                for key, value in account["profile_data"].items():
                    if value:
                        print(f"    • {key}: {value}")

        # Face analysis
        if "face_analysis" in results:
            face = results["face_analysis"]
            print(f"\n  {self._color('🎭 FACIAL RECOGNITION ANALYSIS', 'magenta')}")
            print(f"    Analyzed Images: {face['analyzed_accounts']}")
            print(f"    Platforms with Images: {', '.join(face['analysis_summary']['platforms_with_images'])}")

        print(f"\n{self._color('═' * 70, 'blue')}")

    def _show_csv(self, results: Dict):
        print("platform,url,response_time,profile_data")
        for account in results["accounts"]:
            profile = json.dumps(account.get("profile_data", {})).replace('"', '""')
            print(f"{account['platform']},{account['url']},{account.get('response_time', 0)},\"{profile}\"")

    def _show_html(self, results: Dict):
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Sherlock Pro - Results for {results['username']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }}
        h1 {{ color: #00d4ff; }}
        .summary {{ background: #16213e; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .account {{ background: #0f3460; padding: 15px; margin: 10px 0; border-radius: 8px; }}
        .platform {{ color: #e94560; font-weight: bold; }}
        a {{ color: #00d4ff; }}
    </style>
</head>
<body>
    <h1>🔍 Sherlock Pro Results</h1>
    <div class="summary">
        <p><strong>Username:</strong> {results['username']}</p>
        <p><strong>Platforms Scanned:</strong> {results['total_platforms']}</p>
        <p><strong>Accounts Found:</strong> {results['found_accounts']}</p>
        <p><strong>Time:</strong> {results['investigation_time']}s</p>
    </div>
"""
        for account in results["accounts"]:
            html += f"""
    <div class="account">
        <p class="platform">{account['platform']}</p>
        <p><a href="{account['url']}" target="_blank">{account['url']}</a></p>
    </div>
"""
        html += "</body></html>"
        print(html)
