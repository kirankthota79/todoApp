from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_dynamodb as _dynamodb,
    aws_lambda as _lambda,
    CfnOutput
)
from constructs import Construct
# from 


class TodoInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        """ Creating Dynamodb Table to store the Tasks """
        
        table = _dynamodb.Table(self, id="MydynamodbTable", table_name="Tasks", 
                               partition_key=_dynamodb.Attribute(
                                   name="task_id",
                                   type= _dynamodb.AttributeType.STRING
                                   ), 
                               billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
                               time_to_live_attribute="ttl"
                               )
        """ Adding Global Secondary Index based on User_id """
        
        table.add_global_secondary_index(
            index_name="user-index",
            partition_key= _dynamodb.Attribute(
                name="user_id",
                type= _dynamodb.AttributeType.STRING
            ),
            sort_key= _dynamodb.Attribute(
                name="created_time",
                type=_dynamodb.AttributeType.NUMBER
            )
        )
        
        """ Creating Lambda Function for the API"""
        
        api = _lambda.Function(self, id="myApiLamdbad",
                               runtime=_lambda.Runtime.PYTHON_3_10,
                               handler="todo.handler",
                               code = _lambda.Code.from_asset("api/my_deployment_package.zip"),
                               environment={
                                   "TABLE_NAME": table.table_name
                               }
                               )
        
        """ Create a URL so we can access the Function  """
        
        api_url = api.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors=_lambda.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_headers=["*"],
                allowed_methods=[_lambda.HttpMethod.ALL]
            )
        )
        
        """ Print URL to console using cfn output"""
        CfnOutput(self,"ApiUrl",
                  value= api_url.url
                  )
        
        table.grant_read_write_data(api)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "TodoInfraQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
