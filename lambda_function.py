import boto3
import os
import ftplib

from config import *

# AWS S3 Bucket name
bucket = S3_BUCKET

# FTP Credentials
ftp_host = FTP_HOST
username = FTP_USERNAME
password = FTP_PASSWORD
remote_directory = FTP_DIRECTORY

s3_client = boto3.resource('s3')


def getObjectsList(bucket):
    s3_files = []
    my_bucket = s3_client.Bucket(bucket)
    
    for file in my_bucket.objects.all():
        s3_files.append(file.key)
    return s3_files

def lambda_handler(event, context):
    # Connecting to FTP
    try:
        ftp = ftplib.FTP(ftp_host)
        ftp.login(username, password)
    except:
        print("Error connecting to FTP")

    try:
        ftp.cwd(remote_directory)
    except:
        print("Error changing to directory {}".format(remote_directory))
    
    # Create list of new files for sync
    ftp_files = ftp.nlst()
    current_s3_files = getObjectsList(bucket)
    delta = set(ftp_files).symmetric_difference(set(current_s3_files))
    files = list(delta)
    
    # Copy new files if they exist
    if len(files):    
        for file in files:
            try:
                print("Downloading new file {} ....".format(file))
                ftp.retrbinary("RETR " + file, open("/tmp/" + file, 'wb').write)
                try:
                    s3_client.meta.client.upload_file("/tmp/" + file, bucket, file)
                    print("File {} uploaded to S3".format(file))
                except:
                    print("ERROR: Can't uploading file {}!".format(file))
            except:
                print("ERROR: Can't download file {}!".format(file))
    else:
        print("No new files, SKIP")