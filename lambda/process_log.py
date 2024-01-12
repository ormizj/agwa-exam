import json
import boto3
import os

def handler(event, context):
    # Get the log file content from the event
    log_content = event['body']

    # Get the target S3 bucket from the environment variables
    target_bucket = os.environ['TARGET_BUCKET']

    # Upload the log file content to the S3 bucket
    s3 = boto3.client('s3')
    s3.put_object(Body=log_content, Bucket=target_bucket, Key='log_file.txt')

    return {
        'statusCode': 200,
        'body': json.dumps('Log file processed and stored successfully!')
    }
