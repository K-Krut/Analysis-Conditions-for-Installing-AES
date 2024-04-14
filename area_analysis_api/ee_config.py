import ee
from diploma_api import settings

EE_CREDENTIALS = ee.ServiceAccountCredentials(email=settings.EE_ACCOUNT, key_file=settings.EE_PRIVATE_KEY_FILE)
