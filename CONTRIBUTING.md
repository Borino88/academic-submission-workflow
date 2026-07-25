# Contributing Guide

1. Fork the repository and create a feature branch (`git checkout -b feat/new-scorecard`).
2. Install development dependencies (`pip install -e .[dev]`).
3. Verify all pytest unit specifications pass (`pytest -v`).
4. Ensure Docker builds cleanly (`docker build -t test-academic .`).
5. Submit a pull request with clear description and test logs.
