import os

AZURE_VAULT_URL = os.getenv('AZURE_VAULT_URL')

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
client = SecretClient(
    vault_url=AZURE_VAULT_URL,  credential=credential)

### Database configuration
SENTINEL_DATABASE_NAME = client.get_secret('SENTINEL-DATABASE-NAME').value
SENTINEL_DATABASE_USERNAME = client.get_secret('SENTINEL-DATABASE-USERNAME').value
SENTINEL_DATABASE_PASSWORD = client.get_secret('SENTINEL-DATABASE-PASSWORD').value
SENTINEL_DATABASE_HOST = client.get_secret('SENTINEL-DATABASE-HOST').value

## celery
CELERY_BROKER_URL = client.get_secret('SENTINEL-CELERY-BROKER-URL').value


### Azure storage account
AZURE_STORAGE_ACCOUNT = client.get_secret('SENTINEL-AZURE-STORAGE-ACCOUNT').value
AZURE_ACCOUNT_KEY = client.get_secret('SENTINEL-AZURE-ACCOUNT-KEY').value
AZURE_CUSTOM_DOMAIN = client.get_secret('SENTINEL-AZURE-ACCOUNT-KEY').value
AZURE_MEDIA_CONTAINER = client.get_secret('SENTINEL-AZURE-MEDIA-CONTAINER').value
# AZURE_STATIC_CONTAINER = client.get_secret('SENTINEL-AZURE-STATIC-CONTAINER').value

### Azure service bus
AZURE_SB_CONN_STRING = client.get_secret('SENTINEL-AZURE-SB-CONN-STRING').value
# AZURE_SB_CANCEL_QUEUE = client.get_secret('SENTINEL-AZURE-SB-CANCEL-QUEUE').value


### Azure AD Services
# TENANT_ID = client.get_secret('SENTINEL-AZURE-TENANT-ID').value
# CLIENT_ID = client.get_secret('SENTINEL-AZURE-CLIENT-ID').value
# RELYING_PARTY_ID = client.get_secret('SENTINEL-AZURE-RELYING-PARTY-ID').value
# AUDIENCE = client.get_secret('SENTINEL-AZURE-AUDIENCE').value