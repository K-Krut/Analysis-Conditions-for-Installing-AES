import ee
from diploma_api import settings


FILE_PATH = str(settings.BASE_DIR / 'area_analysis_api' / settings.EE_PRIVATE_KEY_FILE)
EE_CREDENTIALS = ee.ServiceAccountCredentials(email=settings.EE_ACCOUNT, key_file=FILE_PATH)
