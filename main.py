import requests
import argparse
import sys
from urllib.parse import urlparse

def enum(url):
    if not url.parse(url).scheme:
        return "http://" + url
    return url

def brute(base_url, wordlist):
    base_url = enum(base_url)
    if not base_url.endswith('/'):
        base_url += '/'

    for word in wordlist:
        url = base_url + word.strip()
        try:
            response = requests.get(url, timeout=1)

            if response.status_code == 200:
                print(f"Found {url}")

        except requests.exceptions.Timeout:
            print(f"Timeout with {url}")
        except requests.ConnectionError:
            print(f"Filed Connection{url}")

parser = argparse.ArgumentParser()
parser.add_argument("base_url")
args = parser.parse_args()

wordlist = [line for line in sys.stdin]
brute(args.base_url, wordlist)

#cat wordlist.txt | python main.py https://example.com