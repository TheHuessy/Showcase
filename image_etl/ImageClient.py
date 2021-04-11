import concurrent.futures as cf
from imgurpython import ImgurClient
import os
import yaml

class ImPI:

    def __init__(self):
        with open(os.environ['CREDS_PATH']) as file:
            self.creds = yaml.full_load(file)
        self.client = ImgurClient(self.creds['im_cid'], self.creds['im_cs'])

    def get_file_name(self,url):
        return(url.split("/")[-1])

    def download_image(self, link, destination=None):
        dest = ""
        if destination:
            os.makedirs(destination) if not os.path.isdir(destination) else ""
            dest = "-O {}/{} ".format(destination,self.get_file_name(link))

        cmd = "wget {}{}".format(dest,link)
        print(cmd)
        try:
            os.system(cmd)
        except Exception as err:
            print("Could not download file: {}\nERROR:{}\n".format(link, err))

    def get_some_links_by_tag(self, tag):
        galls_list = self.client.gallery_tag(tag)
        outs = [x.link for x in galls_list.items if not x.is_album and x.type == 'image/jpeg'] + [z[0]['link'] for z in [y.images for y in [x for x in galls_list.items if x.is_album]] if z[0]['type'] == 'image/jpeg']
        return(outs)

    def fetch_images_by_tag(self, tag, destination_path, threads=4):
        out_hash = {}
        images_to_download = self.get_some_links_by_tag(tag)

        with cf.ThreadPoolExecutor(max_workers=threads) as executor:
            for image_link in images_to_download:
                executor.submit(self.download_image, image_link, destination_path)
                out_hash[image_link] = "{}/{}".format(destination_path,self.get_file_name(image_link))
        print("{} images have been downloaded to {}".format(len(images_to_download), destination_path))
        return(out_hash)


## TO DOWNLOAD NEW IMAGES:
# images = ImPI().fetch_images_by_tag("cats", "/home/pi/c_drive/test_dl")
# images is now a dict of {link_url:destination_path}




