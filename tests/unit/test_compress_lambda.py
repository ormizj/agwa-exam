import unittest
from unittest.mock import patch
from moto import mock_s3
import boto3
import os
import gzip
import io
import json
from compress_log import handler

@mock_s3
class TestHandler(unittest.TestCase):
    @patch.dict(os.environ, {'SOURCE_BUCKET': 'source-bucket', 'TARGET_BUCKET': 'target-bucket'})
    def test_handler(self):
        # Set up the mock S3 environment
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='source-bucket')
        conn.create_bucket(Bucket='target-bucket')

        # Add a file to the source bucket
        conn.Object('source-bucket', 'log_file.txt').put(Body=b'This is a test log file')

        # Call the handler function
        result = handler({}, {})

        # Check the result
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(json.loads(result['body']), 'Log file compressed and stored successfully!')

        # Check that the compressed file was added to the target bucket
        target_obj = conn.Object('target-bucket', 'log_file.txt.gz').get()
        self.assertEqual(gzip.decompress(target_obj['Body'].read()), b'This is a test log file')

if __name__ == '__main__':
    unittest.main()