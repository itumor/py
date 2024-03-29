from logger import *
import boto3
from botocore.config import Config
import json

my_config = Config(
    # Optionally lets you specify a region other than your default.
    region_name='eu-central-1'
)


sc_client = boto3.client('servicecatalog')
secrets_manager_client = boto3.client('secretsmanager')

# Open Search Conn function
def GetDomain_Endpoint(ProvisionedProductId):
    response = sc_client.get_provisioned_product_outputs(
    ProvisionedProductId = ProvisionedProductId
    )
    Domain_Endpoint = next(filter(lambda x: x['OutputKey'] == 'DomainEndpoint', response['Outputs']), None)
    ##logger.info(Domain_Endpoint['OutputValue'])
    return(Domain_Endpoint['OutputValue'])

def GetDomain_username(ProvisionedProductId):
    response = sc_client.get_provisioned_product_outputs(
    ProvisionedProductId = ProvisionedProductId
    )
    DomainMasterSecret = next(filter(lambda x: x['OutputKey'] == 'DomainMasterSecret', response['Outputs']), None)
    #logger.info(DomainMasterSecret['OutputValue'])
    
    
    secret_response = secrets_manager_client.get_secret_value(
                SecretId=DomainMasterSecret['OutputValue']
            )
    
    secret = json.loads(secret_response['SecretString'])
    #logger.info(secret['username'])
    return(secret['username'])

def GetDomain_password(ProvisionedProductId):
    response = sc_client.get_provisioned_product_outputs(
    ProvisionedProductId = ProvisionedProductId
    )
    DomainMasterSecret = next(filter(lambda x: x['OutputKey'] == 'DomainMasterSecret', response['Outputs']), None)
    #logger.info(DomainMasterSecret['OutputValue'])
    
    
    secret_response = secrets_manager_client.get_secret_value(
                SecretId=DomainMasterSecret['OutputValue']
            )
    
    secret = json.loads(secret_response['SecretString'])
    #logger.info(secret['password'])
    return(secret['password'])

def GetDomain_Domain_name(ProvisionedProductId):
    response = sc_client.get_provisioned_product_outputs(
    ProvisionedProductId = ProvisionedProductId
    )
    OpenSearchArn = next(filter(lambda x: x['OutputKey'] == 'OpenSearchArn', response['Outputs']), None)
    #logger.info(OpenSearchArn['OutputValue'])
    
    OpenSearch_Arn=OpenSearchArn['OutputValue']
    Domain_name=OpenSearch_Arn.split("domain/",1)[1]
    #logger.info(OpenSearch_Arn.split("domain/",1)[1])
    return(Domain_name)

def GetDomain_EngineVersion(Domain_name):
    awsclient = boto3.client('opensearch', config=my_config)

    # Describe The Domain.
    response = awsclient.describe_domain(
        DomainName=Domain_name
       # ARN='arn:aws:es:eu-central-1:600027353764:domain/pcgtpjpuinupryhuhdng'
    )
    
    #logger.info('\Describe Domain:')
    #logger.info(response['DomainStatus']['EngineVersion'])
    return(response['DomainStatus']['EngineVersion'])


def GetDomain_InstanceCount(Domain_name):
    awsclient = boto3.client('opensearch', config=my_config)
    response = awsclient.describe_domain_config(
        DomainName=Domain_name
    )
    
    #logger.info('\Describe Domain Config:')
    #logger.info(response['DomainConfig']['ClusterConfig']['Options']['InstanceCount'])
    return(response['DomainConfig']['ClusterConfig']['Options']['InstanceCount'])