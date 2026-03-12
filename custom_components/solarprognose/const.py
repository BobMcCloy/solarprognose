"""Constants for the Solarprognose integration."""
from datetime import timedelta

DOMAIN = "solarprognose"
CONF_PROJECT = "project"
CONF_ACCESS_TOKEN = "access_token"
CONF_ITEM_TYPE = "item_type"
CONF_ITEM_ID = "item_id"
CONF_NAME = "name"

API_URL = "https://solarprognose.de/web/solarprediction/api/v1"
SCAN_INTERVAL = timedelta(hours=1)

ITEM_TYPES = {
    "plant": "Plant (Anlage)",
    "inverter": "Inverter (Wechselrichter)",
    "module": "Module-Field (Modulfeld)"
}
