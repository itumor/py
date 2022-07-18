from opensearchpy import OpenSearch, RequestsHttpConnection
from logger import *

# Open Search Conn function
def OpenSearchConn(host,region,user,password):
    print(host)
    print(region)
    print(user)
    print(password)
    auth = (user, password)
    print (auth)
    
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
    logger.info('Creating index:')
    logger.info(response)
    
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
    
    logger.info('Adding document:')
    logger.info(response)
    
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
    logger.info('Search results:')
    logger.info(response)
    
    # Delete the document.
    response = client.delete(
        index = index_name,
        id = id
    )
    
    logger.info('Deleting document:')
    logger.info(response)
    
    # Delete the index.
    idx_list = [x for x in client.indices.get_alias("*").keys() ]
    logger.info('List index:')
    logger.info(idx_list)
    
    delete_index= client.indices.delete(index=index_name, ignore=[400, 404])
    logger.info('Delete index:')
    logger.info(delete_index)
    
    idx_list = [x for x in client.indices.get_alias("*").keys() ]
    logger.info('List index:')
    logger.info(idx_list)
    
