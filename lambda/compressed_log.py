import json
import logging
import boto3
import os
import gzip

def handler(event, context):
    try:
        # prepare data
        parsed_data = json.loads(event['Records'][0]['Sns']['Message'])
        s3 = boto3.client('s3')

        # setup data for creating log files
        log_name = parsed_data.get('name')
        log_content = parsed_data.get('content')
        compressed_log_key = f"compressed_log-{log_name}.txt.gz"
        
        # create compressed log
        compressed_log_content = gzip.compress(log_content.encode('utf-8'))
        create_compressed_log(s3, compressed_log_key, compressed_log_content)

        return {
            'statusCode': 200,
            'body': 'Compressed log file created successfully!'
        }

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

def create_compressed_log(s3, log_key, log_content)->None:    
    s3.put_object(
        Body=log_content,
        Bucket=os.environ['TARGET_BUCKET'],
        Key=log_key
    )