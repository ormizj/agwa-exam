import json
import logging
import boto3
import os
import gzip
from utils.db_util import sanitize_filename
from utils.request_util import success_result, error_result, send_email_to_admin


def handler(event, context):
    """
    lambda function handler that creates a compressed log file in S3
    the lambda function should be sent through an sns event
    with the message containing: {name_id: str, content: str}

    Args:
        event (dict): the event data passed to the lambda function
        context (object): the runtime information of the lambda function

    Returns:
        dict: a dictionary containing the success or error response
    """
    try:
        # prepare data
        parsed_data = json.loads(event['Records'][0]['Sns']['Message'])
        s3 = boto3.client('s3')

        # prepare log key
        name_id = parsed_data.get('name_id')
        name_id = sanitize_filename(name_id)  # ensure name is valid
        compressed_log_key = f"compressed_log-{name_id}.txt.gz"

        # prepare log content
        log_content = parsed_data.get('content')

        # create compressed log
        compressed_log_content = gzip.compress(log_content.encode('utf-8'))  # using utf-8 encoding for a general purpose solution
        create_compressed_log(s3, compressed_log_key, compressed_log_content)

        return success_result(200, 'Compressed log file created successfully!')

    except Exception as e:
        send_email_to_admin()
        logging.error(f"Error: {str(e)}")
        return error_result(500, f"Error: {str(e)}")


def create_compressed_log(s3, log_key, log_content) -> None:
    """
    creates a compressed log file in S3

    Args:
        s3 (boto3.client): the S3 client object
        log_key (str): the key of the log file in S3
        log_content (bytes): the content of the log file to be compressed

    Returns:
        None
    """
    s3.put_object(
        Body=log_content,
        Bucket=os.environ['TARGET_BUCKET'],
        Key=log_key
    )
