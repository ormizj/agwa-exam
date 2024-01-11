### Log File Upload and Auto-Compression System

Assignment Goal: Design and implement a solution to enable log file upload and auto-comperssion.

#### Objective:

Design and implement a solution using AWS CDK to facilitate log file uploads, auto-compression, and
storage. The solution should include an API Gateway and Lambda to accept log file content and store in
S3, another Lambda function to compress the log file, and S3 buckets for both uncompressed and
compressed log files.

#### Requirements:

1. Create an AWS CDK script in Python to define the following components:
   - API Gateway to receive log file content via HTTP POST requests.
   - Lambda function to process the log file content and store it in S3.
   - Lambda function to compress the log file and store it in another S3 bucket.
   - Two S3 buckets: one for storing the uncompressed log files and another for storing the
     compressed log files.
2. Configure the API Gateway and the lambda to accept HTTP POST requests with the log file
   content in the request body and store it in S3.
3. When a log file is uploaded through the API Gateway, the 2nd Lambda function should be
   triggered to store the compressed version in the appropriate S3 bucket.
4. Include proper error handling in the Lambda function to manage potential issues during
   compression.
5. Provide a README.md file that explains the purpose of each component, gives instructions on
   how to deploy the infrastructure, and details how to test the system.

#### Bonus:

1. Implement a mobile client (iOS or Android) that listens for a silent push notification and
   automatically uploads a log file when triggered.
2. Enhance the mobile client to display relevant information about the compression process or
   handle errors gracefully.
3. Implement a back-office web application that enables sending the push notification to a specific
   mobile user.

#### Deliveries:

- Solution architecture diagram
- Working code of the codable parts of the solution (including the test scenario)
- Answer the questions below

Please don’t hesitate to ask for any information or if you have any questions.
Good luck!
The Agwa Team
