"""Config flow for Solarprognose integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_PROJECT,
    CONF_ACCESS_TOKEN,
    CONF_ITEM_TYPE,
    CONF_ITEM_ID,
    CONF_NAME,
    ITEM_TYPES
)

class SolarprognoseConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Solarprognose."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Hier könnte man die API testen, zur Vereinfachung übernehmen wir die Daten direkt.
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_ACCESS_TOKEN): str,
            vol.Required(CONF_PROJECT): str,
            vol.Required(CONF_ITEM_TYPE, default="plant"): vol.In(ITEM_TYPES),
            vol.Required(CONF_ITEM_ID): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
