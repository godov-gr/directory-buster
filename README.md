# Directory Brute-Forcing Tool

This script is a directory brute-forcing tool that helps find accessible directories on a target URL. It uses a wordlist to systematically check for valid paths and logs the results.

## Features

- Multi-threaded brute-forcing for faster results.
- Automatic normalization and validation of URLs.
- Customizable via command-line arguments.
- Logs discovered directories and errors in real-time.

## Requirements

- Python 3.6 or later
- `requests` library

Install the required library with:
pip install requests

Usage

Basic Syntax:
python main.py <base_url> [options]

With Wordlist File"
python main.py https://example.com -w wordlist.txt -t 20

Using Wordlist via Stdin:
cat wordlist.txt | python main.py https://example.com
