# Summarize my doc app

## Prerequisites

Fork this repo into your own GitHub account.
Edit the file `config.json` to put your AWS account ID and region.
Push these changes to your fork repository.

Install both nodejs and python on your computer.

Set up a virtual env:
```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

After this initial setup, you only need to run `source .venv/bin/activate` to use the virtual env for further development.

## 1 - Deploy with AWS CDK

Install CDK:
```sh
npm install -g aws-cdk
```

Synthesize your stacks:
```sh
cdk synth --app 'python3 cdk_stacks.py' SummarizeMyDoc-Backend
```

Set your AWS profile to get credentials into your favorite terminal
```sh
export AWS_PROFILE="default" # Replace it by your own profile you fools! :) Do NOT use default
```

Deploy your stacks:
```sh
cdk deploy --app 'python3 cdk_stacks.py' SummarizeMyDoc-Backend --profile $AWS_PROFILE
```

## 2 - Run locally

Edit the file `config.json` to specify the endpoint of your Amazon API Gateway previously deployed.

Make sure to set AWS credentials into your favorite terminal so this Streamlit app can perform API calls to AWS services on your behalf.

Run in the same terminal your streamlit app thanks to the following commands:
```sh
cd frontend
streamlit run Home.py
```

## Clean up

```sh
cdk destroy --app 'python3 cdk_stacks.py' SummarizeMyDoc-Backend --profile $AWS_PROFILE
```
