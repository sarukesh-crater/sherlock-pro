# Contributing to Sherlock Pro

Thank you for your interest! Here's how to contribute:

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/sherlock-pro.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make changes and test
5. Submit a pull request

## Development Setup

```bash
pip install -r requirements.txt
pip install pytest flake8 black
```

## Code Style

- Follow PEP 8
- Use `black` for formatting: `black src/`
- Run tests: `pytest tests/ -v`

## Adding New Platforms

Edit `src/core/config.py` and add to `get_default_platforms()`:

```python
"PlatformName": {
    "url": "https://platform.com/{username}",
    "check_method": "status_code",
    "success_code": 200,
    "category": "social",
    "icon": "🚀"
}
```

## Commit Messages

- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Move cursor to..." not "Moves cursor to..."

## Questions?

Open an issue or discussion!
