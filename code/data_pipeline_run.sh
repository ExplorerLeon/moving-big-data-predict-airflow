# ====================================================================
#   Moving Big Data Predict
#
#   Bash script to mount S3 bucket to EC2 instance and to initiate the
#   first step of data pipeline workflow which is to perform
#   transformations and and calculations on the raw input data
#   contained in the S3 bucket.
# ====================================================================

# -------- Mount S3 Bucket----------
# The general syntax followed by this command is:
# s3fs S3_BUCKET_NAME TARGET_FOLDER.
# If following the naming convention in the model solution,
# This would be:
s3fs de-mbd-predict-leon-smith-s3-source ~/s3-drive

python /home/ec2-user/s3-drive/Scripts/historical_processing-ec2.py
