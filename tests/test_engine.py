"""
Sherlock Pro - Unit Tests
"""

import pytest
import asyncio
from src.core.config import Config, PlatformConfig
from src.core.engine import SherlockEngine
from src.scanners.platform_scanner import PlatformScanner


class TestConfig:
    def test_default_config(self):
        config = Config()
        assert config.timeout == 30
        assert config.threads == 50
        assert config.verbose is False

    def test_custom_config(self):
        config = Config(timeout=60, threads=100, verbose=True)
        assert config.timeout == 60
        assert config.threads == 100
        assert config.verbose is True


class TestPlatformConfig:
    def test_load_default_platforms(self):
        platforms = PlatformConfig.get_default_platforms()
        assert len(platforms) > 0
        assert "GitHub" in platforms
        assert "Twitter/X" in platforms

    def test_platform_structure(self):
        platforms = PlatformConfig.get_default_platforms()
        for name, config in platforms.items():
            assert "url" in config
            assert "check_method" in config
            assert "category" in config


class TestPlatformScanner:
    def test_load_platforms(self):
        config = Config()
        scanner = PlatformScanner(config)
        platforms = scanner.load_platforms()
        assert len(platforms) > 0

    def test_filter_platforms(self):
        config = Config()
        scanner = PlatformScanner(config)
        platforms = scanner.load_platforms(["GitHub", "Twitter/X"])
        assert len(platforms) == 2


class TestSherlockEngine:
    @pytest.mark.asyncio
    async def test_engine_init(self):
        config = Config()
        engine = SherlockEngine(config)
        assert engine.config == config
        assert engine.session is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
