from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlparse
from collections import deque
import re
import sys
from log_to_file import LogToFile
import time

processed_urls = set()
new_urls = deque()
broken_urls = set()
out_of_scope_url = set()
temp_urls = set()

logger_in_file_discover = LogToFile("url_discover.out", "url_discover_err.out")

def get_link_references(url, scope, queue_msg):    
    new_urls = deque([url])
    scope_regex = generate_regex(scope)
    
    while len(new_urls):

        url = new_urls.popleft()
        processed_urls.add(url)

        if not valid_scope(urlparse(url).hostname, scope_regex):
            if url not in out_of_scope_url:
                out_of_scope_url.add(url)
                logger_in_file_discover.log_info(f'[+] Out of scope URL: {url}')
            continue

        queue_msg.put(url)
        logger_in_file_discover.log_info(f'[+] Processing URL: {url}')

        try:
            response = requests.get(url, timeout=5)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            if url not in broken_urls:
                broken_urls.add(url)
                logger_in_file_discover.log_info(f'[+] Broken URL: {url}')
            continue
        except Exception as e:
            logger_in_file_discover.log_error(e)
            continue
        
        get_absolute_paths(response.text)
        get_relatives_paths(response.text, url)

        for url in temp_urls:
            if not url in new_urls and not url in processed_urls:
                new_urls.append(url)

        temp_urls.clear()
        sys.stderr.flush()
        sys.stdout.flush()

        time.sleep(1)

    queue_msg.put("FINISHED")
    print(f'[+] Discovery finished')
    logger_in_file_discover.log_info(f'[+] Discovery finished')
    sys.stderr.flush()
    sys.stdout.flush()

def get_absolute_paths(body):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
    [temp_urls.add(url) for url in urls]

def get_relatives_paths(body, origin_url):
    soup = BeautifulSoup(body, 'lxml')
    for link in soup.find_all('a'):
        url = link.attrs["href"] if "href" in link.attrs else ''

        if not url or url == "/":
            continue

        parsed_url = urlparse(origin_url)
        if url.startswith("/") or url.startswith("#"):
            if url.startswith("//"):
                url = f'{parsed_url.scheme}:{url}'
            else:
                url = f'{parsed_url.scheme}://{parsed_url.netloc}{url}'

        temp_urls.add(url)

def valid_scope(hostname, regular_expressions):
    if not hostname:
        return False

    return [True for regex in regular_expressions if re.match(regex, hostname)]


def generate_regex(scope):
    regular_expressions = []
    for domain in scope:
        regex = "("
        last = ""
        for part in domain.split("."):
            if part == "*":
                part = ".*"

            if last:
                regex += last + "\."
            last = part

        regex += last + ")"
        regular_expressions.append(regex)

    return regular_expressions