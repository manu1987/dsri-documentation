import datetime
import logging

from api.config import settings
from kubernetes import client
from openshift.dynamic import DynamicClient
from openshift.helper.userpassauth import OCPLoginConfiguration

## Instantiate logging utility
log = logging.getLogger()
log.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: [%(module)s:%(funcName)s] %(message)s"
)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

## You can also ask more details like line number:
# "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
## You can also export logs to a file
# fh = logging.FileHandler(filename='./server.log')
# fh.setFormatter(formatter)
# logger.addHandler(fh)


## Login to the OpenShift cluster using https://github.com/openshift/openshift-restclient-python
def oc_login():
    """Login to the OpenShift cluster"""
    # os.system(f"oc login {settings.CLUSTER_URL} --insecure-skip-tls-verify -u {settings.CLUSTER_USER} -p {settings.CLUSTER_PASSWORD}")
    kubeConfig = OCPLoginConfiguration(
        ocp_username=settings.CLUSTER_USER,
        ocp_password=settings.CLUSTER_PASSWORD
    )
    kubeConfig.host = settings.CLUSTER_URL
    kubeConfig.verify_ssl = False
    # kubeConfig.ssl_ca_cert = '/app/dsri.pem' # use a certificate bundle for the TLS validation

    # Retrieve the auth token
    kubeConfig.get_token()
    # print('Auth token: {0}'.format(kubeConfig.api_key))
    # print('Token expires: {0}'.format(kubeConfig.api_key_expires))

    k8s_client = client.ApiClient(kubeConfig)
    dyn_client = DynamicClient(k8s_client)

    return dyn_client, k8s_client, kubeConfig
