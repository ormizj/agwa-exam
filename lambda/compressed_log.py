import json
import logging
import boto3
import os
import gzip
from utils.request_util import success_result, error_result

def handler(event, context):
    try:
        # prepare data
        parsed_data = json.loads(event['Records'][0]['Sns']['Message'])
        s3 = boto3.client('s3')

        # setup data for creating log files
        name_id = parsed_data.get('name_id')
        log_content = parsed_data.get('content')
        compressed_log_key = f"compressed_log-{name_id}.txt.gz"
        
        # create compressed log
        compressed_log_content = gzip.compress(log_content.encode('utf-8'))
        create_compressed_log(s3, compressed_log_key, compressed_log_content)

        return success_result(200, 'Compressed log file created successfully!')

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return error_result(500, f"Error: {str(e)}")

def create_compressed_log(s3, log_key, log_content)->None:    
    s3.put_object(
        Body=log_content,
        Bucket=os.environ['TARGET_BUCKET'],
        Key=log_key
    )