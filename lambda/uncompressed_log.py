import json
import logging
import boto3
import os
from utils.db_util import create_uuid

def handler(event, context):
    try:
        # prepare data
        parsed_data = json.loads(event['body'])
        s3 = boto3.client('s3')
        sns = boto3.client('sns')
        
        # default to 'untitled' if no name provided, considered returning an error with status code 400
        # but wouldn't make sense in a logging scenario (prioritize logging over error handling)
        name = parsed_data.get('name', 'untitled')
        name_id = f"{name}({create_uuid()})" # create unique id for log file
        
        # setup data for creating log files
        content = parsed_data.get('content')
        uncompressed_log_key = f"uncompressed_log-{name_id}.txt" 

        # create logs
        is_request_sent = create_compressed_log_request(sns, name_id, content)
        create_uncompressed_log(s3, uncompressed_log_key, content)

        # handle failed compression log request
        if (not is_request_sent):
            internal_uncompressed_log_key = f"internal_uncompressed_log-{name_id}.txt"
            create_uncompressed_log(s3, internal_uncompressed_log_key, 'Failed to compress log file')

        return {
            'statusCode': 200,
            'body': 'Log file created successfully!'
        }

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

def create_uncompressed_log(s3, log_key, log_content)->None:
    s3.put_object(
        Body=log_content,
        Bucket=os.environ['TARGET_BUCKET'],
        Key=log_key
    )

def create_compressed_log_request(sns, log_name, log_content)->bool:
    try:        
        payload = {
            'name': log_name,
            'content': log_content
        }
        
        # create compressed log request trough SNS
        response = sns.publish(
            TopicArn=os.environ['TOPIC_ARN'],  # Get the topic ARN from the environment variables
            Message=json.dumps(payload),
        )
        
        # return whether publishing the message was successful
        return 'MessageId' in response

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return False