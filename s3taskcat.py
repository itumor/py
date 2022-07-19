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




region = 'eu-central-1' # e.g. us-west-1
def OpenSearchConnTest(ProvisionedProductId):
    Endpoint=GetDomain_Endpoint(ProvisionedProductId)
    logger.info(Endpoint)
    username= GetDomain_username(ProvisionedProductId)
    logger.info(username)
    password= GetDomain_password(ProvisionedProductId)
    logger.info(password)
    assert OpenSearchConn(Endpoint,region,username,password) == True,"issue was the OpenSearch connection"




def TestCase(ProvisionedProductId):
    Domain_name=GetDomain_Domain_name(ProvisionedProductId)
    logger.info(Domain_name)
    EngineVersion=GetDomain_EngineVersion(Domain_name)
    logger.info(EngineVersion)
    assert EngineVersion == 'OpenSearch_1.2' ,"issue was the Engine Version"
    InstanceCount=GetDomain_InstanceCount(Domain_name)
    logger.info(InstanceCount)
    assert InstanceCount == 2 ,"issue was the number of Instance"
    
    a = 2
    b = InstanceCount
    if b == a:
      logger.info("True")
    else:
      logger.info("False")


output_directory='./out'

test = CFNTest.from_file(project_root='.', input_file='taskcatop.yml')
logger.info("Starting")
with test as stacks:
    test.report(output_directory)
        
    for stack in stacks:
        for output in stack.outputs:
            if output.key == "ScItemId":
                service_catalog_provided_item_id = output.value
        if stack.name.startswith('tCaT-iaws-product-opensearch-opensearch4Instances'):  
                logger.info(f"Testing {stack.name}")
                OpenSearchConnTest(service_catalog_provided_item_id)
                TestCase(service_catalog_provided_item_id)
                logger.info(f"Testing {stack.name} done!")
        if stack.name.startswith('tCaT-iaws-product-opensearch-opensearch2Instances'):
                logger.info(f"Testing {stack.name}")
                OpenSearchConnTest(service_catalog_provided_item_id)
                TestCase(service_catalog_provided_item_id)
                logger.info(f"Testing {stack.name} done!")
logger.info('done')