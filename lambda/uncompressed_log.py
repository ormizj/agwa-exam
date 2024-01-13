from utils.time_util import get_current_timestamp
import json
import boto3
import os

def handler(event, context):
    try:        
        # parse request body into json
        parsed_data = json.loads(event['body'])

        # get current timestamp to ensure unique name for the log
        timestamp = get_current_timestamp()
        
        # default to 'untitled' if no name provided, considered returning an error with status code 400
        # but wouldn't make sense in a logging scenario (prioritize logging over error handling)
        log_name = parsed_data.get('name','untitled')
        log_key = f"uncompressed_log-{log_name}({timestamp}).txt"
        
        log_content = parsed_data.get('content')
        
        # returning bad request if log content is missing or empty (nothing to log)
        # TODO add this to the compressed log lambda function
        # if not log_content or not log_content.strip():
        #     return {
        #         'statusCode': 400,
        #         'body': 'Error: Log content is missing or empty'
        #     }

        # upload log file to S3 bucket
        s3 = boto3.client('s3')
        s3.put_object(
            Body=log_content,
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

def invoke_compression_lambda(log_name, log_content):
    try:
        # Create a Lambda client
        lambda_client = boto3.client('lambda')

        # Payload with the parameters you want to pass
        payload = {
            'name': log_name,
            'content': log_content
        }

        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName='CompressLogLambda',
            InvocationType='Event',  # Asynchronous invocation
            Payload=json.dumps(payload)
        )

        # Check the response
        if response['StatusCode'] == 200:
            return True
        else:
            logging.error(f"Lambda invocation failed with StatusCode: {response['StatusCode']}")
            return False

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return False