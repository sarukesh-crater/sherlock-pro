.PHONY: install test run clean web lint

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

run:
	python sherlock.py

web:
	python sherlock.py --web-ui

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/

lint:
	flake8 src/ --max-line-length=100
	black src/ --check

format:
	black src/
