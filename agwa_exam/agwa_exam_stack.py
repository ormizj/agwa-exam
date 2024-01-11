from aws_cdk import Stack, Duration
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_apigateway as apigateway
from constructs import Construct

class AgwaExamStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       # Create S3 buckets
        uncompressed_bucket = s3.Bucket(self, "UncompressedBucket")
        compressed_bucket = s3.Bucket(self, "CompressedBucket")

        # Create Lambda function to process and store log file in S3
        process_log_lambda = _lambda.Function(
            self, "ProcessLogLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="process_log.handler",
            code=_lambda.Code.from_asset("lambda_functions"),
            environment={
                "TARGET_BUCKET": uncompressed_bucket.bucket_name
            }
        )
        uncompressed_bucket.grant_read_write(process_log_lambda)

        # Create Lambda function to compress log file and store in another S3 bucket
        compress_log_lambda = _lambda.Function(
            self, "CompressLogLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="compress_log.handler",
            code=_lambda.Code.from_asset("lambda_functions"),
            environment={
                "SOURCE_BUCKET": uncompressed_bucket.bucket_name,
                "TARGET_BUCKET": compressed_bucket.bucket_name
            }
        )
        compressed_bucket.grant_read_write(compress_log_lambda)

        # Create API Gateway to receive log file content via HTTP POST requests
        api = apigateway.RestApi(self, "LogFileUploadApi")
        integration = apigateway.LambdaIntegration(process_log_lambda)
        api.root.add_resource("upload").add_method("POST", integration)
