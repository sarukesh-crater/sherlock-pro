#!/usr/bin/env python3
"""
Sherlock Pro - Advanced OSINT Tool
One command. One username. 100+ platforms.
"""

import sys
import asyncio
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.engine import SherlockEngine
from core.config import Config
from ui.banner import Banner
from ui.progress import ProgressManager
from ui.results import ResultsDisplay
from utils.logger import setup_logger

logger = setup_logger()


def create_parser():
    parser = argparse.ArgumentParser(
        description="Sherlock Pro - Advanced OSINT Username Investigation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sherlock.py username123
  python sherlock.py username123 --face --output json
  python sherlock.py username123 --platforms twitter,instagram,github
  python sherlock.py username123 --web-ui
        """
    )

    parser.add_argument("username", help="Username to investigate")
    parser.add_argument("--platforms", "-p", help="Comma-separated platforms (default: all)")
    parser.add_argument("--output", "-o", choices=["json", "csv", "html", "table"], 
                       default="table", help="Output format")
    parser.add_argument("--face", "-f", action="store_true", 
                       help="Enable facial recognition analysis")
    parser.add_argument("--timeout", "-t", type=int, default=30, 
                       help="Request timeout in seconds")
    parser.add_argument("--threads", type=int, default=50, 
                       help="Concurrent threads (default: 50)")
    parser.add_argument("--web-ui", "-w", action="store_true", 
                       help="Launch web interface")
    parser.add_argument("--no-color", action="store_true", 
                       help="Disable colored output")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--export", "-e", help="Export results to file")
    parser.add_argument("--proxy", help="Proxy URL (e.g., http://127.0.0.1:8080)")
    parser.add_argument("--tor", action="store_true", 
                       help="Route through Tor network")
    parser.add_argument("--version", action="version", version="Sherlock Pro v2.0.0")

    return parser


async def main():
    parser = create_parser()
    args = parser.parse_args()

    # Show banner
    banner = Banner(no_color=args.no_color)
    banner.show()

    if args.web_ui:
        from web.server import start_server
        await start_server()
        return

    # Initialize config
    config = Config(
        timeout=args.timeout,
        threads=args.threads,
        proxy=args.proxy,
        use_tor=args.tor,
        verbose=args.verbose,
        no_color=args.no_color
    )

    # Initialize engine
    engine = SherlockEngine(config)

    # Setup progress
    progress = ProgressManager(no_color=args.no_color)

    # Parse platforms
    platforms = None
    if args.platforms:
        platforms = [p.strip() for p in args.platforms.split(",")]

    # Run investigation
    try:
        progress.start()
        results = await engine.investigate(
            username=args.username,
            platforms=platforms,
            progress_callback=progress.update
        )

        # Facial recognition
        if args.face:
            from face.analyzer import FaceAnalyzer
            analyzer = FaceAnalyzer(config)
            face_results = await analyzer.analyze_accounts(results)
            results["face_analysis"] = face_results

        progress.complete()

        # Display results
        display = ResultsDisplay(no_color=args.no_color)
        display.show(results, format=args.output)

        # Export if requested
        if args.export:
            from utils.exporter import export_results
            export_results(results, args.export, args.output)
            print(f"\n📁 Results exported to: {args.export}")

    except KeyboardInterrupt:
        progress.stop()
        print("\n\n⚠️  Investigation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Investigation failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
