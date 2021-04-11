from ImageClient import ImPI
from SQLUtils import SQLUtils
import Transformations as trans
import pandas as pd

## Download the new images
images = ImPI().fetch_images_by_tag("cats", "/home/pi/c_drive/test_dl")
## Create raw and thumb files
image_out_data = pd.DataFrame()

for link in images:
    image_data = trans.expand_dir_and_transform(images[link], link)
    image_out_data = image_out_data.append(image_data, ignore_index=True)
    print("Finished processing {}".format(images[link]))

## Write data out to SQL
SQLUtils("novartis_dummy_db").write_dataframe_safe(image_out_data, "pulled_images")


