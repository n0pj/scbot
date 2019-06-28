import requests
from bs4 import BeautifulSoup
from utils import query_generator, search_image

class BOT(object):
    def __init__(self):
        super(BOT, self).__init__()
        self.url = 'https://www.google.co.jp/search'
        self.sess = requests.session()
        self.sess.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})

    def search_query(self, *args):
        print(args)
        query = query_generator(args[0], self.url)
        return search_image(self.sess, query, args[1])

    