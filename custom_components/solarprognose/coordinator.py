"""DataUpdateCoordinator for Solarprognose."""
import logging
import aiohttp
from datetime import timedelta
import homeassistant.util.dt as dt_util

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, API_URL, SCAN_INTERVAL, CONF_ACCESS_TOKEN, CONF_PROJECT, CONF_ITEM_TYPE, CONF_ITEM_ID

_LOGGER = logging.getLogger(__name__)

class SolarprognoseCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, entry_data: dict) -> None:
        """Initialize."""
        self.entry_data = entry_data
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from API and calculate sensor values."""
        params = {
            "access-token": self.entry_data[CONF_ACCESS_TOKEN],
            "project": self.entry_data[CONF_PROJECT],
            "item": self.entry_data[CONF_ITEM_TYPE],
            "id": self.entry_data[CONF_ITEM_ID],
            "type": "hourly",
            "algorithm": "mosmix",
            "_format": "json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

        return self._calculate_values(data.get("data", {}))

    def _calculate_values(self, api_data):
        """Translate the API timestamps into our required sensor values."""
        now = dt_util.now()
        today_str = now.strftime('%Y-%m-%d')
        tomorrow_str = (now + timedelta(days=1)).strftime('%Y-%m-%d')
        day_after_str = (now + timedelta(days=2)).strftime('%Y-%m-%d')
        current_hour_str = now.strftime('%Y-%m-%d %H')
        next_hour_str = (now + timedelta(hours=1)).strftime('%Y-%m-%d %H')

        current_ts = int(now.replace(minute=0, second=0, microsecond=0).timestamp())

        results = {
            "current_hour": 0.0,
            "next_hour": 0.0,
            "today": 0.0,
            "remaining_today": 0.0,
            "tomorrow": 0.0,
            "day_after_tomorrow": 0.0
        }

        for ts_str, vals in api_data.items():
            ts = int(ts_str)
            val = float(vals[0])
            
            # Zeitzonen-sicheres Parsen des Unix Timestamps
            ts_dt = dt_util.utc_from_timestamp(ts).astimezone(dt_util.DEFAULT_TIME_ZONE)
            date_str = ts_dt.strftime('%Y-%m-%d')
            hour_str = ts_dt.strftime('%Y-%m-%d %H')

            if hour_str == current_hour_str:
                results["current_hour"] = val * 1000 # convert to Watts
            if hour_str == next_hour_str:
                results["next_hour"] = val * 1000 # convert to Watts

            if date_str == today_str:
                results["today"] += val
                if ts >= current_ts:
                    results["remaining_today"] += val
            elif date_str == tomorrow_str:
                results["tomorrow"] += val
            elif date_str == day_after_str:
                results["day_after_tomorrow"] += val

        # Runden für eine saubere Darstellung
        results["today"] = round(results["today"], 3)
        results["remaining_today"] = round(results["remaining_today"], 3)
        results["tomorrow"] = round(results["tomorrow"], 3)
        results["day_after_tomorrow"] = round(results["day_after_tomorrow"], 3)
        
        results["current_hour"] = int(results["current_hour"])
        results["next_hour"] = int(results["next_hour"])

        return results
