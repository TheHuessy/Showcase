### No need to be a full class, can just be a module with functions
"""
Transformation methods for the hypothetical image ETL
"""

import PIL
from SQLUtils import SQLUtils

## Just the methods, none of the actual etl pipeline

### CREATE NEW DIRECTORY FOR IMAGE
    ## Allow to either create the image directory in place or to choose a new destination to put the transformed images in
        ## Have the default be to do it in place, and allow for another directory to be passed in

### RESIZE IMAGE
    ## Thumbnail should be height of 75 pixels, make it scale like with cropper

### WRITE IMAGE OUT

### GET DATA FROM IMAGE (RAW, RESIZED)
    ## Probs good to add functionality in imageclent that outputs a dict of the file location:origin link
        ##Can add that info to the db
        ## |image_id(original image name)|image_name(thumb vs raw)|width|height|orign_link|current_path|

### WRITE DATA OUT TO POSTGRES
    ## Utilize the SQL Utils for this

