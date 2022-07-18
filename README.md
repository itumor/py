# opensearch Regression tests

Check that python 3.10 is installed on your system.

## Create & setup virtual env

* sudo yum -y update 
* sudo amazon-linux-extras install python3.8

* move to dir  `cd /home/ec2-user/environment/env/py`

* Create virtualenv: `virtualenv -p /usr/bin/python3.8  venv`
 

* Active virtualenv: `source venv/bin/activate`

* Install distutils `sudo apt-get install python3.8-distutils`

* Install needed pacakges: `pip3 install -r requirements.txt`

## Prepare taskCat

* Create a `.taskcat.yml` file in your home directory (e.g `touch ~/.taskcat.yml`)

The following properties are needed in the created file:

```
general:
  auth:
    default: "<aws cli profile to be used>"
  s3_bucket: <bucket-name-where-documents-are-uploaded>
```

## KMS Key

A specially created KMS key for regression testing is automatically used. This key will be created when the account is flagged as regression testing capable.

The key has the following alias: `alias/sc/${AWS::AccountId}/regression-testing`

# Run the tests

Execute `python3 test.py`

The results will be in the log file. A web view can be found in the `out/` directory.

#taskcat 

taskcat test run -n


