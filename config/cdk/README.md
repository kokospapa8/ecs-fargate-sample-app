#How to deploy CDK

## Install AWS-CDK
[How to InstallAWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
- install CDK
- set AWS credentials

## install requirements
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Environment variables
```
CDK_DEFAULT_ACCOUNT - this is your account_id
CDK_DEFAULT_REGION - set your default region
KEY_PAIR_NAME - create key pair refer to following step
```
[How to create key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)


## Run AWS CDK
```
$ cd config/cdk
$ cdk synth 
$ cdk deploy

```