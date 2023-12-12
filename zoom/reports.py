import logging

import requests
from zoom.auth import Client

# Configure logging
logging.basicConfig(
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level=logging.INFO,
)

# Establish a set of valid Engagement Types and Intervals
ENGAGEMENT_TYPES = ["voice", "video", "chat", "sms"]
INTERVALS = ["15_minutes", "30_minutes", "1_hour", "1_day", "1_week", "1_month"]


def historical_detail_report(client: Client, engagement_type: str, date_range: tuple) -> list[dict]:
    if engagement_type not in ENGAGEMENT_TYPES:
        raise ValueError("Please check your engagement type.")
    output = []
    endpoint = f"{client.base_url}/contact_center/analytics/historical/details/metrics"
    headers = {"Authorization": f"Bearer {client.token}"}
    params = {
        "next_page_token": "",
        "page_size": 100,
        "channel_types": [engagement_type],
        "from": date_range[0],
        "to": date_range[1],
    }
    while True:
        try:
            if client.token_has_expired:
                logging.debug("Bearer token has expired, generating a new one...")
                client.get_token()
                headers["Authorization"] = f"Bearer {client.token}"
            r = requests.get(endpoint, headers=headers, params=params)
            r.raise_for_status()
            response = r.json()
            if "details" in response:
                output.extend(response["details"])
            params["next_page_token"] = response["next_page_token"]
            if not params["next_page_token"]:
                break
        except requests.HTTPError as err:
            logging.error(err)
            exit(1)
    return output


def historical_queue_report(
    client: Client, engagement_type: str, interval: str, date_range: tuple
) -> list[dict]:
    if engagement_type not in ENGAGEMENT_TYPES or interval not in INTERVALS:
        raise ValueError("Please check your interval or engagement type.")
    output = []
    endpoint = f"{client.base_url}/contact_center/analytics/historical/queues/metrics"
    headers = {"Authorization": f"Bearer {client.token}"}
    params = {
        "next_page_token": "",
        "page_size": 100,
        "channel_types": [engagement_type],
        "interval": interval,
        "from": date_range[0],
        "to": date_range[1],
    }
    while True:
        try:
            r = requests.get(endpoint, headers=headers, params=params)
            r.raise_for_status()
            response = r.json()
            if "queues" in response:
                output.extend(response["queues"])
            params["next_page_token"] = response["next_page_token"]
            if not params["next_page_token"]:
                break
        except requests.HTTPError as err:
            logging.error(err)
            exit(1)
    return output
