
"""
Sherlock Pro - Animated Progress & Status Display
"""

import sys
import time
import threading
from typing import Optional


class ProgressManager:
    def __init__(self, no_color: bool = False):
        self.no_color = no_color
        self.running = False
        self.current = 0
        self.total = 0
        self.current_platform = ""
        self.found_count = 0
        self._thread = None

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._animate)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=1)

    def complete(self):
        self.stop()
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()

    def update(self, current: int, total: int, platform: str, found: bool):
        self.current = current
        self.total = total
        self.current_platform = platform
        if found:
            self.found_count += 1

    def _animate(self):
        animations = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        idx = 0

        while self.running:
            if self.total > 0:
                pct = (self.current / self.total) * 100
                bar_width = 30
                filled = int(bar_width * self.current / self.total)
                bar = "█" * filled + "░" * (bar_width - filled)

                anim = animations[idx % len(animations)]

                status = f"\r{anim} [{bar}] {pct:.1f}% | {self.current}/{self.total} | Found: {self.found_count} | Current: {self.current_platform[:20]}"

                sys.stdout.write(status[:80])
                sys.stdout.flush()

            idx += 1
            time.sleep(0.1)


class Spinner:
    """Simple spinner for individual tasks"""

    def __init__(self, message: str = "Loading"):
        self.message = message
        self.running = False
        self._thread = None

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._spin)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=1)
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()

    def _spin(self):
        spins = ["◐", "◓", "◑", "◒"]
        idx = 0
        while self.running:
            sys.stdout.write(f"\r{spins[idx % len(spins)]} {self.message}...")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.15)
