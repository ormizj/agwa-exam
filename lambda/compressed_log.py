import json
import boto3
import os
import gzip
import io

def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Log file compressed and stored successfully!')
    }
    
    # Get the source and target S3 buckets from the environment variables
    target_bucket = 

    # Get the log file content from the source S3 bucket
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=source_bucket, Key='log_file.txt')
    log_content = response['Body'].read()

    # Compress the log file content
    compressed_content = gzip.compress(log_content)

    # Upload the compressed content to the target S3 bucket
    s3.put_object(
        Body=compressed_content,
        Bucket=os.environ['TARGET_BUCKET'],
        Key='log_file.txt.gz'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Log file compressed and stored successfully!')
    }