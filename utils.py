import urllib, json
from bs4 import BeautifulSoup
from timeout_decorator import timeout, TimeoutError
import os, re, imghdr
from PIL import Image
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

@timeout(5)
def get_imgf(url, save_file):
    if os.path.isfile(save_file):
        pass
    else:
        urllib.request.urlretrieve(url, save_file)


def get_img(tup):
    indx = tup[0]
    url = tup[1]
    save_dir = tup[2]
    p = "\.(jpg|png|bmp|gif|jpeg)"
    result = re.search(p, url ,re.IGNORECASE)
    if result:
        print("download image...", str(indx+1).zfill(5), end="\r")
        save_file = save_dir + str(indx+1).zfill(5) + result.group()
        try:
            get_imgf(url, save_file)
        except TimeoutError:
            print("-->could not download image(timeout)", str(indx+1).zfill(5))
            try:
                os.remove(save_file)
            except:
                pass
        except:
            print("-->could not download image", str(indx+1).zfill(5))
            try:
                os.remove(save_file)
            except:
                pass
        else:
            try:
                img = Image.open(save_file)
                img = []
            except:
                os.remove(save_file)

            


