import os
# ftp credentials
FTP_HOST = os.getenv("FTP_HOST")
FTP_PORT = os.getenv("FTP_PORT")
FTP_USERNAME = os.getenv("FTP_USERNAME")
FTP_PASSWORD = os.getenv("FTP_PASSWORD")
FTP_DIRECTORY = os.getenv("FTP_DIRECTORY")

# s3 parameters
S3_BUCKET = os.getenv("S3_BUCKET")