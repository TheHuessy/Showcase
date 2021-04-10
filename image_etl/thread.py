#import threading
import os
import concurrent.futures as cf

links = ['https://i.imgur.com/C6CdOV4.jpg', 'https://i.imgur.com/6zh26D0.jpg', 'https://i.imgur.com/2IeMBHT.jpg', 'https://i.imgur.com/OGgVc4j.jpg', 'https://i.imgur.com/MZxkFBW.jpg', 'https://i.imgur.com/5nFThRQ.jpg', 'https://i.imgur.com/ZuDQv39.jpg', 'https://i.imgur.com/vLiNx6A.jpg', 'https://i.imgur.com/ENXL0eH.jpg', 'https://i.imgur.com/fmpowJ5.jpg', 'https://i.imgur.com/CXPjWWa.jpg', 'https://i.imgur.com/PTSKUqD.jpg', 'https://i.imgur.com/he9Cxgc.jpg', 'https://i.imgur.com/8Ia9H0L.jpg', 'https://i.imgur.com/DFNtbz5.jpg', 'https://i.imgur.com/4tXm0X5.jpg', 'https://i.imgur.com/ihR0lFw.jpg', 'https://i.imgur.com/y8l0O6T.jpg', 'https://i.imgur.com/2xaVIm9.jpg', 'https://i.imgur.com/AZGvReD.jpg', 'https://i.imgur.com/KEI1tCI.jpg', 'https://i.imgur.com/AzglW0x.jpg', 'https://i.imgur.com/bfI4WDW.jpg', 'https://i.imgur.com/Vlaoy7J.jpg', 'https://i.imgur.com/z8xEybZ.jpg', 'https://i.imgur.com/mYExqdd.jpg']

def download_image(links, link_idx, destination=None):
    dest = "-O {} ".format(destination) if destination else ""
    cmd = "wget {}{} > /dev/null 2>&1".format(dest,links[ink_idx])
    try:
        os.system(cmd)
    except Exception as err:
        print("Could not download file: {}\nERROR:{}\n".format(link, err))

class ThreadPool:
    def __init__(self, pool_size=4):
        self.pool = cf.ThreadPoolExecutor(max_workers=pool_size)

    def run(self, func, *args):
       # self.pool.map(func, *args)
        self.pool.sumbit(func, *args)
        self.pool.join()

ThreadPool(4).run(download_image, (links, "test_dl"))
