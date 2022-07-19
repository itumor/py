import logging
from datetime import datetime

# create logger
logger = logging.getLogger('taskcat_opensearch')
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d_%H%M%S")
logging.basicConfig(filename='testcat-{}.log'.format(dt_string), level=logging.INFO)

# create console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

#test the logger
logger.info('log_test_start')
