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
AZURE_ACCOUNT_KEY = client.get_secret('SENTINEL-AZURE-ACCOUNT_KEY').value
AZURE_CUSTOM_DOMAIN = client.get_secret('SENTINEL-AZURE-ACCOUNT-KEY').value
AZURE_MEDIA_CONTAINER = client.get_secret('SENTINEL-AZURE-MEDIA-CONTAINER').value
# AZURE_STATIC_CONTAINER = client.get_secret('SENTINEL-AZURE-STATIC-CONTAINER').value

### Azure service bus
AZURE_SB_CONN_STRING = client.get_secret('SENTINEL-AZURE-SB_CONN-STRING').value
# AZURE_SB_CANCEL_QUEUE = client.get_secret('SENTINEL-AZURE-SB-CANCEL-QUEUE').value


### Azure AD Services
TENANT_ID = client.get_secret('SENTINEL-AZURE-TENANT-ID').value
CLIENT_ID = client.get_secret('SENTINEL-AZURE-CLIENT-ID').value
RELYING_PARTY_ID = client.get_secret('SENTINEL-AZURE-RELYING-PARTY-ID').value
AUDIENCE = client.get_secret('SENTINEL-AZURE-AUDIENCE').value


##

# SENTINEL-DJANGO-SETTINGS-MODULE = "sentinel.settings",
# SENTINEL-CELERY-BROKER-URL = "redis://:bXdrR76xUo5bAV4EBk4LCH3LNWVIkPe6ZKH3SWyiLB0=@cardinal-us-alpha-prod-redis-emerald-black-alpha.redis.cache.windows.net:6380/2",
# SENTINEL-AZURE-STORAGE-ACCOUNT = "83b4a135d5e74f069a8f0d7",
# SENTINEL-AZURE-ACCOUNT-KEY = "3N+SB3fC5RK6hZPzPUE/mb3Xmt8+lG0WajxMtUCOZZ+m62I595efcQAjD2dpR1suqlJGJGX7hUdRDd6DP0Nk3Q==",
# SENTINEL-AZURE-CUSTOM-DOMAIN = "83b4a135d5e74f069a8f0d7.blob.core.windows.net",
# SENTINEL-AZURE-SB-CONN-STRING = "Endpoint=sb://prdmonarchservicebus.servicebus.windows.net/;SharedAccessKeyName=OPSAutomation;SharedAccessKey=EHIvPR82aj/HoRweVcMeBcTydHBooq4Z0zYf8IBtsak=;EntityPath=cancelledorders",
# SENTINEL-AZURE-SB-CANCEL-QUEUE = "CancelledOrders",
# SENTINEL-DATABASE-NAME = "sentinel-email-parser-management",
# SENTINEL-DATABASE-USERNAME = "sentinel_email_parser_readwrite@cardinal-us-alpha-prod-db-emerald-black-alphadbsvr",
# SENTINEL-DATABASE-PASSWORD = "FCEbY4.=",
# SENTINEL-DATABASE-HOST = "cardinal-us-alpha-prod-db-emerald-black-alphadbsvr.postgres.database.azure.com"
# SENTINEL-AZURE-MEDIA-CONTAINER = 'media'