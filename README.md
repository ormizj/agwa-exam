# Getting Started

### DEPLOYMENT

1. Install libraries from the `requirements.txt` file

```
pip install -r requirements.txt
```

2. Run the server

```
cdk deploy
```

3. Run tests

4. Close the server when done

```
cdk destroy
```

---

### COMPONENTS

#### `lambda`

- `uncompressed_log.py` - Creates and saves an uncompressed log into the `UncompressedLogBucket` as a `txt` file. this lambda function will send an `SNS` request to the `CompressedLogLambda` to also create a compressed version of the log file

- `compressed_log.py` - Creates and saves a compressed log into the `CompressedLogBucket` as a `gz` file. this lambda function can only be called trough an `SNS` request

#### `utils`

- `db_util.py` - Contains functions that are related to the database (S3 buckets in this case)

- `request_util.py` - Contains functions that are related to handling/making requests

#### `agwa_exam`

- `agwa_exam_stack.py` - Contains the stack and API configurations of the AWS CDK app

#### `root`

- `app.py` - Initializes the `agwa_exam_stack.py` when running the `cdk deploy` command

---

### TESTING

Basic tests:

1. Running the basic tests from the unit tests (this will run a test for the `agwa_exam_stack.py` file)

> ```
> python -m unittest discover -p 'test_*.py' tests
> ```

2. Running the `uncompressed_log.py` lambda function

- After deployment send a request to the URL (example shows `create-log` to send request to `UncompressedLogLambda`)

> ```
> https://<api-id>.execute-api.<region>.amazonaws.com/<stage>/create-log
> ```

Example:

> ```
> https://8set3jo3gk.execute-api.eu-central-1.amazonaws.com/prod/create-log
> ```

- Include in the request body name and content values

Example:

> ```
> {"name": "test-file", "content": "testing \nmy \nlog \nfile"}
> ```

If the request was successful, there should be a `txt` file in the `uncompressedlogbucket` and a `gz` file in the `compressedlogbucket`

---

### PERSONAL NOTES

- error handling - I minimized the odds of error occurrences (doesn't check if a `name` is given, doesn't check if `content` is empty), I didn't want a log creation failing considering its job is to log failures

- lambda functions modularity - I kept the 2 functions as modular as possible (`compressed_log.py` & `uncompressed_log.py` call the `sanitize_filename` function, to ensure that each function can work individually), also success of the `UncompressedLogLambda` is not reliant on the success of the `CompressedLogLambda`

- `agwa_exam_stack.py` - Will grant `read` & `write` privileges to the lambda functions, I thought about checking if a file exists before saving a file, to ensure not overwriting existing file (`UUID4` does not guarantee 100% unique identifier, but the odds are so low, i didn't take that slim chance into consideration)

- `utils` - Kept the purpose of each util file quite broad, because of the lack of currently existing utilities

- Solution Architecture Diagram is located in `assets->solution-architecture-diagram` with all relevant files

---

### SOLUTION ARCHITECTURE DIAGRAM

![Solution Architecture Diagram](assets/solution-architecture-diagram/Solution%20Architecture%20Diagram.png)
