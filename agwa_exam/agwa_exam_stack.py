from aws_cdk import Stack, Duration
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_apigateway as apigateway
from constructs import Construct

PYTHON_RUNTIME = _lambda.Runtime.PYTHON_3_9
CODE_PATH = _lambda.Code.from_asset('lambda')

class AgwaExamStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       # create S3 buckets to store log files
        uncompressed_bucket = s3.Bucket(self, 'UncompressedBucket')
        compressed_bucket = s3.Bucket(self, 'CompressedBucket')

        # create Lambda function to store log file in S3 bucket
        compressed_log_lambda = _lambda.Function(
            self,
            'UncompressedLogLambda',
            runtime=PYTHON_RUNTIME,
            handler="uncompressed_log.handler",
            code=CODE_PATH,
            environment={
                'TARGET_BUCKET': uncompressed_bucket.bucket_name
            }
        )
        uncompressed_bucket.grant_read_write(compressed_log_lambda)

        # create Lambda function to compressed log file and store in S3 bucket
        compressed_log_lambda = _lambda.Function(
            self,
            'CompressedLogLambda',
            runtime=PYTHON_RUNTIME,
            handler='compressed_log.handler',
            code=CODE_PATH,
            environment={
                'SOURCE_BUCKET': uncompressed_bucket.bucket_name,
                'TARGET_BUCKET': compressed_bucket.bucket_name
            }
        )
        compressed_bucket.grant_read_write(compressed_log_lambda)

        # create API Gateway to trigger lambda function
        api = apigateway.RestApi(self, 'LogProcessingApi')
        integration = apigateway.LambdaIntegration(compressed_log_lambda)
        api.root.add_resource('create-log').add_method('POST', integration)
        
        # didn't create an API for the compressed log lambda function since the function is triggered by the uncompressed log lambda function (speculation)
