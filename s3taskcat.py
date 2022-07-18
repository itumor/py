from taskcat.testing import CFNTest
from taskcat._tui import TerminalPrinter
from datetime import datetime
import logging
import boto3
from botocore.config import Config
import pymongo
import urllib.parse
import botocore
import time
import json
from typing import List, Set, Tuple
from opensearchpy import OpenSearch, RequestsHttpConnection
from OpenSearch import *
from logger import *
from ServiceCatalogConfig import *


##opencase

#host = 'vpc-pcgtpjpuinupryhuhdng-jbmrtspwc3qe6oilrue4cwxcqq.eu-central-1.es.amazonaws.com' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'eu-central-1' # e.g. us-west-1
Endpoint=GetDomain_Endpoint('pp-aywt5clfexwze')
logger.info(Endpoint)
username= GetDomain_username('pp-aywt5clfexwze')
logger.info(username)
password= GetDomain_password('pp-aywt5clfexwze')
logger.info(password)

OpenSearchConn(Endpoint,region,username,password)

##opencase

###case
Domain_name=GetDomain_Domain_name('pp-aywt5clfexwze')
logger.info(Domain_name)




my_config = Config(
    # Optionally lets you specify a region other than your default.
    region_name='eu-central-1'
)


sc_client = boto3.client('servicecatalog')
secrets_manager_client = boto3.client('secretsmanager')


##response = sc_client.get_provisioned_product_outputs(

##ProvisionedProductName = 'iaws-opensearch'
##)
response = sc_client.get_provisioned_product_outputs(
ProvisionedProductId = 'pp-aywt5clfexwze'
)



#outputs = sc_client.get_provisioned_product_outputs(
#    ProvisionedProductName = 'prod-zdpipcxs7ekou' 
#)


logger.info(response['Outputs'])

OpenSearchArn = next(filter(lambda x: x['OutputKey'] == 'OpenSearchArn', response['Outputs']), None)
logger.info(OpenSearchArn['OutputValue'])

OpenSearch_Arn=OpenSearchArn['OutputValue']
Domain_name=OpenSearch_Arn.split("domain/",1)[1]
logger.info(OpenSearch_Arn.split("domain/",1)[1])

Domain_Endpoint = next(filter(lambda x: x['OutputKey'] == 'DomainEndpoint', response['Outputs']), None)
logger.info(Domain_Endpoint['OutputValue'])

DomainMasterSecret = next(filter(lambda x: x['OutputKey'] == 'DomainMasterSecret', response['Outputs']), None)
logger.info(DomainMasterSecret['OutputValue'])


secret_response = secrets_manager_client.get_secret_value(
            SecretId=DomainMasterSecret['OutputValue']
        )

secret = json.loads(secret_response['SecretString'])
logger.info(secret['password'])
logger.info(secret['username'])



#domain_name='pcgtpjpuinupryhuhdng'

awsclient = boto3.client('opensearch', config=my_config)

# Describe The Domain.
response = awsclient.describe_domain(
    DomainName=Domain_name
   # ARN='arn:aws:es:eu-central-1:600027353764:domain/pcgtpjpuinupryhuhdng'
)


logger.info('\Describe Domain:')
logger.info(response['DomainStatus']['EngineVersion'])



response = awsclient.describe_domain_config(
    DomainName=Domain_name
)

logger.info('\Describe Domain Config:')
logger.info(response['DomainConfig']['ClusterConfig']['Options']['InstanceCount'])

a = 2
b = response['DomainConfig']['ClusterConfig']['Options']['InstanceCount']
if b == a:
  logger.info("True")
else:
  logger.info("False")




###case

#test = CFNTest.from_file(project_root='.', input_file='taskcatop.yml')
#with test as stacks:
    # Calling 'with' or 'test.run()' will deploy the stacks.
#    for stack in stacks:
#        logger.info(f"Testing {stack.name}")
#        bucket_name = ""
#        for output in stack.outputs:
#            if output.key == "ScItemId":
#                bucket_name = output.value
#                logger.info(bucket_name)
#                break
        #assert "logs" in bucket_name
        #assert stack.region.name in bucket_name
       # logger.info(f"Created bucket: {bucket_name}")
        #test.run()

       
