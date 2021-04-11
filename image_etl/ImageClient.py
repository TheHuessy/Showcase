import concurrent.futures as cf
from imgurpython import ImgurClient
import os
import yaml

class ImPI:
    """
    A class used to access the imgur API and download images based on user inputted tags.
    """

    def __init__(self):
        """
        Initializing the class.

        Parameters
        ----------
        None

        Returns
        ----------
        self.creds : dict
            Credentials used to access the imgur API.

        self.client : ImgurClient
            The Imgur API Client.
        """

        with open(os.environ['CREDS_PATH']) as file:
            self.creds = yaml.full_load(file)
        self.client = ImgurClient(self.creds['im_cid'], self.creds['im_cs'])

    def get_file_name(self,url):
        """
        Takes in a url and returns the last section in the path, assumably the
        source file name.

        Parameters
        ----------
        url : url or string
            The url pointing to the image location on imgur.

        Returns
        ----------
        file name : string
            The file name of the file the url is pointing to.
        """

        return(url.split("/")[-1])

    def download_image(self, link, destination=None):
        """
        Downloads an image from a given url and saves it either
        in the script's directory or in a user given location after
        ensuring the existence of the destination directory.

        Parameters
        ----------
        link : url or string
            The url to the image to be downloaded

        destination : os.path object or string
            The destination path for the file to be downloaded to.
            If not supplied, the file will be downloaded to the
            directory that the script sits in.

        Returns
        ----------
        Downloads the file to the specified location, does not retrun anything.
        """

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
        """
        Takes in a tag to search imgur and returns a list of the top images with that tag.
        This is sure to sift through returned albums and galleries to get all images within.

        Parameters
        ----------
        tag : string
            A tag to search for.

        Returns
        ----------
        outs : array[string]
            An array of url strings pointing to images that match the tag.
        """

        galls_list = self.client.gallery_tag(tag)
        outs = [x.link for x in galls_list.items if not x.is_album and x.type == 'image/jpeg'] + [z[0]['link'] for z in [y.images for y in [x for x in galls_list.items if x.is_album]] if z[0]['type'] == 'image/jpeg']
        return(outs)

    def fetch_images_by_tag(self, tag, destination_path, threads=4):
        """
        Takes in a tag, a destination directory path, and number of threads.
        Searches imgur via API to get the top images with the specified
        tag, then proceeds to download each image to the specified destination
        using a threadpool of size `threads`.

        Parameters
        ----------
        tag : string
            A tag to search for.

        destination_path : os.path object or string
            The path to the destination directory for the image downloads.

        threads : integer
            The number of threads to spin up in the thread pool
            when downloading. If no value is passed, 4 threads
            will be assigned as default value.

        Returns
        ----------
        out_hash : dict{string:string}
            A dictionary of {image_link: download_full_path}.
        """

        out_hash = {}
        images_to_download = self.get_some_links_by_tag(tag)

        with cf.ThreadPoolExecutor(max_workers=threads) as executor:
            for image_link in images_to_download:
                executor.submit(self.download_image, image_link, destination_path)
                out_hash[image_link] = "{}/{}".format(destination_path,self.get_file_name(image_link))
        print("{} images have been downloaded to {}".format(len(images_to_download), destination_path))
        return(out_hash)


