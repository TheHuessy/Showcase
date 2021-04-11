### No need to be a full class, can just be a module with functions
"""
Transformation methods for the hypothetical image ETL
"""

from PIL import Image
from SQLEngine import SQLEngine
from datetime import datetime
import os
import pandas as pd


## Just the methods, none of the actual etl pipeline

### CREATE NEW DIRECTORY FOR IMAGE
    ## Allow to either create the image directory in place or to choose a new destination to put the transformed images in
        ## Have the default be to do it in place, and allow for another directory to be passed in

def ensure_path(output_dir):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

def chop_up_path(image_path):
    base_name,image_ext = os.path.basename(image_path).split(".")
    target_dir = os.path.dirname(image_path)
    return([base_name,image_ext,target_dir])

def append_file_name(image_path,append):
    base_name,image_ext,target_dir = chop_up_path(image_path)
    new_raw_name = "{}_{}.{}".format(base_name,append,image_ext)
    return(os.path.join(target_dir,base_name,new_raw_name))

def make_raw(image_path, image_link):
    new_path = append_file_name(image_path, "raw")
    raw_image = Image.open(image_path)
    ensure_path(os.path.dirname(new_path))
    raw_image.save(new_path)
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
    ## target_height/raw_height = conv_factor to multiply raw by to get desired thumb size
    conv = 72/image_size[1]
    new_height = image_size[1]*conv
    new_width = image_size[0]*conv
    return((int(new_width),int(new_height)))


def make_thumb(image_path, image_link):
    new_path = append_file_name(image_path, "thumbnail")
    raw_image = Image.open(image_path)
    new_dims = calc_thumb_resize(raw_image.size)
    raw_image.resize(new_dims).save(new_path)

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

    ## PG TABLE FORMAT:
    ##|image_id|file_name|file_path|image_width_px|image_height_px|image_size_byte|origin_link|date_saved|##

#    return(new_path)

    ##Going to need to redo what the output of the functions is
        ##need to be able to get the needed pg data with each run
            ##Output two rows per run: one for raw, one for the thumb
                ## each iteration of this function then returns a two row dataframe
            ##Might be able to get all needed info from the thumb run
                ##Then just copy that row and swap out the file name path(s) for raw
                    ##Don't have to worry about returning and merging dataframe rows
                    ##Have another task, get_image_data that parses a single row output from make_thumb and then adds the new line with raw swapped in and return the two row df that way

def remove_original(image_path):
    os.remove(image_path)


def expand_dir_and_transform(image_path, image_link):
#    base_name,image_ext = os.path.basename(image_path).split(".")
#    target_dir = os.path.dirname(image_path)
    ## Call specific functions for each file type
        ## Rename the file that's already downloaded to raw, no real transformation other than to be renamed
        try:
            raw = make_raw(image_path, image_link)
            thumb = make_thumb(image_path, image_link)
        except Exception as err:
            print("Was not able to transform {}!\nERROR: {}".format(image_path, err))
            raise
        else:
            remove_original(image_path)
            return(raw.append(thumb, ignore_index=True))



### START HERE!! vvvvvv ###


## THIS ORIGINAL IDEA OF JUST CHANGING A DUPLICATED ROW TO MATCH WON'T WORK BECAUSE WE NEED TO PEEK AT THE IMAGE TO GET HEIGHT/WIDTH/SIZE
## HAVE TO BUILD IN DATA COLLECTION INTO BOTH FILE TRANSFORMATIONS AND HAVE THEM ALL RETURN A SINGLE LINE WHICH ARE THEN APPENEDED AND RETURNED TO BE ADDED TO SQL
    ##THE LAST PART WILL TAKE PLACE IN WHATEVER SCRIPT CALLS THE METHODS FROM THIS ONE


##-- Rewrite make_raw to output the same df as make_thumb
    ## probably going to need to make a dataframe assembling function




#        output_data = thumb.append(thumb, ignore_index=True)
#        output_data.loc[1, "file_name"] = ""
#        output_data.loc[1, "file_path"] = raw

        ## Creating the thumbnail will be an actual transformation
            # Open image and load into PIL
            # Get info from that and calc new height AND width
            # img.resize(size=(new_width,new_height)).save(new_filepath)
        ##Remove original if all other images have been created
        ##Going to need to redo what the output of the functions is
            ##need to be able to get the needed pg data with each run
                ##Output two rows per run: one for raw, one for the thumb
                    ## each iteration of this function then returns a two row dataframe


### RESIZE IMAGE
    ## Thumbnail should be height of 75 pixels, make it scale like with cropper

### WRITE IMAGE OUT

### GET DATA FROM IMAGE (RAW, RESIZED)
    ## Probs good to add functionality in imageclent that outputs a dict of the file location:origin link
        ##Can add that info to the db
        ## |image_id(original image name)|image_name(thumb vs raw)|width|height|orign_link|current_path|

### WRITE DATA OUT TO POSTGRES
    ## Utilize the SQL Utils for this

