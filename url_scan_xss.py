import time
import sys
from urllib.parse import urlparse, parse_qs
import string
import random
from log_to_file import LogToFile
import time
import requests

url_with_reflected_params = set()

logger_in_file_scanner = LogToFile("scan_xss_url.out", "scan_xss_url_err.out")

def random_string(stringLength=15):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def evaluate_url(url):
    parsed_url = urlparse(url)

    url_without_qs = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    
    parsed_qs = parse_qs(parsed_url.query)
    if parsed_qs:
        logger_in_file_scanner.log_info(f'[+] URL with QueryParams: {url}')
        is_possible_url, new_url = check_reflected_params(url, url_without_qs, dict(parsed_qs))
        if is_possible_url and new_url not in url_with_reflected_params:
            url_with_reflected_params.add(new_url)
            log_message = f'[+] Reflection Detect: {new_url}'
            print('\033[92m' + log_message + '\033[0m')
            logger_in_file_scanner.log_info(log_message)
    else:
        logger_in_file_scanner.log_info(f'[+] URL without QueryParams: {url}')

def check_reflected_params(url, url_without_qs, params):
    modified_params = dict()
    exist_reflected_param = False
    for k, v in params.items():
        modified_params[k] = random_string()
    try:
        r = requests.get(url=url_without_qs, params=modified_params, timeout=5)
        for k, v in modified_params.items():
            if v in r.text:
                exist_reflected_param = True
                ori_param = k + "=" + params.get(k)[0].replace(" ", "+")
                url = url.replace(ori_param, k + "=*")

    except Exception as e:
        logger_in_file_scanner.log_error(e)

    return exist_reflected_param, url

def scan_xss_url(queue_msg):
    while True:
        url = queue_msg.get()
        if url == "FINISH":
            return

        logger_in_file_scanner.log_info(f'[+] Scanning URL: {url}')
        evaluate_url(url)
        time.sleep(1)