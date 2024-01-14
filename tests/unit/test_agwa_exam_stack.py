import sys
sys.path.append('../../agwa_exam')

import unittest
from aws_cdk import App
from agwa_exam.agwa_exam_stack import AgwaExamStack

class TestAgwaExamStack(unittest.TestCase):

    def test_stack_creation(self):
        app = App()
        stack = AgwaExamStack(app, 'TestStack')
        
        # synthesize the stack
        template = app.synth().get_stack_by_name('TestStack').template

        # dynamic assertions for S3 buckets, lambda functions, SNS topic, and API gateway
        self.assert_resource_with_property(template, 'AWS::S3::Bucket', 'CompressedLogBucket')
        self.assert_resource_with_property(template, 'AWS::S3::Bucket', 'UncompressedLogBucket')

        self.assert_resource_with_property(template, 'AWS::Lambda::Function', 'CompressedLogLambda')
        self.assert_resource_with_property(template, 'AWS::Lambda::Function', 'UncompressedLogLambda')

        self.assert_resource_with_property(template, 'AWS::SNS::Topic', 'Topic')

        self.assert_resource_with_property(template, 'AWS::ApiGateway::RestApi', 'LogProcessingApi')

    # checking if prefix is in the logical id of the resource, and not exact match
    def assert_resource_with_property(self, template, resource_type, resource_name_prefix):
        for resource_logical_id, resource_value in template['Resources'].items():
            if resource_value['Type'] == resource_type and resource_name_prefix in resource_logical_id:
                return
        self.fail(f"{resource_type} with name prefix '{resource_name_prefix}' not found in template")

if __name__ == '__main__':
    unittest.main()