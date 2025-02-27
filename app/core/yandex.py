from yandex_cloud_ml_sdk import YCloudML
from app.core.config import YANDEX_API_KEY, YANDEX_FOLDER_ID

sdk = YCloudML(
    folder_id=YANDEX_FOLDER_ID,
    auth=YANDEX_API_KEY,
)