# What is Pants Web Server

## Installation
The server shares the same conda environment as the parent WhatIsPants
training project. See the [WhatIsPants README](../README.md) for
details setting up the conda enviornment.

## Local Development
For local development, you can use `docker-compose` to run:
- an `nginx` server for the frontend HTML & javascript files
- a lamdba emulator for the serverless functions

Install
[`sam-cli`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
```bash
conda install docker-compose==2.27.0
```

To start the server, run:
```bash
docker-compose up
```

# Problems
* Running sam local start-api with the default YOLO package using
  ```python
  model = YOLO("lvis_fash_m_50.pt")
  model.predict(image)
  ```
  fails with
  ```python
  [ERROR] Runtime.ImportModuleError: Unable to import module 'app': libGL.so.1:
   cannot open shared object file: No such file or directory
  ```
  * Presumably, this is because a Lambda environment doesn't have libGL
  * I will try to use a built docker image for the lambda environment (instead of a
    vanilla python lambda environment)