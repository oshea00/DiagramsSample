import boto3
#import pandas as pd

# Create a session using your AWS credentials
session = boto3.Session()


def listEc2():
    # Create an EC2 resource object using the session
    ec2_resource = session.resource('ec2')

    # Use the filter method to get running instances
    ec2instances = ec2_resource.instances.filter(
        Filters=[
            {
                # 'Name': 'tag:Name',
                # 'Values': ['True']
                # 'Name': 'instance-state-name',
                # 'Values': ['running']
            }
        ]
    )


    # Print the instance IDs
    for instance in ec2instances:
        name_tag = next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), None)
        print('ID: {}, Name: {}, State: {}, Type: {}'.format(instance.id, name_tag, instance.state['Name'], instance.instance_type))

def lists3():
    # List s3 buckets    
    # Create an S3 client
    s3 = session.client('s3')

    # Call to S3 to list current buckets
    response = s3.list_buckets()

    # Get a list of all bucket names from the response
    s3buckets = [bucket['Name'] for bucket in response['Buckets']]

    # Print out the bucket list
    for bucket in s3buckets:
        print(f'{bucket}')

def listDomainAPIs():
    # Create an API Gateway V2 client
    apigatewayv2 = session.client('apigatewayv2')
    apigateway = session.client('apigateway')

    # Call to API Gateway to list current domain names
    response = apigatewayv2.get_domain_names()

    # Get a list of all domain names from the response
    domain_names = [domain['DomainName'] for domain in response['Items']]

    # Get apis
    get_apis_response = apigateway.get_rest_apis()
    apis = {}
    for api in get_apis_response['items']:
        apis[api['id']] = api['name']

    # Print out the domain names list
    for domain in domain_names:
        print(f'Domain: {domain}')
        # Get API mappings for the domain
        api_mappings_response = apigatewayv2.get_api_mappings(DomainName=domain)
        # Get a list of all API mappings from the response
        api_mappings = [mapping['ApiMappingId'] for mapping in api_mappings_response['Items']]
        # Print out the API mappings list
        for mapping in api_mappings:
            # Get the API mapping
            api_mapping_response = apigatewayv2.get_api_mapping(DomainName=domain, ApiMappingId=mapping)
            #print(api_mapping_response)
            # Get the API ID from the response
            api_name = apis[api_mapping_response['ApiId']] if api_mapping_response['ApiId'] in apis else 'NotFound'
            # Print out the API details
            print(f'    API ID: {api_mapping_response["ApiId"]}, API Name: {api_name}')

listEc2()
lists3()
listDomainAPIs()
