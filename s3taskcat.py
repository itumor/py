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



EngineVersion=GetDomain_EngineVersion(Domain_name)
logger.info(EngineVersion)



InstanceCount=GetDomain_InstanceCount(Domain_name)
logger.info(InstanceCount)



a = 2
b = InstanceCount
if b == a:
  logger.info("True")
else:
  logger.info("False")




###case

test = CFNTest.from_file(project_root='.', input_file='taskcatop.yml')
with test as stacks:
    # Calling 'with' or 'test.run()' will deploy the stacks.
    for stack in stacks:
        logger.info(f"Testing {stack.name}")
        bucket_name = ""
        for output in stack.outputs:
            if output.key == "ScItemId":
                bucket_name = output.value
                logger.info(bucket_name)
#                break
        #assert "logs" in bucket_name
        #assert stack.region.name in bucket_name
       # logger.info(f"Created bucket: {bucket_name}")
        #test.run()

       
