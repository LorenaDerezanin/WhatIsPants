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

## Deployment

### Set up AWS CLI
The simplest way to set up the AWS CLI is to use the `aws configure --profile <profile-name>` command.
You will need to create an Access Key and a Secret Access Key in the AWS Console
and paste them below
```bash
aws configure --profile <profile-name>                  
  AWS Access Key ID [None]: <copy this from the AWS Console>
  AWS Secret Access Key [None]: <copy this from the AWS Console>
  Default region name [None]: eu-central-1  # This is Frankfurt, feel free to choose another region
  Default output format [None]: json
```

### Run guided deployment using `sam deploy`
Run the `sam deploy --guided` wizard using the `<profile-name>` created above.
```bash
AWS_PROFILE=<profile-name> sam deploy --guided

    Configuring SAM deploy
    ======================
    
            Looking for config file [samconfig.toml] :  Found
            Reading default arguments  :  Success
    
            Setting default arguments for 'sam deploy'
            =========================================
            Stack Name [whatispants]: 
            AWS Region [eu-central-1]: 
            #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
            Confirm changes before deploy [Y/n]: n
            #SAM needs permission to be able to create roles to connect to the resources in your template
            Allow SAM CLI IAM role creation [Y/n]: y
            #Preserves the state of previously provisioned resources when an operation fails
            Disable rollback [y/N]: n
            WhatIsPantsFunction has no authentication. Is this okay? [y/N]: y
            Save arguments to configuration file [Y/n]: y
            SAM configuration file [samconfig.toml]: 
            SAM configuration environment [default]: 
    
            Looking for resources needed for deployment:
            Creating the required resources...
            Successfully created!
    
            Managed S3 bucket: aws-sam-cli-managed-default-samclisourcebucket-zjevpajgf53z
            A different default S3 bucket can be set in samconfig.toml and auto resolution of buckets turned off by setting resolve_s3=False
             Image repositories: Not found.
             #Managed repositories will be deleted when their functions are removed from the template and deployed
             Create managed ECR repositories for all functions? [Y/n]: y
```