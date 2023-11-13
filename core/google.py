import os
import sys
import time
import hashlib
from http.cookiejar import LWPCookieJar
from urllib.request import Request, urlopen
from urllib.parse import quote_plus, urlparse, parse_qs
from bs4 import BeautifulSoup

# URL templates to make Google searches.
url_home = "http://www.google.%(tld)s/"
url_search = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search&inurl=https"
url_next_page = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d&inurl=https"
url_search_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search&inurl=https"
url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d&inurl=https"

# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME', '.')
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load(ignore_discard=True)
except Exception:
    pass

def get_page(url):
    request = Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    cookie_jar.add_cookie_header(request)
    with urlopen(request) as response:
        html = response.read()
    cookie_jar.extract_cookies(response, request)
    cookie_jar.save(ignore_discard=True)
    return html

def filter_result(link):
    try:
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link
        if link.startswith('/url?'):
            link = parse_qs(o.query)['q'][0]
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link
    except Exception:
        pass
    return None

def search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0, only_standard=False):
    hashes = set()
    query = quote_plus(query)
    get_page(url_home % vars())
    if start:
        url = url_next_page_num % vars() if num != 10 else url_next_page % vars()
    else:
        url = url_search_num % vars() if num != 10 else url_search % vars()

    while not stop or start < stop:
        time.sleep(pause)
        html = get_page(url)
        soup = BeautifulSoup(html, "html.parser")
        anchors = soup.find(id='search').findAll('a')
        for a in anchors:
            if only_standard and (not a.parent or a.parent.name.lower() != "h3"):
                continue
            try:
                link = a['href']
            except KeyError:
                continue
            link = filter_result(link)
            if not link:
                continue
            h = hashlib.sha1(link.encode('utf-8')).hexdigest()
            if h in hashes:
                continue
            hashes.add(h)
            yield link
        if not soup.find(id='nav'):
            break
        start += num
        url = url_next_page_num % vars() if num != 10 else url_next_page % vars()

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Python script to use the Google search engine")
    parser.add_argument("--tld", default="com", help="Top level domain to use [default: com]")
    parser.add_argument("--lang", default="en", help="Produce results in the given language [default: en]")
    parser.add_argument("--num", type=int, default=10, help="Number of results per page [default: 10]")
    parser.add_argument("--start", type=int, default=0, help="First result to retrieve [default: 0]")
    parser.add_argument("--stop", type=int, default=None, help="Last result to retrieve [default: unlimited]")
    parser.add_argument("--pause", type=float, default=2.0, help="Pause between HTTP requests [default: 2.0]")
    parser.add_argument("--all", dest="only_standard", action="store_false", default=True, help="Grab all possible links from result pages")
    parser.add_argument("query", nargs='+', help="Query string")
    args = parser.parse_args()
    query = ' '.join(args.query)

    for url in search(query, **vars(args)):
        print(url)
