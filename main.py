from xss_scanner import url_scan_xss
from webscraper import url_discover
import multiprocessing as mp
import sys

def get_scope(file_name):
	file = open(file_name,"r")
	scope = []
	for line in file:
	    scope.append(line.replace('\n', ''))

	file.close()

	return scope

def main():

	if not len(sys.argv) > 1:
	    print("Not arguments")
	    exit

	url = sys.argv[1]
	scope_file = sys.argv[2]
	
	scope = get_scope(scope_file)

	queue_url = mp.Queue()

	r = mp.Process(target=url_scan_xss.scan_xss_url, args=(queue_url,))
	w = mp.Process(target=url_discover.get_link_references, args=(url, scope, queue_url,))
	r.start()
	w.start()
	print(f'[+] URL Discover: {url}')

if __name__ == "__main__":
	main()

