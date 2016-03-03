# Author Thomas F McGeehan V
from google import search
from BeautifulSoup import *
import urllib
import random
from time import sleep
import warnings

warnings.filterwarnings('ignore')
# Sleep for a random number of seconds to make the web requests appear more "human-like"
def sleep_seconds():
    sleep(random.randrange(1, 4))

result_size = 10
# These should be displayed in a combo box and read from a database
# users = ['jimmy smith', 'john anderson']

# for user in users :
#     print user
#     ctr=0
#     for url in search(user, stop=result_size):
#         print url
#         ctr += 1
#         sleep_seconds()
#     print ctr


def getGoogleSearch(users):
	result = []
	for user in users:
	    ctr = 0
	    urls = []
	    for url in search(user, stop=result_size):
	        urls.append(url)
	        ctr += 1
	    result.append({
	    	'user': user,
	    	'ctr': ctr,
	    	'urls': urls
	    	})
	return result
