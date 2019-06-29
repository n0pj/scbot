import json, os, sys, urllib
from bs4 import BeautifulSoup
from model import BOT
from multiprocessing import Pool
import json
from utils import get_img
import time
from PIL import Image

def main():
    bot = BOT()
    if len(sys.argv) != 3:
        print('invalid argment')
        sys.exit()
    else:
        time1 = time.time()
        f = open("carmaker.json", "r")
        jsond = json.load(f)
        for i in jsond:
            data_dir = "collect/"

            os.makedirs(data_dir + i, exist_ok=True)

            for j in jsond[i]:
                print(j)
                os.makedirs(data_dir + i + "/" + j, exist_ok=True)
                for k in jsond[i][j]:
                    os.makedirs(data_dir + i + "/" + j + "/" + k, exist_ok=True)
                    for l in jsond[i][j][k]:
                        try:                                
                            os.makedirs(data_dir + i + "/" + j + "/" + k + "/" + l, exist_ok=True)

                            result = bot.search_query("Automotive "+l, int(1000))
                            with Pool(8) as pool:
                                
                                save_dir = data_dir + i + "/" + j + "/" + k + "/" + l + "/"
                                save_dir_list = []
                                sd = [save_dir_list.append(save_dir) for i in range(len(result))]

                                pool.map(get_img, zip(range(len(result)), result, save_dir_list))
                            print("----------------------------------")
                            print("complete")
                            print("Time: {:.0f}s".format(time.time()-time1))
                            print("----------------------------------")
                        except KeyboardInterrupt:
                            sys.exit()
        print("Time: {:.0f}s".format(time.time()-time1))




if __name__ == "__main__":
    main()
