from aws_cdk import Stack, Duration
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_iam as iam
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from constructs import Construct

PYTHON_RUNTIME = _lambda.Runtime.PYTHON_3_9
CODE_PATH = _lambda.Code.from_asset('lambda')

class AgwaExamStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create SNS topic, buckets and lambdas
        uncompressed_log_bucket = s3.Bucket(self, 'UncompressedLogBucket')
        compressed_log_bucket = s3.Bucket(self, 'CompressedLogBucket')
        topic = sns.Topic(self, 'Topic')

        uncompressed_log_lambda = _lambda.Function(
            self,
            'UncompressedLogLambda',
            runtime=PYTHON_RUNTIME,
            handler='uncompressed_log.handler',
            code=CODE_PATH,
            environment={
                'TARGET_BUCKET': uncompressed_log_bucket.bucket_name,
                'TOPIC_ARN': topic.topic_arn
            }
        )
        uncompressed_log_bucket.grant_read_write(uncompressed_log_lambda)

        compressed_log_lambda = _lambda.Function(
            self,
            'CompressedLogLambda',
            runtime=PYTHON_RUNTIME,
            handler='compressed_log.handler',
            code=CODE_PATH,
            environment={
                'TARGET_BUCKET': compressed_log_bucket.bucket_name
            }
        )
        compressed_log_bucket.grant_read_write(compressed_log_lambda)

        # create SNS subscription from uncompressed log lambda to compressed log lambda
        topic.add_subscription(subscriptions.LambdaSubscription(compressed_log_lambda))
        topic.grant_publish(uncompressed_log_lambda)

        # create API gateway for uncompressed log lambda
        api = apigateway.RestApi(self, 'LogProcessingApi')
        integration = apigateway.LambdaIntegration(uncompressed_log_lambda)
        api.root.add_resource('create-log').add_method('POST', integration)