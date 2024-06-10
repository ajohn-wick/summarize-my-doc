from aws_cdk import (
    App,
    Environment,
)
from pathlib import Path
from os import path
import json
from stacks.backend_stack import BackendStack

################### ENVIRONMENT VARIABLES ###################
aws_account_id = ""
aws_region = ""
config_file = Path(__file__).absolute().parent.__str__() + "/config.json"
################### END ENVIRONMENT VARIABLES ###################

if path.isfile(config_file) is False:
    raise Exception("File not found")

with open(config_file, "r") as config:
    config = json.load(config)
    aws_account_id = config["aws_account_id"]
    aws_region = config["aws_region"]

if aws_account_id != "" and aws_region != "":
    app = App()
    env = Environment(account=aws_account_id, region=aws_region)
    BackendStack(
        app,
        "SummarizeMyDoc-Backend",
        env=env
    )
    app.synth()
