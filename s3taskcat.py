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

test = CFNTest.from_file(project_root='.', input_file='taskcatop.yml')


# create logger
logger = logging.getLogger('simple_example')
#logger.setLevel(logging.INFO)
#logging.basicConfig(filename='example.log')
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d_%H%M%S")

logging.basicConfig(filename='testcat-{}.log'.format(dt_string), level=logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
#logger.debug('debug message')
#logger.info('info message')
#logger.warning('warn message')
#logger.error('error message')
#logger.critical('critical message')

logger.info(test)

##opencase
host = 'vpc-pcgtpjpuinupryhuhdng-jbmrtspwc3qe6oilrue4cwxcqq.eu-central-1.es.amazonaws.com' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'eu-central-1' # e.g. us-west-1

credentials = boto3.Session().get_credentials()
#auth = AWSV4SignerAuth(credentials, region)
auth = ('master-user', 'RybfCQn!R1iHmB-^&.8q<1!DjTeDPgH_')
#index_name = 'movies'

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

# Create an index with non-default settings.
index_name = 'python-test-index'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(index_name, body=index_body)
print('\nCreating index:')
print(response)

# Add a document to the index.
document = {
  'title': 'Moneyball',
  'director': 'Bennett Miller',
  'year': '2011'
}
id = '1'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
)

print('\nAdding document:')
print(response)

# Search for the document.
q = 'miller'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['title^2', 'director']
    }
  }
}

response = client.search(
    body = query,
    index = index_name
)
print('\nSearch results:')
print(response)

# Delete the document.
response = client.delete(
    index = index_name,
    id = id
)

print('\nDeleting document:')
print(response)

# Delete the index.
idx_list = [x for x in client.indices.get_alias("*").keys() ]
print('\nList index:')
print(idx_list)

delete_index= client.indices.delete(index=index_name, ignore=[400, 404])
print('\nDelete index:')
print(delete_index)

idx_list = [x for x in client.indices.get_alias("*").keys() ]
print('\nList index:')
print(idx_list)


##opencase


###case



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


print(response['Outputs'])

OpenSearchArn = next(filter(lambda x: x['OutputKey'] == 'OpenSearchArn', response['Outputs']), None)
print(OpenSearchArn['OutputValue'])

OpenSearch_Arn=OpenSearchArn['OutputValue']
Domain_name=OpenSearch_Arn.split("domain/",1)[1]
print(OpenSearch_Arn.split("domain/",1)[1])

Domain_Endpoint = next(filter(lambda x: x['OutputKey'] == 'DomainEndpoint', response['Outputs']), None)
print(Domain_Endpoint['OutputValue'])

DomainMasterSecret = next(filter(lambda x: x['OutputKey'] == 'DomainMasterSecret', response['Outputs']), None)
print(DomainMasterSecret['OutputValue'])


secret_response = secrets_manager_client.get_secret_value(
            SecretId=DomainMasterSecret['OutputValue']
        )

secret = json.loads(secret_response['SecretString'])
print (secret['password'])
print (secret['username'])



#domain_name='pcgtpjpuinupryhuhdng'

awsclient = boto3.client('opensearch', config=my_config)

# Describe The Domain.
response = awsclient.describe_domain(
    DomainName=Domain_name
   # ARN='arn:aws:es:eu-central-1:600027353764:domain/pcgtpjpuinupryhuhdng'
)


print('\Describe Domain:')
print(response['DomainStatus']['EngineVersion'])



response = awsclient.describe_domain_config(
    DomainName=Domain_name
)

print('\Describe Domain Config:')
print(response['DomainConfig']['ClusterConfig']['Options']['InstanceCount'])

a = 2
b = response['DomainConfig']['ClusterConfig']['Options']['InstanceCount']
if b == a:
  print("True")
else:
  print("False")




###case


with test as stacks:
    # Calling 'with' or 'test.run()' will deploy the stacks.
    for stack in stacks:
        print(f"Testing {stack.name}")
        bucket_name = ""
        for output in stack.outputs:
            if output.key == "ScItemId":
                bucket_name = output.value
                logger.info(bucket_name)
                break
        #assert "logs" in bucket_name
        #assert stack.region.name in bucket_name
       # print(f"Created bucket: {bucket_name}")
        #test.run()

       
