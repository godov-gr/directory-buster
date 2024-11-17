import requests
import argparse
import sys
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
import logging

# Настройка логирования.
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Функция проверки и нормализации URL.
def normalize_url(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "http://" + url
    if not url.endswith('/'):
        url += '/'
    return url

# Функция для проверки URL.
def check_url(base_url, path):
    url = urljoin(base_url, path.strip())
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            logging.info(f"Found: {url}")
            return url
    except requests.exceptions.Timeout:
        logging.warning(f"Timeout: {url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error with {url}: {e}")
    return None

# Основная функция брутфорса.
def brute(base_url, wordlist, threads):
    base_url = normalize_url(base_url)
    logging.info(f"Starting brute force on {base_url}")

    found_urls = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_url, base_url, word): word for word in wordlist}
        for future in futures:
            result = future.result()
            if result:
                found_urls.append(result)

    logging.info(f"Brute force completed. Found {len(found_urls)} directories.")
    return found_urls

# Настройка парсинга аргументов.
def parse_arguments():
    parser = argparse.ArgumentParser(description="Directory brute-forcing tool.")
    parser.add_argument("base_url", help="The base URL to brute force.")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file.", required=False)
    parser.add_argument("-t", "--threads", help="Number of threads to use (default: 10).", type=int, default=10)
    return parser.parse_args()

# Основной запуск.
if __name__ == "__main__":
    args = parse_arguments()

    # Чтение wordlist.
    if args.wordlist:
        try:
            with open(args.wordlist, "r", encoding="utf-8") as file:
                wordlist = file.readlines()
        except FileNotFoundError:
            logging.error(f"Wordlist file not found: {args.wordlist}")
            sys.exit(1)
    else:
        logging.info("Reading wordlist from stdin...")
        wordlist = [line.strip() for line in sys.stdin]

    if not wordlist:
        logging.error("Wordlist is empty. Please provide a valid wordlist.")
        sys.exit(1)

    found = brute(args.base_url, wordlist, args.threads)

    if found:
        logging.info("Found directories:")
        for url in found:
            print(url)
    else:
        logging.info("No directories found.")


#python main.py https://example.com -w wordlist.txt -t 20               С файлом словаря.

#cat wordlist.txt | python main.py https://example.com