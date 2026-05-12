# GitHub Autoloader

## Overview
A lightweight, zero-dependency Python automation script designed to stream files from a network share, rigorously sanitize them for sensitive data (API keys, IP addresses, emails), and autonomously commit and push them to a Git repository.

## Features
- **Network Transfer:** Automatically copies files from a networked NAS share.
- **Data Sanitization:** Uses regex heuristics to scrub emails, phone numbers, IPs, and API keys/secrets before they reach source control.
- **Git Automation:** Seamlessly handles `git add`, `git commit`, and `git push` without user intervention.
- **Portable:** Runs on standard Python with zero external pip dependencies.
