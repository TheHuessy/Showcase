import os
from pyspark import SparkContext
from pathlib import Path
#import sys
import argparse

def get_args():
    args_setup = argparse.ArgumentParser(description='Spark Counter')
    args_setup.add_argument("--file_path", help="The path pointing to the file or folder of files you wish to count. Does not support HDFS just yet.")
    return(vars(args_setup.parse_args()))

def get_path(args):
    input_path = args['file_path']

    if not os.path.exists(input_path):
        raise FileNotFoundError('Path provided does not exist')

    files = list(input_path)

    if os.path.isdir(input_path):
        files = [x for x in os.listdir(input_path) if os.path.isfile(os.path.join(input_path,x))]

    return(files)


## get file uri
## check if it's a file or a directory
    ## if it's a directory, dive in one layer down and pull files into array
args = get_args()

print(get_path(args))
#for i in args:
#    print(i)
#    print(args[i])




## Accept file uri as parameter
## This will need to be a SparkUtils class that has file count as a method
    ## Or a module and figure out how to pass command line arg into Spark
        ## Should be as easy as getting ARGV in the code
## Read in file via uri (hadoop or not)
    ## Will that require too much file handling?

#print(sys.argv)


#sc = SparkContext(master='yarn', appName="R-Log-Test")


#data = sc.textFile("{}/user/pi/pyspark_practice/2020-11-01.csv".format(os.environ['NAMENODE_PATH']))

