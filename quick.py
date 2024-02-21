# diagram.py
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, Dynamodb, ElastiCache
from diagrams.aws.network import ELB
from diagrams.aws.integration import StepFunctions
from diagrams.azure.database import SQLDatabases
from diagrams.programming.framework import GraphQL

with Diagram("PCW Data Integration", show=False):
    radius = GraphQL("Radius APIs")
    onpremSql = SQLDatabases("On-Prem SQL")

    with Cluster("Map"):
        staticdata = Lambda("Lookup Data")
        lambdadata = [
            Lambda("Account Data"),
            Lambda("Benchmark Data"),
            Lambda("Accounts"),
            staticdata]

    getdata = StepFunctions("Get Data")
    radius >> getdata
    onpremSql >> getdata
    getdata >> lambdadata
    staticdata >> ElastiCache("Redis")

    createSession = Lambda("Create Session")
    integration = Dynamodb("Integration Cache")
    lambdadata >> integration 

    onpremSql >> createSession
    integration >> createSession
    integration >> Lambda("PCW Account List")


# list the members of the diagrams.aws.compute module
# print(dir(diagrams.aws.compute))
# ['ASG', 'AutoScaling', 'EC2', 'ECS', 'EKS', 'Lambda', 'LightSail', 'VM']
# list the members of the diagrams.aws.database module
# print(dir(diagrams.aws.database))
# ['DynamoDB', 'ElasticCache', 'Neptune', 'RDS', 'Redshift']
# list the members of the diagrams.aws.network module
# print(dir(diagrams.aws.network))
# ['APIGateway', 'CloudFront', 'CloudMap', 'DirectConnect', 'ELB', 'GlobalAccelerator', 'Route53', 'VPC', 'VPCPeering', 'VPCPrivate', 'VPCPublic']

# list the members of the diagrams.aws module
# print(dir(diagrams.aws))
# ['analytics', 'applicationintegration', 'compute', 'database', 'developer', 'enduser', 
#'engagement', 'iot', 'management', 'media', 'migration', 'mobile', 'network', 'security', 'storage', 'web']

# Use boto3 to list the APIs in APIGateway
# import boto3
# client = boto3.client('apigateway')
# response = client.get_rest_apis()
# for item in response['items']:
#     print(item['name'])

# Use boto3 to list the APIs in EC2 that have a specific tag WEB
# import boto3
# client = boto3.client('ec2')
# response = client.describe_instances(

