from datetime import datetime
import json
import boto3
import os

def handler(event, context):
    try:
        # parse request body into json
        parsed_data = json.loads(event['body'])

        # generate unique key for log file
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
        
        # default to 'untitled' if no name provided, considered returning an error with status code 400
        # but wouldn't make sense in a logging scenario
        name = parsed_data.get('name','untitled')
        log_key = f"uncompressed_log-{name} ({timestamp}).txt"

        # upload log file to S3 bucket
        s3 = boto3.client('s3')
        s3.put_object(
            Body=parsed_data['content'], 
            Bucket=os.environ['TARGET_BUCKET'], 
            Key=log_key
        )

        return {
            'statusCode': 200,
            'body': 'Log file stored successfully!'
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
