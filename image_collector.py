# coding: utf-8
import json
import os
import sys
import requests

import urllib
from bs4 import BeautifulSoup


class Google:
    def __init__(self):
        self.GOOGLE_SEARCH_URL = 'https://www.google.co.jp/search'
        self.session = requests.session()
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})

    def search(self, keyword, amount):
        print('begin searching', keyword)
        query = self.query_gen(keyword)
        return self.image_search(query, amount)

    def query_gen(self, keyword):
        # search query generator
        page = 0
        while True:
            params = urllib.parse.urlencode({
                'q': keyword,
                'tbm': 'isch',
                'ijn': str(page)})

            yield self.GOOGLE_SEARCH_URL + '?' + params
            page += 1

    def image_search(self, query_gen, amount):
        # search image
        result = []
        total = 0
        while True:
            # search
            html = self.session.get(next(query_gen)).text
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select('.rg_meta.notranslate')
            jsons = [json.loads(e.get_text()) for e in elements]
            imageURLs = [js['ou'] for js in jsons]

            # add search result
            if not len(imageURLs):
                print('-> no more images')
                break
            elif len(imageURLs) > amount - total:
                result += imageURLs[:amount - total]
                break
            else:
                result += imageURLs
                total += len(imageURLs)

        print('-> found', str(len(result)), 'images')
        return result


def main():
    google = Google()
    if len(sys.argv) != 3:
        print('invalid argment')
        print('> ./image_collector_cui.py [target name] [download number]')
        sys.exit()
    else:
        # save location
        name = sys.argv[1]
        data_dir = 'data/'
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs('data/' + name, exist_ok=True)

        # search image
        result = google.search(
            name, amount=int(sys.argv[2]))

        # download
        download_error = []
        for i in range(len(result)):
            print('-> downloading image', str(i + 1).zfill(4))
            try:
                urllib.request.urlretrieve(
                    result[i], data_dir + name + '/' + str(i + 1).zfill(4) + '.jpg')
            except:
                print('--> could not download image', str(i + 1).zfill(4))
                download_error.append(i + 1)
                continue

        print('complete download')
        print('├─ download', len(result)-len(download_error), 'images')
        print('└─ could not download', len(
            download_error), 'images', download_error)


if __name__ == '__main__':
    main()
