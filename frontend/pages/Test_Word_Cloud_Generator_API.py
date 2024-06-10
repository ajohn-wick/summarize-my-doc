import streamlit as st

from aws_requests_auth.aws_auth import AWSRequestsAuth
import boto3
import requests
import urllib.parse
from pathlib import Path
from os import path
import json

################### ENVIRONMENT VARIABLES ###################
config_file = Path(__file__).absolute().parent.parent.parent.__str__() + "/config.json"
################### END ENVIRONMENT VARIABLES ###################

st.set_page_config(initial_sidebar_state="collapsed")

st.title("Test the Word Cloud Generator API")

if path.isfile(config_file) is False:
    raise Exception("File not found")

with open(config_file, "r") as config:
    config = json.load(config)
    aws_region = config["aws_region"]
    api_endpoint = config["aws_api_gateway_endpoint"]
    if api_endpoint.endswith("/"):
        api_endpoint = config["aws_api_gateway_endpoint"][:-1]
    api_endpoint += "/word-cloud-generator"

aws_credentials = boto3.Session().get_credentials()
api_auth = AWSRequestsAuth(
    aws_access_key=aws_credentials.access_key,
    aws_secret_access_key=aws_credentials.secret_key,
    aws_token=aws_credentials.token,
    aws_host=urllib.parse.urlparse(api_endpoint).netloc,
    aws_region=aws_region,
    aws_service="execute-api",
)

with st.form("test_word_cloud_generator_api"):
    content_input = st.text_area(
        "Text to analyze",
        "Vous savez, moi je ne crois pas qu'il y ait de bonne ou de mauvaise indentation. mais demain qui sait ? Peut-être simplement à me mettre au service de l’open source, à faire le don, le don de son code."
        "\nMoi, si je devais résumer ma vie de développeur aujourd’hui avec vous, je dirais que c’est d’abord des lignes de code."
        "\nDes langages qui m’ont tendu la main, peut-être à un moment où mon écran était bleu, où j’étais seul face à mon clavier."
        "\nEt c’est assez curieux de se dire que les bugs, les commits forgent un projet..."
        "\n\nParce que quand on a le goût du code, quand on a le goût de la fonction bien faite, le beau test, parfois on ne trouve pas l'API en face je dirais, la bibliothèque qui vous aide à avancer."
        "\nAlors ça n’est pas mon cas, comme je disais là, puisque moi au contraire, j’ai pu ; et je dis merci à Stack Overflow, je lui dis merci, je code la vie, je débugge la vie... je ne suis qu’amour !"
        "\nEt finalement, quand des gens me disent \"Mais comment fais-tu pour rester si patient ?\", je leur réponds très simplement que c’est ce goût du challenge, ce goût donc qui m’a poussé aujourd’hui à entreprendre un projet aux deadlines intenables..."
        "\n\nMais demain qui sait ? Peut-être simplement à me mettre au service de l’open source, à faire le don, le don de son code."
        "\n\nCopyright Nicolas Lecointre - https://lesjoiesducode.fr/",
        height=500
    )
    submitted = st.form_submit_button("Test")
    if submitted:
        r = requests.post(
            url=api_endpoint,
            auth=api_auth,
            json={"doc_content": content_input},
        )
        api_response_json = r.json()

        # Example response:
        # { "word_cloud_image": "<base-64 encoded image content>" }
        st.subheader("API Response")
        st.write(f"Status Code: {r.status_code}")
        st.code(json.dumps(api_response_json, indent=2), language="json")
