import json
import logging
import boto3
import os
from utils.db_util import create_uuid, sanitize_filename
from utils.request_util import success_result, error_result, send_email_to_admin

def handler(event, context):
    try:
        # only allow supported invocation methods, to avoid false alarms
        if 'httpMethod' not in event:
            return error_result(400, 'Invalid invocation method, please use HTTP request')
        
        # prepare data
        parsed_data = json.loads(event['body'])
        s3 = boto3.client('s3')
        sns = boto3.client('sns')
        
        # prepare log key
        # default to 'untitled' if no name provided, considered returning an error with status code 400
        # but wouldn't make sense in a logging scenario (prioritize logging over error handling)
        name = parsed_data.get('name', 'untitled')
        name_id = f"{name}({create_uuid()})" # create unique id for log file
        name_id = sanitize_filename(name_id) # ensure name is valid
        uncompressed_log_key = f"uncompressed_log-{name_id}.txt"         

        # prepare log content
        content = parsed_data.get('content')

        # create logs
        is_request_sent = create_compressed_log_request(sns, name_id, content) # send async request
        create_uncompressed_log(s3, uncompressed_log_key, content) # send sync request

        # handle failure to send compressed log request
        if (not is_request_sent):
            send_email_to_admin() # send an email, etc... to the admin to notify of the issue

        return success_result(200, 'Log file created successfully!')

    except Exception as e:
        send_email_to_admin()
        logging.error(f"Error: {str(e)}")
        return error_result(500, f"Error: {str(e)}")

def create_uncompressed_log(s3, log_key, log_content)->None:
    s3.put_object(
        Body=log_content,
        Bucket=os.environ['TARGET_BUCKET'],
        Key=log_key
    )

def create_compressed_log_request(sns, name_id, log_content)->bool:
    try:        
        payload = {
            'name_id': name_id,
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
    