from bson import json_util
import json
import os

from dotenv import load_dotenv
from mongo.auth import Client as MongoClient
from pymongo import errors
from zoom.auth import Client as ZoomClient
from zoom.reports import (
    historical_detail_report,
    historical_queue_report,
    ENGAGEMENT_TYPES,
)

load_dotenv()
ZOOM_ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID")
ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
MONGO_USERNAME = os.getenv("MONGO_DB_UN")
MONGO_PASSWORD = os.getenv("MONGO_DB_PW")
MONGO_DATABASE = os.getenv("MONGO_DB_NAME")


def mongo_upload_queue_report(client: MongoClient, data: list[dict]) -> None:
    client.databases["queue_report_voice"].collection.insert_many(data)


def mongo_upload_detail_report(client: MongoClient, data: list[dict]) -> None:
    try:
        for engagement_type, database in client.databases.items():
            database.collection.insert_many(data[engagement_type])
    except errors.BulkWriteError as err:
        print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))


def main() -> None:
    # mongo_client = MongoClient(MONGO_USERNAME, MONGO_PASSWORD, MONGO_DATABASE)
    zoom_client = ZoomClient(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, ZOOM_ACCOUNT_ID)
    zoom_client.get_token()

    detail_report_data = {}
    queue_report_data = {}

    for engagement_type in ENGAGEMENT_TYPES:
        detail_report_data[engagement_type] = historical_detail_report(
            zoom_client, engagement_type
        )
        queue_report_data[engagement_type] = historical_queue_report(
            zoom_client, engagement_type, "1_day"
        )

    print(detail_report_data)
    print(queue_report_data)


if __name__ == "__main__":
    main()
