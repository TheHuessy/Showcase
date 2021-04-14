# image_qc

## Description
A local web app that reads in the data from the imgur [image ETL](../image_etl/) and displays a preview image. The app also allows a user to select and zoom in on each image.

Can be deployed locally using the [runner file](image_qc_runner.R) after sourcing required crednetials.

## Files

*[image_qc_runner.R](image_qc_runner.R):*

A runner file that sets the host ip and port and then executes an instance of the app. Logging output is printed to terminal.

Usage:

`$ Rscript image_qc_runner.R`


*[image_qc_viewer/server.R](image_qc_viewer/server.R):*

The server file for the shiny app. This contols the backend functions and interactions with the Postgres server. The workflow of the app is as follows:

* Pull in credentials from environment variable loaded prior to execution

* Pull the imgur ETL data from postgres

* Generate a global id variable `image_id` using the filename (sans file extension) of the first image returned from the db

* Cache the raw photo for better zoom creation later on

* Get file path to `_preview` image based on `image_id`

* Load the preview image and display it on the main page section

* Generate and display image statistics for the preview image and the underlying raw image

A user can select a section of the preview image which generates a "zoomed in" image below. The zoomed in version is generted as follows:

* Record pixel locations of the selected box

* Convert those values using the conversion factor from the db between the preview image's dimensions and the underlying raw image's dimensions

* Generate a `crop_string` based on the converted dimensions that can be used with `magick`'s `image_crop()` function

* Using the cached raw image, generate a cropped version using the converted dimensions of the slected box and save it locally as `tmp.jpg`

* Change the output of the main page of the app to include a second image viewing object under the preview image

When a user disconnects from the app, it ensures that any sql connection that might be active is disconnected and deletes `tmp.jpg`

*[image_qc_viewer/ui.R](image_qc_viewer/ui.R):*

The ui file for the shiny app. This sets the front end aspects of the app, providing the placeholders for the dynamic image displays and file selection dropdown with `uiOutput()` objects. This app uses the `shinydashboard` package to wrap the UI and make it look a little bit more presentable.

*[image_qc_viewer/www/custom.css](image_qc_viewer/www/custom.css):*

A CSS file to handle the look and aesthetic actions of the app. At this stage, it just ensures that the main page will allow a user to scroll to the left or right if a zoomed image is larger than the size of the screen. Other aesthetics can be changed here.


## Limitations

This app is incredibly limited and really only meant as a way to enhance the example of the imgur ETL and any other image related work. 

Shiny apps, and R in general, can only operate on a single threaded basis. Furthermore, this app is highly reliant on RAM which it has to share with the data it works with and especially with the images it processes. A better solution would need to be written in a more robust language and connected to a real webserver as opposed to just starting up the instance and shoving it into a specified port. 

The advantage of this app is that it is easy to code and able to get up and running, processing images and managing data connection, within a number of hours. It can also easily be deployed locally using simple bash commands or via docker.

This is not a wonderful production solution, but it is an incredible proof of concept tool.

