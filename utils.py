import urllib, json
from bs4 import BeautifulSoup
from timeout_decorator import timeout, TimeoutError
import os
def query_generator(keyword, url):
    page = 0
    while True:
        params = urllib.parse.urlencode({
            "q": keyword,
            "tbm": "isch",
            "ijn": str(page)
        })
        yield url + "?" + params
        page += 1

def search_image(sess, query, n):
    result = []
    total = 0
    while True:
        html = sess.get(next(query)).text
        bs = BeautifulSoup(html, "html.parser")
        elements = bs.select(".rg_meta.notranslate")
        tjson = [json.loads(e.get_text()) for e in elements]
        url = [js["ou"] for js in tjson]

        if not len(url):
            break
        elif len(url) > n - total:
            result += url[:n - total]
            break
        else:
            result += url
            total += len(url)
    print("-> found", str(len(result)), "images")
    return result

@timeout(8)
def get_imgf(url, save_dir):
    urllib.request.urlretrieve(url, save_dir)


def get_img(tup):
    indx = tup[0]
    url = tup[1]
    save_dir = tup[2]
    print("download image...", str(indx+1).zfill(5))
    save_dir = save_dir + str(indx+1).zfill(5) + ".jpg"

    try:
        get_imgf(url, save_dir)
    except TimeoutError:
        # os.remove(save_dir)
        print("could not download image(timeout)", str(indx+1).zfill(5))
    except:
        print("could not download image", str(indx+1).zfill(5))

