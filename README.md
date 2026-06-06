# 🔍 Sherlock Pro

> **Advanced OSINT Tool** — One command. One username. 100+ platforms scanned.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![OSINT](https://img.shields.io/badge/OSINT-Powered-red)](https://osint.org)

## 🌐 Live Web Demo

**[Try the Web UI →](https://sarukesh-crater.github.io/sherlock-pro/)**

The web interface runs entirely in your browser with animated effects, terminal simulation, and real-time scanning visualization.

## ✨ Features

- **🚀 One Command Scan** — Investigate a username across 100+ platforms instantly
- **🎭 Facial Recognition** — Analyze profile images across platforms
- **📧 Email Pattern Analysis** — Generate potential email addresses
- **📱 Phone Number Detection** — Extract phone patterns from usernames
- **🌐 Web UI** — Beautiful web interface that runs on GitHub Pages
- **⚡ Async Engine** — Concurrent scanning with 50+ threads
- **🎨 Stunning Terminal UI** — Animated banners, progress bars, and effects
- **📁 Export Options** — JSON, CSV, HTML reports
- **🔒 No Login Required** — Completely free, no API keys needed
- **🧅 Tor Support** — Route requests through Tor network

## 🚀 Quick Start

### CLI Usage

```bash
# Clone the repository
git clone https://github.com/yourusername/sherlock-pro.git
cd sherlock-pro

# Install dependencies
pip install -r requirements.txt

# Run investigation
python sherlock.py username123

# With facial recognition
python sherlock.py username123 --face

# Launch web UI locally
python sherlock.py --web-ui
```

### Web UI (GitHub Pages)

The web UI is already deployed at `https://yourusername.github.io/sherlock-pro/`

## 📋 CLI Commands

```bash
# Basic scan
python sherlock.py <username>

# Specific platforms
python sherlock.py <username> --platforms twitter,instagram,github

# Export results
python sherlock.py <username> --export results.json --output json

# Use proxy/Tor
python sherlock.py <username> --tor
python sherlock.py <username> --proxy http://127.0.0.1:8080

# Full options
python sherlock.py <username> --face --threads 100 --timeout 60 --verbose
```

## 🏗️ Architecture

```
sherlock-pro/
├── sherlock.py              # Main entry point
├── index.html               # Root redirect to web UI
├── web/
│   └── index.html             # GitHub Pages OSINT Web UI
├── src/
│   ├── core/
│   │   ├── engine.py        # Investigation engine
│   │   └── config.py        # Configuration management
│   ├── scanners/
│   │   ├── platform_scanner.py   # Platform detection
│   │   ├── email_scanner.py      # Email analysis
│   │   └── phone_scanner.py      # Phone analysis
│   ├── face/
│   │   └── analyzer.py        # Facial recognition
│   ├── ui/
│   │   ├── banner.py          # Terminal visuals
│   │   ├── progress.py        # Progress animation
│   │   └── results.py         # Results display
│   ├── utils/
│   │   ├── logger.py          # Logging
│   │   ├── rate_limiter.py    # Rate limiting
│   │   ├── proxy_manager.py   # Proxy handling
│   │   └── exporter.py        # Export utilities
│   └── web/
│       └── server.py          # Local web UI server
├── docs/
│   └── index.html             # Backup GitHub Pages source
├── data/
│   └── platforms.json         # Platform configurations
├── requirements.txt
└── README.md
```

## 🌐 Web Interface Features

The web UI (`web/index.html`) includes:

- **Animated Background** — Gradient orbs + grid overlay with pulse effects
- **Glowing Logo** — CSS animated pulse shadow
- **Interactive Search** — Real-time terminal simulation
- **Progress Animation** — Smooth progress bar with scan status
- **Result Cards** — Hover transforms, platform icons, metadata
- **Facial Recognition Gallery** — Profile image grid with hover zoom
- **Responsive Design** — Works on mobile and desktop
- **No Backend Required** — Pure HTML/CSS/JS, runs on any static host

## 🛡️ Supported Platforms

| Category | Platforms |
|----------|-----------|
| **Social** | Twitter/X, Instagram, Facebook, TikTok, Reddit, Pinterest, Snapchat |
| **Development** | GitHub, GitLab, Bitbucket, Dev.to, StackOverflow |
| **Professional** | LinkedIn, Medium |
| **Streaming** | Twitch, YouTube |
| **Music** | Spotify |
| **Messaging** | Discord, Telegram, WhatsApp |

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. Always:
- Respect privacy laws and regulations
- Obtain proper authorization before investigating individuals
- Use responsibly and ethically
- Do not use for harassment, stalking, or illegal activities

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>Built for the OSINT Community</b><br>
  ⭐ Star this repo if you find it useful!
</p>
