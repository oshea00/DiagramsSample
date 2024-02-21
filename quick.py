# diagram example
# https://diagrams.mingrammer.com/docs/guides/diagram

from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb, ElastiCache
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

