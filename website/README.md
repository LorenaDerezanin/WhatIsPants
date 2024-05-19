# What is Pants Web Server

## Installation
The server shares the same conda environment as the parent WhatIsPants
training project. See the [WhatIsPants README](../README.md) for
details setting up the conda environment.

## Local Development
Install
[`sam-cli`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

To start the server, run:
```bash
sam build --use-container --cached --parallel && \
  sam local start-api
```

Open [index.html](frontend/index.html) in a browser to test the upload.

Alternatively, run the following `curl` command:
```bash
curl -v POST \ 
     -H "Content-Type: application/json" \
     -d "$(base64 -i ../test_images/tito.jpg)" \
     http://127.0.0.1:3000/whatispants/
```
