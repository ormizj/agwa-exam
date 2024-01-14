import json
import logging
import boto3
import os
import gzip
from utils.db_util import sanitize_filename
from utils.request_util import success_result, error_result, send_email_to_admin

def handler(event, context):
    try:
        # only allow supported invocation methods, to avoid false alarms
         if 'Records' not in event:
            return error_result(400, 'Invalid invocation method, please use SNS request.')
        
        # prepare data
        parsed_data = json.loads(event['Records'][0]['Sns']['Message'])
        s3 = boto3.client('s3')

        # prepare log key
        name_id = parsed_data.get('name_id')
        name_id = sanitize_filename(name_id) # ensure name is valid
        compressed_log_key = f"compressed_log-{name_id}.txt.gz"
        
        # prepare log content
        log_content = parsed_data.get('content')
        
        # create compressed log
        compressed_log_content = gzip.compress(log_content.encode('utf-8')) # using utf-8 encoding for a general purpose solution
        create_compressed_log(s3, compressed_log_key, compressed_log_content)

        return success_result(200, 'Compressed log file created successfully!')

    except Exception as e:
        send_email_to_admin()
        logging.error(f"Error: {str(e)}")
        return error_result(500, f"Error: {str(e)}")

def create_compressed_log(s3, log_key, log_content)->None:    
    s3.put_object(
        Body=log_content,
        Bucket=os.environ['TARGET_BUCKET'],
        Key=log_key
    )
    