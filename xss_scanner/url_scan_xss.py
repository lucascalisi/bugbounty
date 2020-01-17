import time
import sys
from urllib.parse import urlparse
from log_to_file import LogToFile
import time
from xss_scanner.get_reflections import get_reflections

logger_in_file_scanner = LogToFile("scan_xss_url.out", "scan_xss_url_err.out")

def detect_reflections(url):
    try:
        reflections  = get_reflections(url)
        if reflections:
            print(reflections)
            logger_in_file_scanner.log_info(reflections)
    except Exception as e:
        logger_in_file_scanner.log_error(e)

def scan_xss_url(queue_msg):
    while True:
        url = queue_msg.get()
        if url == "FINISHED":
            return

        detect_reflections(url)
        time.sleep(1)