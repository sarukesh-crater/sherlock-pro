
"""
Sherlock Pro - Terminal Banner & Visual Effects
"""

import random
import time
from typing import Optional


class Banner:
    def __init__(self, no_color: bool = False):
        self.no_color = no_color
        self.colors = {
            "red": "\033[91m",
            "green": "\033[92m", 
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "bold": "\033[1m",
            "reset": "\033[0m"
        }

    def _color(self, text: str, color: str) -> str:
        if self.no_color:
            return text
        return f"{self.colors.get(color, '')}{text}{self.colors['reset']}"

    def show(self):
        """Display animated banner"""
        self._clear_screen()
        self._print_banner()
        self._print_tagline()
        self._print_separator()

    def _clear_screen(self):
        import os
        os.system("cls" if os.name == "nt" else "clear")

    def _print_banner(self):
        banner_art = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║     ███████╗██╗  ██╗███████╗██████╗ ██╗      ██████╗  ██████╗   ║
    ║     ██╔════╝██║  ██║██╔════╝██╔══██╗██║     ██╔═══██╗██╔════╝   ║
    ║     ███████╗███████║█████╗  ██████╔╝██║     ██║   ██║██║        ║
    ║     ╚════██║██╔══██║██╔══╝  ██╔══██╗██║     ██║   ██║██║        ║
    ║     ███████║██║  ██║███████╗██║  ██║███████╗╚██████╔╝╚██████╗   ║
    ║     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝   ║
    ║                                                                  ║
    ║                    ██████╗ ██████╗  ██████╗                      ║
    ║                    ██╔══██╗██╔══██╗██╔═══██╗                     ║
    ║                    ██████╔╝██████╔╝██║   ██║                     ║
    ║                    ██╔═══╝ ██╔══██╗██║   ██║                     ║
    ║                    ██║     ██║  ██║╚██████╔╝                     ║
    ║                    ╚═╝     ╚═╝  ╚═╝ ╚═════╝                      ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
        """

        lines = banner_art.strip().split("\n")
        for line in lines:
            colored_line = self._color(line, "cyan")
            print(colored_line)
            time.sleep(0.02)

    def _print_tagline(self):
        taglines = [
            "🔍 One Command. One Username. 100+ Platforms.",
            "🌐 Open Source Intelligence at Your Fingertips",
            "🕵️  Digital Footprint Reconnaissance Tool",
            "⚡ Lightning Fast OSINT Investigation"
        ]

        tagline = random.choice(taglines)
        centered = tagline.center(70)
        print(f"\n{self._color(centered, 'yellow')}")
        print(f"{self._color('    v2.0.0 | No Login Required | Completely Free'.center(70), 'green')}")

    def _print_separator(self):
        sep = "═" * 70
        print(f"\n{self._color(sep, 'blue')}\n")

    def print_status(self, message: str, status: str = "info"):
        """Print status message with icon"""
        icons = {
            "info": "ℹ️ ",
            "success": "✅",
            "warning": "⚠️ ",
            "error": "❌",
            "search": "🔍",
            "found": "🎯",
            "complete": "🎉"
        }

        colors = {
            "info": "blue",
            "success": "green",
            "warning": "yellow",
            "error": "red",
            "search": "cyan",
            "found": "magenta",
            "complete": "green"
        }

        icon = icons.get(status, "ℹ️ ")
        color = colors.get(status, "white")

        print(f"{icon} {self._color(message, color)}")
