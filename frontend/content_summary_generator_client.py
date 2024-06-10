from aws_requests_auth.aws_auth import AWSRequestsAuth
import boto3
import requests
import urllib.parse
from pathlib import Path
from os import path
import json

################### ENVIRONMENT VARIABLES ###################
config_file = Path(__file__).absolute().parent.parent.__str__() + "/config.json"
################### END ENVIRONMENT VARIABLES ###################


# Client for the content summary generator backend API
class ContentSummaryGeneratorAPI:
    if path.isfile(config_file) is False:
        raise Exception("File not found")

    with open(config_file, "r") as config:
        config = json.load(config)
        _aws_region = config["aws_region"]
        _api_endpoint = config["aws_api_gateway_endpoint"]
        if _api_endpoint.endswith("/"):
            _api_endpoint = config["aws_api_gateway_endpoint"][:-1]
        _api_endpoint += "/content-summary-generator"
    
    # Set up request signing for calls to the content summary generator API
    _aws_credentials = boto3.Session().get_credentials()
    _api_auth = AWSRequestsAuth(
        aws_access_key=_aws_credentials.access_key,
        aws_secret_access_key=_aws_credentials.secret_key,
        aws_token=_aws_credentials.token,
        aws_host=urllib.parse.urlparse(_api_endpoint).netloc,
        aws_region=_aws_region,
        aws_service="execute-api",
    )

    # Post a document's contents to the content summary generator backend API
    # and return the generated summary from the API response
    def get_content_summary(self, document: str) -> str:
        r = requests.post(
            url=self._api_endpoint,
            auth=self._api_auth,
            json={"doc_content": document},
        )

        if r.status_code == 200:
            # Example response:
            # { "content_summary": "Here is a short summary of the document..." }
            return r.json()["content_summary"]
        else:
            raise Exception(
                f"Content summary generator API returned failure status code: {r.status_code}"
            )
