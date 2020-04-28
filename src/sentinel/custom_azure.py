from storages.backends.azure_storage import AzureStorage
from django.conf import settings


class AzureMediaStorage(AzureStorage):
    account_name = settings.AZURE_STORAGE_ACCOUNT
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.AZURE_MEDIA_CONTAINER
    expiration_secs = None


# class AzureStaticStorage(AzureStorage):
#     account_name = settings.AZURE_STORAGE_ACCOUNT
#     account_key = settings.AZURE_ACCOUNT_KEY
#     azure_container = settings.AZURE_STATIC_CONTAINER
#     expiration_secs = None