from PIL import Image
from SQLEngine import SQLEngine
from datetime import datetime
import os
import pandas as pd

def ensure_path(output_dir):
    """
    Checks a path to make sure it exists.
    If the path does not exist, it will create
    it and any parent direcotries that are needed.

    Parameters
    ----------
    output_dir : os.path object or string
        The directory path to check the existence of

    Returns
    ----------
    Creates the directory structure if it doesn't exist and returns nothing
    """

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

def chop_up_path(image_path):
    """
    Takes in a path and breaks it up into an array
    of [file name, file extension, base directory path].

    Parameters
    ----------
    image_path : os.path object or string
        The full path to the file in question.

    Returns
    ----------
    [base_name,image_ext,target_dir] : array[os.path objects]
        An array of file name, file extension, and base directory path.
    """

    base_name,image_ext = os.path.basename(image_path).split(".")
    target_dir = os.path.dirname(image_path)
    return([base_name,image_ext,target_dir])

def append_file_name(image_path,append):
    """
    Generates a new file path with a string, 'append', added to the filename.

    Parameters
    ----------
    image_path: os.path object or string
        The original file path whose filename will be changed.
    append: string
        A string to be appened to the filename.

    Returns
    ----------
    A new path : os.path object
        The newly generated full path with the new filename.
    """

    base_name,image_ext,target_dir = chop_up_path(image_path)
    new_raw_name = "{}_{}.{}".format(base_name,append,image_ext)
    return(os.path.join(target_dir,base_name,new_raw_name))

def make_raw(image_path, image_link):
    """
    Takes in an image path and the original link to the image,
    generates a new subfolder based on the image file name, and
    saves an unaltered version of the original image with the file
    name appended with '_raw'.

    Parameters
    ----------
    image_path : os.path object or string
        The path to where the image is currently stored.

    image_link : url or string
        The online source of the image, only used to add to output dataframe.

    Returns
    ----------
    A single row data frame : pandas dataframe
        A single row of data with image information to be added to a database.
    """
    new_path = append_file_name(image_path, "raw")
    raw_image = Image.open(image_path)
    ensure_path(os.path.dirname(new_path))
    raw_image.save(fp=new_path, format="JPEG")
    return(pd.DataFrame({
        "image_id": [os.path.basename(image_path).split(".")[0]],
        "file_name": [os.path.basename(new_path)],
        "file_path" : [new_path],
        "image_width_px": [raw_image.size[0]],
        "image_height_px": [raw_image.size[1]],
        "image_size_byte": [os.path.getsize(new_path)],
        "origin_link": [image_link],
        "date_saved": [datetime.now().strftime("%Y-%m-%d")]
        })
        )

def calc_thumb_resize(image_size):
    """
    Takes in image dimensions in pixels, calcualtes and returns a tuple 
    with new image dimensions such that the new hiegh would be no more
    than 72 pixels. This maintains original image aspect ratio.

    Parameters
    ----------
    image_size : tuple(int,int) or array[int,int]
        The original dimensions in pixels of an image.

    Returns
    ----------
    A tuple with new image dimensions : tuple(int,int)
        The new dimensions for the image to be resized into a thumbnail version.
    """

    ## target_height/raw_height = conv_factor to multiply raw by to get desired thumb size
    conv = 72/image_size[1]
    new_height = image_size[1]*conv
    new_width = image_size[0]*conv
    return((int(new_width),int(new_height)))


def make_thumb(image_path, image_link):
    """
    Takes in an image path, generates a thumbnail version,
    thumbnail version file path, and saves it out to the 
    new file path.

    Parameters
    ----------
    image_path : os.path object or string
        The path to where the image is currently stored.

    image_link : url or string
        The online source of the image, only used to add to output dataframe.

    Returns
    ----------
    A single row data frame : pandas dataframe
        A single row of data with image information to be added to a database.
    """

    new_path = append_file_name(image_path, "thumbnail")
    raw_image = Image.open(image_path)
    new_dims = calc_thumb_resize(raw_image.size)
    raw_image.resize(new_dims).save(fp=new_path, format="JPEG")

    return(pd.DataFrame({
        "image_id": [os.path.basename(image_path).split(".")[0]],
        "file_name": [os.path.basename(new_path)],
        "file_path" : [new_path],
        "image_width_px": [new_dims[0]],
        "image_height_px": [new_dims[1]],
        "image_size_byte": [os.path.getsize(new_path)],
        "origin_link": [image_link],
        "date_saved": [datetime.now().strftime("%Y-%m-%d")]
        })
        )

def remove_original(image_path):
    """
    Deletes the input file from local storage.

    Parameters
    ----------
     image_path : os.path object or string
        The path to where the image is currently stored.

    Returns
    ----------
    Does the file deletion in place, does not return anything.
    """

    os.remove(image_path)


def expand_dir_and_transform(image_path, image_link):
    """
    Takes in an image path and a url link to the source image.
    Processes the image to create a new directory and generates
    new versions of the image in the new directory. It then deletes
    the original image, leaving only the newly processed images.

    Parameters
    ----------
    image_path : os.path object or string
        The path to where the image is currently stored.

    image_link : url or string
        The online source of the image, only used to add to output dataframe.

    Returns
    ----------
    A data frame with one row per transformation : pandas dataframe
        A dataframe of data from the image transformation process.
    """

    try:
        raw = make_raw(image_path, image_link)
        thumb = make_thumb(image_path, image_link)
    except Exception as err:
        print("Was not able to transform {}!\nERROR: {}".format(image_path, err))
        raise
    else:
        remove_original(image_path)
        return(raw.append(thumb, ignore_index=True))

