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

# Load environment variables from local .env file
load_dotenv()
ZOOM_ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID")
ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
MONGO_USERNAME = os.getenv("MONGO_DB_UN")
MONGO_PASSWORD = os.getenv("MONGO_DB_PW")
MONGO_DATABASE = os.getenv("MONGO_DB_NAME")


def mongo_upload_queue_report(client: MongoClient, data: list[dict]) -> None:
    if "voice" in data:
        try:
            client.databases["queue_report_voice"].collection.insert_many(data["voice"])
        except errors.BulkWriteError as err:
            print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))
    if "video" in data:
        try:
            client.databases["queue_report_video"].collection.insert_many(data["video"])
        except errors.BulkWriteError as err:
            print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))
    if "chat" in data:
        try:
            client.databases["queue_report_chat"].collection.insert_many(data["chat"])
        except errors.BulkWriteError as err:
            print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))
    if "sms" in data:
        try:
            client.databases["queue_report_sms"].collection.insert_many(data["sms"])
        except errors.BulkWriteError as err:
            print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))


def mongo_upload_detail_report(client: MongoClient, data: list[dict]) -> None:

    if "voice" in data:
        try:
            client.databases["queue_detail_voice"].collection.insert_many(data["voice"])
        except errors.BulkWriteError as err:
            print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))
    if "video" in data:
        try:
            client.databases["queue_detail_video"].collection.insert_many(data["video"])
        except errors.BulkWriteError as err:
            print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))
    if "chat" in data:
        try:
            client.databases["queue_detail_chat"].collection.insert_many(data["chat"])
        except errors.BulkWriteError as err:
            print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))
    if "sms" in data:
        try:
            client.databases["queue_detail_sms"].collection.insert_many(data["sms"])
        except errors.BulkWriteError as err:
            print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))
    # try:
    #     for engagement_type, database in client.databases.items():
    #         database.collection.insert_many(data[engagement_type])
    # except errors.BulkWriteError as err:
    #     print(json.dumps(json.loads(json_util.dumps(err.details)), indent=4))


def main() -> None:

    date_range = ("2023-11-01", "2023-11-30")  # From:To date range to download via Zoom API
    mongo_client = MongoClient(MONGO_USERNAME, MONGO_PASSWORD, MONGO_DATABASE)
    zoom_client = ZoomClient(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, ZOOM_ACCOUNT_ID)
    zoom_client.get_token()

    detail_report_data = {}
    queue_report_data = {}

    for engagement_type in ENGAGEMENT_TYPES:
        detail_report_data[engagement_type] = historical_detail_report(
            zoom_client, engagement_type, date_range
        )
        queue_report_data[engagement_type] = historical_queue_report(
            zoom_client, engagement_type, "1_day", date_range
        )

    for engagement_type in ENGAGEMENT_TYPES:
        if not detail_report_data[engagement_type]:
            del detail_report_data[engagement_type]

        if not queue_report_data[engagement_type]:
            del queue_report_data[engagement_type]

    # print(json.dumps(detail_report_data, indent=4))
    # print(json.dumps(queue_report_data, indent=4))

    mongo_upload_detail_report(mongo_client, detail_report_data)
    mongo_upload_queue_report(mongo_client, queue_report_data)


if __name__ == "__main__":
    main()
