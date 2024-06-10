from aws_cdk import (
    BundlingOptions,
    BundlingOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_nodejs as nodejs,
    aws_logs as logs,
)
from constructs import Construct
from pathlib import Path
from os import path


# Deploy an API Gateway that serves the content summary generator API and word Cloud generator API
class BackendStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Content summary generator Lambda function, written in Typescript
        function_code_dir = (
            Path(__file__).absolute().parent.parent.__str__() + "/backend/"
        )
        summary_lambda_function = nodejs.NodejsFunction(
            self,
            "ContentSummaryGenerator",
            entry=path.join(function_code_dir, "content-summary-generator/index.ts"),
            deps_lock_file_path=path.join(
                function_code_dir, "content-summary-generator/package-lock.json"
            ),
            handler="handler",
            timeout=Duration.seconds(30),
            log_retention=logs.RetentionDays.ONE_WEEK,
        )
        summary_lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel",
                ],
                resources=[
                    "arn:aws:bedrock:*::foundation-model/amazon.titan-text-express-v1",
                ],
            )
        )

        # Word cloud generator Lambda function, written in Java
        java_packaging_instructions = [
            "/bin/sh",
            "-c",
            "mvn clean install "
            + "&& cp /asset-input/target/word-cloud-generator-1.0.jar /asset-output/",
        ]

        java_bundling_options = BundlingOptions(
            command=java_packaging_instructions,
            image=_lambda.Runtime.JAVA_8_CORRETTO.bundling_image,
            user="root",
            output_type=BundlingOutput.ARCHIVED,
        )

        word_cloud_lambda_function = _lambda.Function(
            self,
            "WordCloudGenerator",
            runtime=_lambda.Runtime.JAVA_8_CORRETTO,
            code=_lambda.Code.from_asset(
                path.join(function_code_dir, "word-cloud-generator"),
                bundling=java_bundling_options,
            ),
            handler="wordcloud.WordCloudGenerator",
            memory_size=1024,
            timeout=Duration.seconds(30),
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        backend_apis = apigw.RestApi(
            self,
            "SummarizeMyDocBackendAPIs",
            description="Backend APIs for Summarize My Doc",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ),
            
        )

        summary_api = backend_apis.root.add_resource("content-summary-generator")
        summary_api.add_method(
            "POST",
            apigw.LambdaIntegration(summary_lambda_function),
            authorization_type=apigw.AuthorizationType.IAM,
        )

        word_cloud_api = backend_apis.root.add_resource("word-cloud-generator")
        word_cloud_api.add_method(
            "POST",
            apigw.LambdaIntegration(word_cloud_lambda_function),
            authorization_type=apigw.AuthorizationType.IAM,
        )
